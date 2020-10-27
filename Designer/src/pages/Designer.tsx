import * as React from "react";
import { FunctionComponent, useRef, useCallback } from "react";
import { Alignment, Button, Classes, Navbar, Position, Toaster, Tooltip } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";

import { DndProvider, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { ItemTypes } from "../types/dnd-types";
import Device, { DeviceProps, DeviceDragItem } from "../components/Device";
import update from "immutability-helper";
import Search from "../components/Search";
import { PartDragItem } from "../components/Part";
import { v4 as uuid } from "uuid";
import { Container, Row, Col } from "react-grid-system";
import { saveAs } from "file-saver";

import { PartLines } from "../components/Line";
import { DesignerProvider, useDesignerContext, DesignerState } from "../states/designer";
import { Link, useLocation } from "react-router-dom";
import { ImageRecogn, ImageRecognProps } from "../components/ImageRecogn";
import { NewPart } from "../components/NewPart";
import { GeneNet } from "../components/GeneNet";
import { Simulation } from "../components/Simulation";
import { Similiar } from "../components/Similiar";
import { TongjiToaster } from "../components/TongjiToaster";
import { Bayes } from "../components/Bayes";
import { SaveLoad } from "../components/SaveLoad";

export const DesignerCanvas: FunctionComponent = () => {
  const { editMode, setEditMode, editArgs, setEditArgs, devices, setDevices, links, setLinks } = useDesignerContext();

  const [{ canDrop }, drop] = useDrop({
    accept: [ItemTypes.DEVICE, ItemTypes.PART],
    collect: (monitor) => ({
      canDrop: !!monitor.canDrop(),
    }),
    drop(item, monitor) {
      if (item.type === ItemTypes.DEVICE) {
        const data = item as DeviceDragItem;
        if (!data.id) {
          throw new Error("item.id cannot be null");
        }
        const group = devices[data.id];
        if (!group) {
          throw new Error("group not found");
        }
        const delta = monitor.getDifferenceFromInitialOffset();
        const top = group.position[0] + (delta?.y ?? 0);
        const left = group.position[1] + (delta?.x ?? 0);
        setDevices(
          update(devices, {
            [data.id]: {
              position: { $set: [top, left] },
            },
          })
        );
      } else if (item.type === ItemTypes.PART && !monitor.didDrop()) {
        const data = item as PartDragItem;
        const id = uuid();
        const { top, left } = document
          .getElementsByClassName("designer-canvas")
          ?.item?.(0)
          ?.getBoundingClientRect() ?? { top: 0, left: 0 };
        const { x, y } = monitor.getSourceClientOffset() ?? { x: left, y: top };
        const device: DeviceProps = {
          parts: [{ ...data, id: uuid(), parentId: id }],
          position: [y - top, x - left],
          id,
        };
        setDevices((prev) => {
          const ret = update(prev, { [id]: { $set: device } });
          return ret;
        });
      }
    },
  });

  const onDrop = useCallback(
    (item: PartDragItem, monitor, { id, idx }) => {
      setDevices((cur) =>
        update(cur, {
          [id]: {
            parts: {
              $splice: [[idx, 0, { data: item.data, parentId: id, id: uuid() }]],
            },
          },
        })
      );
    },
    [setDevices]
  );

  const partRef = useRef(new Map<string, Element | null>());

  const setPartRef = useCallback((ref: HTMLDivElement | null, id?: string) => {
    if (id) partRef.current.set(id, ref);
  }, []);

  const onConnectStimulate = useCallback(() => {
    setEditMode(DesignerState.CONNECT);
    setEditArgs(["arrow"]);
  }, [setEditMode, setEditArgs]);
  const onConnectInhibition = useCallback(() => {
    setEditMode(DesignerState.CONNECT);
    setEditArgs(["line"]);
  }, [setEditMode, setEditArgs]);
  const onResetMode = useCallback(() => {
    setEditMode(DesignerState.DRAG);
    setEditArgs([]);
  }, [setEditArgs, setEditMode]);

  const onPartClick: React.MouseEventHandler<HTMLDivElement> = useCallback(
    (e) => {
      const partId = e.currentTarget.getAttribute("igem-part-id") ?? "";
      if (editMode === DesignerState.CONNECT) {
        if (editArgs.length === 1) {
          editArgs.push(partId);
        } else {
          setLinks((pv) => {
            const index = pv.findIndex((e) => e[1] === partId && e[3] === true);
            return update(pv, {
              $splice: [[index, index >= 0 ? 1 : undefined]],
              $push: [[editArgs[1], partId, editArgs[0], false]],
            });
          });
          setEditArgs([]);
          setEditMode(DesignerState.DRAG);
        }
      } else if (editMode === DesignerState.DELETE) {
        setLinks(links.filter((l) => l[0] !== partId && l[1] !== partId));
        setDevices(
          Object.fromEntries(
            Object.entries(devices)
              .map((d): [string, DeviceProps] => [
                d[0],
                update(d[1], {
                  parts: { $set: d[1].parts.filter((p) => p.id !== partId) },
                }),
              ])
              .filter((d) => d[1].parts.length > 0)
          )
        );
        setEditMode(DesignerState.DRAG);
      }
    },
    [editMode, editArgs, setLinks, setEditArgs, setEditMode, links, setDevices, devices]
  );
  const onPartMouseEnter: React.MouseEventHandler<HTMLElement> = useCallback(
    (e) => {
      const partId = e.currentTarget.getAttribute("igem-part-id") ?? "";
      if (editMode === DesignerState.CONNECT) {
        if (editArgs.length > 1) {
          setLinks((pv) => update(pv, { $push: [[editArgs[1], partId, editArgs[0], true]] }));
        }
      }
    },
    [editMode, editArgs, setLinks]
  );
  const onPartMouseLeave: React.MouseEventHandler<HTMLDivElement> = useCallback(
    (e) => {
      if (editMode === DesignerState.CONNECT) {
        const partId = e.currentTarget.getAttribute("igem-part-id") ?? "";
        if (editArgs.length > 1) {
          setLinks((pv) => {
            const index = pv.findIndex((e) => e[1] === partId && e[3] === true);
            return update(pv, {
              $splice: [[index, index >= 0 ? 1 : undefined]],
            });
          });
        }
      }
    },
    [editMode, editArgs, setLinks]
  );

  const onDeletePart: React.MouseEventHandler<HTMLElement> = useCallback(() => {
    setEditMode(DesignerState.DELETE);
  }, [setEditMode]);

  const { hash: init } = useLocation();
  const onImageRecognResult: ImageRecognProps["onResult"] = (id, device) => {
    setDevices((cur) => update(cur, { [id]: { $set: device } }));
  };

  return (
    <div>
      <Navbar>
        <Navbar.Group align={Alignment.LEFT}>
          <Navbar.Heading>Maloadis</Navbar.Heading>
          <Navbar.Divider />
          <SaveLoad />
          <Navbar.Divider />
          <ImageRecogn shown={init === "#image"} onResult={onImageRecognResult} />
          <GeneNet shown={init === "#genenet"} />
          <Similiar />
          <Navbar.Divider />
          <Tooltip content="Drag mode">
            <Button className={Classes.MINIMAL} icon={IconNames.HAND} onClick={onResetMode} />
          </Tooltip>
          <Tooltip content="Connect parts (stimulate)">
            <Button className={Classes.MINIMAL} icon={IconNames.TRENDING_UP} onClick={onConnectStimulate} />
          </Tooltip>
          <Tooltip content="Connect parts (inhibition)">
            <Button className={Classes.MINIMAL} icon={IconNames.TRENDING_DOWN} onClick={onConnectInhibition} />
          </Tooltip>
          <Tooltip content="Delete part">
            <Button className={Classes.MINIMAL} icon={IconNames.DELETE} onClick={onDeletePart} />
          </Tooltip>
          <NewPart />
          <Navbar.Divider />
          <Simulation />
          <Tooltip content="Bayes optimization">
            <Bayes shown={init === "#bayes"} />
          </Tooltip>
        </Navbar.Group>
        <Navbar.Group align={Alignment.RIGHT}>
          <Navbar.Heading>Mode: {editMode}</Navbar.Heading>
        </Navbar.Group>
      </Navbar>
      <Container fluid>
        <Row>
          <Col xs={9}>
            <div ref={drop} className="designer-canvas">
              <PartLines
                lines={links.map(([s, e, t, p]) => [
                  partRef.current.get(s) ?? null,
                  partRef.current.get(e) ?? null,
                  t,
                  p,
                ])}
              />
              {Object.values(devices).map((group, idx) => (
                <Device
                  key={idx}
                  {...group}
                  onDrop={onDrop}
                  clientRef={setPartRef}
                  onPartClick={onPartClick}
                  onPartMouseEnter={onPartMouseEnter}
                  onPartMouseLeave={onPartMouseLeave}
                />
              ))}
            </div>
          </Col>
          <Col xs={3} className="igem-ptop-medium">
            <TongjiToaster />
            <Search />
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export const Designer: FunctionComponent = () => {
  return (
    <DesignerProvider>
      <DndProvider backend={HTML5Backend}>
        <DesignerCanvas />
      </DndProvider>
    </DesignerProvider>
  );
};

export default Designer;
