import { FunctionComponent } from "react";
import * as React from "react";
import { useDrag, useDrop, DragObjectWithType, DropTargetMonitor } from "react-dnd";
import { ItemTypes } from "../types/dnd-types";
import Part, { PartProps } from "./Part";
import classnames from "classnames";

export interface PartGapProps {
  index: number;
  onDrop?: (item: any, monitor: DropTargetMonitor, idx: number) => void;
}

export const PartGap: FunctionComponent<PartGapProps> = (props) => {
  const [{ isOver, canDrop, item }, drop] = useDrop({
    accept: ItemTypes.PART,
    collect: (monitor) => ({
      isOver: !!monitor.isOver(),
      canDrop: !!monitor.canDrop(),
      item: monitor.getItem(),
    }),
    drop: (i, m) => props.onDrop?.(i, m, props.index),
  });

  return (
    <div
      className={classnames("igem-part-divider", {
        "igem-hover": isOver && canDrop,
      })}
      ref={drop}
    >
      {isOver && canDrop && <Part data={item.data} />}
    </div>
  );
};

export interface DeviceProps {
  id?: string;
  parts: PartProps[];
  position: [number, number];
  onDrop?: (item: any, monitor: DropTargetMonitor, data: { id?: string; idx: number }) => void;
  clientRef?: (ref: HTMLDivElement | null, id?: string) => void;
  onPartClick?: React.MouseEventHandler<HTMLDivElement>;
  onPartMouseEnter?: React.MouseEventHandler<HTMLDivElement>;
  onPartMouseLeave?: React.MouseEventHandler<HTMLDivElement>;
}

export interface DeviceDragItem extends DragObjectWithType {
  id?: string;
  parts: PartProps[];
  type: ItemTypes.DEVICE;
}

export const Device: FunctionComponent<DeviceProps> = (props) => {
  const { id, parts, position, clientRef, onDrop, onPartClick, onPartMouseEnter, onPartMouseLeave } = props;

  const [{ isDragging }, drag] = useDrag({
    item: { type: ItemTypes.DEVICE, id, parts } as DeviceDragItem,
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  });

  const handleDrop = React.useCallback((item, monitor, idx) => onDrop?.(item, monitor, { id, idx }), [id, onDrop]);

  return (
    <div
      className={classnames("igem-device", {
        "igem-device-dragging": isDragging,
      })}
      ref={drag}
      style={{
        top: position[0],
        left: position[1],
      }}
      igem-device-id={id}
    >
      {parts
        .map((part, idx) => (
          <Part
            key={idx}
            {...part}
            clientRef={clientRef}
            onClick={onPartClick}
            onMouseEnter={onPartMouseEnter}
            onMouseLeave={onPartMouseLeave}
          />
        ))
        .reduce((r, a, i) => r.concat(a, <PartGap key={`G${i + 1}`} index={i + 1} onDrop={handleDrop} />), [
          <PartGap key={`G${0}`} index={0} onDrop={handleDrop} />,
        ])}
    </div>
  );
};

export const SimpleDevice: FunctionComponent<Pick<DeviceProps, "parts">> = (props) => {
  const { parts } = props;

  return (
    <div className="igem-device igem-device-simple">
      {parts.map((part, idx) => (
        <Part key={idx} {...part} />
      ))}
    </div>
  );
};

export default Device;
