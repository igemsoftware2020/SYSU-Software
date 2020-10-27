import {
  Button,
  Callout,
  Classes,
  Dialog,
  FormGroup,
  H4,
  Icon,
  InputGroup,
  Intent,
  MenuItem,
  TextArea,
  Tooltip,
} from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import * as React from "react";
import { useState, useCallback, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useNewElement } from "../hooks/api";
import { Suggest } from "@blueprintjs/select";
import { PartTypes, SequenceEncodings } from "../types/design";
import { ArrayElement } from "../types/utils";
import { INewPart } from "../types/new-part";

export const NewPart: React.FunctionComponent = () => {
  const [dialogOpen, setDialogOpen] = useState(false);

  const onCreatePart = useCallback(() => setDialogOpen(true), []);
  const onDialogDismiss = useCallback(() => setDialogOpen(false), []);

  const { register, handleSubmit } = useForm<{
    name: string;
    description: string;
    type: string;
    sequence: string;
    sequenceType: string;
  }>({
    mode: "onSubmit",
  });

  const { data, loading, fire, error } = useNewElement();

  const onSubmit = handleSubmit((data) => {
    if (!(data.type in PartTypes)) {
      return;
    }
    const form: INewPart = {
      displayId: data.name,
      wasGeneratedBy: "https://maloadis.sysu.edu.cn",
      title: data.name,
      description: data.description,
      mutableProvenance: "",
      mutableDescription: "",
      mutableNotes: "",
      creator: "https://maloadis.sysu.edu.cn/anonymous",
      ownedBy: ["https://maloadis.sysu.edu.cn/anonymous"],
      role: data.type,
      Sequence: [],
    };
    if (data.sequence.length > 0 && data.sequenceType.length > 0) {
      form.Sequence.push({
        elements: data.sequence,
        encoding: data.sequenceType,
      });
    }
    fire(form);
  });

  const [resErr, setResErr] = useState("");

  useEffect(() => {
    if (!loading && !!data && !error) {
      if ((data as any).status) onDialogDismiss();
      else setResErr((data as any).message ?? "");
    }
  }, [data, loading, error, onDialogDismiss]);

  return (
    <>
      <Tooltip content="Create part in database">
        <Button className={Classes.MINIMAL} icon={IconNames.ADD_TO_ARTIFACT} onClick={onCreatePart} />
      </Tooltip>
      <Dialog isOpen={dialogOpen} onClose={onDialogDismiss}>
        <div className={Classes.DIALOG_HEADER}>
          <Icon icon={IconNames.ADD_TO_ARTIFACT} />
          <H4 className={Classes.HEADING}>Create part in database</H4>
        </div>
        <form onSubmit={onSubmit}>
          <div className={Classes.DIALOG_BODY}>
            <FormGroup label="Name" labelInfo="(required)">
              <InputGroup placeholder="Gene Name" name="name" inputRef={register({ required: true })} />
            </FormGroup>
            <FormGroup label="Description" labelInfo="(required)">
              <InputGroup placeholder="Description" name="description" inputRef={register({ required: true })} />
            </FormGroup>
            <FormGroup label="Type" labelInfo="(required)">
              <Suggest
                items={Object.entries(PartTypes)}
                itemRenderer={(item, { handleClick, modifiers }) => (
                  <MenuItem
                    key={item[0]}
                    text={item[1].name}
                    active={modifiers.active}
                    disabled={modifiers.disabled}
                    onClick={handleClick}
                  />
                )}
                inputValueRenderer={(item) => item[0]}
                inputProps={{
                  name: "type",
                  inputRef: register({ required: true }),
                }}
                fill
              />
            </FormGroup>
            <FormGroup label="Gene Sequence" labelInfo="(optional)">
              <TextArea placeholder="Sequence" fill name="sequence" inputRef={register} />
            </FormGroup>
            <FormGroup label="Gene Sequence Type" labelInfo="(optional)">
              <Suggest
                items={SequenceEncodings}
                itemRenderer={(item: ArrayElement<typeof SequenceEncodings>, { handleClick, modifiers }) => (
                  <MenuItem
                    key={item.uri}
                    text={item.name}
                    active={modifiers.active}
                    disabled={modifiers.disabled}
                    onClick={handleClick}
                  />
                )}
                inputValueRenderer={(item) => item.uri}
                inputProps={{
                  name: "sequenceType",
                  inputRef: register,
                }}
                fill
              />
            </FormGroup>
          </div>
          <div className={Classes.DIALOG_FOOTER}>
            {(error || resErr) && (
              <Callout intent={Intent.DANGER} className="igem-mb-small">
                {error ? JSON.stringify(error) : resErr}
              </Callout>
            )}
            <div className={Classes.DIALOG_FOOTER_ACTIONS}>
              <Button type="button" onClick={onDialogDismiss}>
                Cancel
              </Button>
              <Button type="submit" intent="primary" loading={loading}>
                Submit
              </Button>
            </div>
          </div>
        </form>
      </Dialog>
    </>
  );
};
