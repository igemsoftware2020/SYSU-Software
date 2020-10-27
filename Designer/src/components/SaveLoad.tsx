import { Button, Classes, FileInput } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import { useCallback, useState } from "react";
import * as React from "react";
import { useDesignerContext } from "../states/designer";
import { saveAs } from "file-saver";

export const SaveLoad: React.FunctionComponent = () => {
  const [err, setErr] = useState("");

  const { devices, links, setDevices, setLinks } = useDesignerContext();

  const onSaveClick = useCallback(() => {
    const blob = new Blob([JSON.stringify({ devices, links })], { type: "application/json;charset=utf-8" });
    saveAs(blob, prompt("filename = ?") || "design.json");
  }, [devices, links]);

  const onLoadFile: React.FormEventHandler<HTMLInputElement> = React.useCallback(
    (e) => {
      const work = async () => {
        const { devices: newDevices, links: newLinks } = JSON.parse((await e.currentTarget.files?.[0]?.text()) ?? "{}");
        setDevices(newDevices);
        setLinks(newLinks);
      };

      work();
    },
    [setDevices, setLinks]
  );

  const onOpenClick: React.MouseEventHandler<HTMLElement> = React.useCallback(
    (e) => document.getElementById("load-input")?.click(),
    []
  );

  return (
    <>
      <FileInput onInputChange={onLoadFile} style={{ display: "none" }} id="load-input" />
      <Button className={Classes.MINIMAL} icon={IconNames.DOCUMENT_OPEN} text="Open" onClick={onOpenClick} />
      <Button className={Classes.MINIMAL} icon={IconNames.SAVED} text="Save" onClick={onSaveClick} />
    </>
  );
};
