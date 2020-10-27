import { useState, useCallback } from "react";
import constate from "constate";
import * as React from "react";
import { DeviceProps } from "../components/Device";
import { LineType } from "../components/Line";
import useUndo from "use-undo";

export enum DesignerState {
  DRAG = "DRAG",
  CONNECT = "CONNECT",
  DELETE = "DELETE",
}

type DesignerDeviceState = Record<string, DeviceProps>;

type DesignerLinkState = [string, string, LineType, boolean][];

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
const useDesigner = () => {
  const [editMode, setEditMode] = useState(DesignerState.DRAG);

  const [editArgs, setEditArgs] = useState<any>([]);

  // const [design, { set, reset, undo, redo, canUndo, canRedo }] = useUndo<[DesignerDeviceState, DesignerLinkState]>([
  //   {},
  //   [],
  // ]);

  // // const [devices, setDevices] = React.useState<DesignerDeviceState>({});
  // // const [links, setLinks] = React.useState<DesignerLinkState>([]);
  // const setDevices = useCallback((cv) => set([cv, design.present[1]]), [design.present, set]);
  // const setLinks = useCallback((cv) => set([design.present[0], cv]), [design.present, set]);

  // return {
  //   editMode,
  //   setEditMode,
  //   editArgs,
  //   setEditArgs,
  //   devices: design.present[0],
  //   setDevices,
  //   links: design.present[1],
  //   setLinks,
  // };

  const [devices, setDevices] = React.useState<DesignerDeviceState>({});
  const [links, setLinks] = React.useState<DesignerLinkState>([]);

  return {
    editMode,
    setEditMode,
    editArgs,
    setEditArgs,
    devices,
    setDevices,
    links,
    setLinks,
  };
};

export const [DesignerProvider, useDesignerContext] = constate(useDesigner);
