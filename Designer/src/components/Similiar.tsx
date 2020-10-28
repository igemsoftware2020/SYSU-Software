import * as React from "react";
import { useCallback, useState, useEffect } from "react";

import { AnchorButton, Button, Callout, Checkbox, Classes, Drawer, H3, H4, H5, Intent } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";

import { fetchDesignSearch } from "../hooks/api";
import { useForm } from "react-hook-form";
import { useDesignerContext } from "../states/designer";
import { SimiliarResponse } from "../types/similiar";
import { SimpleDevice } from "./Device";

interface SimiliarSearchProps {
  onResult?: (result: SimiliarResponse) => void;
  onClose?: () => void;
}

const SimiliarSearch: React.FunctionComponent<SimiliarSearchProps> = (props) => {
  const { onResult, onClose } = props;
  const [loading, setLoading] = useState(false);

  const { register, handleSubmit } = useForm<{
    element: boolean;
    relement: boolean;
    rstructure: boolean;
    structure: boolean;
  }>();

  const { devices, links } = useDesignerContext();
  const onRun = handleSubmit((data) => {
    const mode: ("structure" | "rstructure" | "element" | "relement")[] = [];
    if (data.structure) {
      mode.push("structure");
    }
    if (data.rstructure) {
      mode.push("rstructure");
    }
    if (data.element) {
      mode.push("element");
    }
    if (data.relement) {
      mode.push("relement");
    }

    const fire = async () => {
      setLoading(true);
      console.log(devices);
      console.log(links);
      const keys = Object.keys(devices);
      if (keys.length === 0) return;
      const device = devices[keys[0]];

      const data = await fetchDesignSearch(
        {
          persistentIdentity: keys[0],
          article: null,
          description: null,
          Activity: [],
          ComponentDefinition: device.parts.map((i) => i.data),
        },
        mode
      );
      onResult?.(data);
    };

    fire()
      .catch(console.error)
      .finally(() => setLoading(false));
  });

  return (
    <form onSubmit={onRun}>
      <div className={Classes.DIALOG_BODY}>
        <Callout intent={Intent.PRIMARY}>Click &quot;Run&quot; to search for similiar designs.</Callout>
        <H3 className="igem-mt-small">Mode</H3>
        <Checkbox label="Match structure" inputRef={register} name="structure" />
        <Checkbox label="Match structure (recursive)" inputRef={register} name="rstructure" />
        <Checkbox label="Match element" inputRef={register} name="element" />
        <Checkbox label="Match element (recursive)" inputRef={register} name="relement" />
      </div>
      <div className={Classes.DIALOG_FOOTER}>
        <div className={Classes.DIALOG_FOOTER_ACTIONS}>
          <Button type="submit" intent={Intent.PRIMARY} loading={loading}>
            Run
          </Button>
          <Button onClick={onClose}>Close</Button>
        </div>
      </div>
    </form>
  );
};

interface SimiliarResultProps {
  data: SimiliarResponse;
  onClose?: () => void;
}

const SimiliarResult: React.FunctionComponent<SimiliarResultProps> = (props) => {
  const { data, onClose } = props;
  const results = data && {
    iGEM: Object.values(data.response.element?.iGEM ?? {})
      .concat(Object.values(data.response["recursive-element"]?.iGEM ?? {}))
      .concat(Object.values(data.response["recursive-structure"]?.iGEM ?? {}))
      .concat(Object.values(data.response["structure"]?.iGEM ?? {})),
    paper: Object.values(data.response.element?.paper ?? {})
      .concat(Object.values(data.response["recursive-element"]?.paper ?? {}))
      .concat(Object.values(data.response["recursive-structure"]?.paper ?? {}))
      .concat(Object.values(data.response["structure"]?.paper ?? {})),
  };
  return (
    <>
      <div className={Classes.DIALOG_BODY}>
        <H3>Results</H3>
        <H4>SynBioHub</H4>
        {results.iGEM.map((d, idx) => (
          <React.Fragment key={idx}>
            <H5>
              {d.persistentIdentity}{" "}
              <AnchorButton
                href={`https://synbiohub.org/public/igem/${d.persistentIdentity}`}
                rightIcon="share"
                target="_blank"
                minimal
              />
            </H5>
            <SimpleDevice
              parts={
                d.ComponentDefinition.find((c) => c.displayId === d.persistentIdentity)?.Component?.map((p) => ({
                  data: d.ComponentDefinition.find((c) => c.persistentIdentity === p.definition.replace("/1", ""))!,
                })) ?? []
              }
            />
          </React.Fragment>
        ))}
        <H4>Articles</H4>
        {results.paper.map((d, idx) => (
          <React.Fragment key={idx}>
            <H5>
              {d.article?.title} <AnchorButton href={d.article?.url} rightIcon="share" target="_blank" minimal />
            </H5>
            <p>
              {JSON.parse(d.article?.authors ?? "[]").join(",")} {d.article?.jourName}
            </p>
            <SimpleDevice
              parts={d.ComponentDefinition.map((p) => ({
                data: { ...p, role: p.role.toLowerCase(), title: p.title ?? p.displayId },
              }))}
            />
          </React.Fragment>
        ))}
      </div>
      <div className={Classes.DIALOG_FOOTER}>
        <div className={Classes.DIALOG_FOOTER_ACTIONS}>
          <Button onClick={onClose}>Close</Button>
        </div>
      </div>
    </>
  );
};

export const Similiar: React.FunctionComponent = () => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const onOpenDialog = useCallback(() => {
    setDialogOpen(true);
    setResult(null);
  }, []);
  const onCloseDialog = useCallback(() => setDialogOpen(false), []);

  const [result, setResult] = useState<SimiliarResponse | null>(null);
  const onResult = useCallback((data) => setResult(data), []);

  return (
    <>
      <Button className={Classes.MINIMAL} icon={IconNames.GEOSEARCH} onClick={onOpenDialog}>
        Similiar Circuits
      </Button>
      <Drawer
        icon={IconNames.GEOSEARCH}
        title="Find similiar circuits"
        isOpen={dialogOpen}
        onClose={onCloseDialog}
        style={{ overflowY: "scroll" }}
      >
        {!result && <SimiliarSearch onClose={onCloseDialog} onResult={onResult} />}
        {result && <SimiliarResult data={result} onClose={onCloseDialog} />}
      </Drawer>
    </>
  );
};
