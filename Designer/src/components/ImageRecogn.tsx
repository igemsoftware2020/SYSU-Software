import * as React from "react";
import { useCallback, useState } from "react";

import { Button, Callout, Classes, Dialog, FileInput, Intent, ProgressBar, Tag } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";

import { v4 as uuid } from "uuid";
import { fetchElementWithRole, useDetect } from "../hooks/api";
import { DeviceProps } from "./Device";
import { PartProps } from "./Part";
import { ArrayElement } from "../types/utils";
import update from "immutability-helper";
import { ComponentDefinition } from "../types/design";

export interface ImageRecognProps {
  onResult: (id: string, data: DeviceProps) => void;
  shown?: boolean;
  highlight?: boolean;
}

export const ImageRecogn: React.FunctionComponent<ImageRecognProps> = (props) => {
  const { shown, onResult, highlight } = props;

  const [imageDialogOpen, setImageDialogOpen] = React.useState(shown ?? false);
  const handleOpenImageDialog = useCallback(() => setImageDialogOpen(true), []);
  const handleCloseImageDialog = useCallback(() => setImageDialogOpen(false), []);
  const { fire, loading, data, error } = useDetect();
  const [imageSelectFilename, setImageSelection] = React.useState<string | null>(null);
  const handleImageSelect: React.FormEventHandler<HTMLInputElement> = useCallback(
    (e) => {
      setImageSelection(e.currentTarget.value);

      const form = new FormData();
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      form.append("file", e.currentTarget.files?.[0] as any);

      fire(form);
    },
    [fire]
  );

  const [loadingPart, setLoadingPart] = useState(false);
  const [recognizedData, setRecognizedData] = useState<[string, boolean][][]>([]);

  React.useEffect(() => {
    const handler = async () => {
      if (data) {
        let top = 100;
        const left = 100;
        setLoadingPart(true);
        const partsMeta = Object.fromEntries<ComponentDefinition>(
          await Promise.all(
            data
              .flatMap((l) => l.map((p) => [p.name, p.type]))
              .map(
                async ([name, type]): Promise<[string, ComponentDefinition]> => [
                  name,
                  Object.values((await fetchElementWithRole(name, type)).response ?? {})[0],
                ]
              )
          )
        );
        const newRecognizedData: [string, boolean][][] = [];
        for (const line of data) {
          const parts = line.map((p) => (partsMeta[p.name] ? { id: uuid(), data: partsMeta[p.name] } : null));
          newRecognizedData.push(line.map((p) => [p.name, !!partsMeta[p.name]]));
          const id = uuid();
          const device: DeviceProps = {
            parts: parts.filter((d): d is Exclude<ArrayElement<typeof parts>, null> => d !== null),
            position: [top, left],
            id,
          };
          if (device.parts.length > 0) onResult(id, device);
          top += 200;
        }
        setRecognizedData(newRecognizedData);
      }
      setLoadingPart(false);
    };
    handler();
  }, [data]);

  return (
    <>
      <Button className={Classes.MINIMAL} icon={IconNames.EYE_OPEN} onClick={handleOpenImageDialog}>
        Image Recognition
      </Button>
      <Dialog
        icon={IconNames.EYE_OPEN}
        title="Select Image for Recognition"
        isOpen={imageDialogOpen}
        onClose={handleCloseImageDialog}
      >
        <div className={Classes.DIALOG_BODY}>
          <FileInput
            text={imageSelectFilename ?? "Choose file..."}
            fill
            hasSelection={imageSelectFilename !== null}
            onInputChange={handleImageSelect}
          />
          {(loading || loadingPart) && <ProgressBar intent={loading ? Intent.PRIMARY : Intent.WARNING} />}
          {error && (
            <Callout className="igem-mt-small" intent={Intent.DANGER}>
              {error}
            </Callout>
          )}
          {!loading && data && !loadingPart && (
            <>
              <Callout className="igem-mt-small" intent={Intent.SUCCESS}>
                Recognized parts added to canvas. The red ones are missing parts.
              </Callout>
              {recognizedData.map((d, dId) => (
                <div key={dId} className="igem-ptop-small">
                  {d.map((p, pId) => (
                    <Tag key={pId} intent={p[1] ? Intent.SUCCESS : Intent.DANGER} className="igem-mr-small">
                      {p[0]}
                    </Tag>
                  ))}
                </div>
              ))}
            </>
          )}
        </div>
        <div className={Classes.DIALOG_FOOTER}>
          <div className={Classes.DIALOG_FOOTER_ACTIONS}>
            <Button onClick={handleCloseImageDialog}>Close</Button>
          </div>
        </div>
      </Dialog>
    </>
  );
};
