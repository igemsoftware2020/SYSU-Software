import * as React from "react";
import { FunctionComponent } from "react";
import { ComponentDefinition, PartTypes, roleArrayToType } from "../types/design";
import { useDrag } from "react-dnd";
import { ItemTypes } from "../types/dnd-types";
import { Tooltip, Classes } from "@blueprintjs/core";
import classnames from "classnames";

export interface PartProps {
  parentId?: string;
  id?: string;
  data: ComponentDefinition;
  clientRef?: (ref: HTMLDivElement | null, id?: string) => void;
  onClick?: React.MouseEventHandler<HTMLDivElement>;
  onMouseEnter?: React.MouseEventHandler<HTMLDivElement>;
  onMouseLeave?: React.MouseEventHandler<HTMLDivElement>;
  popover?: boolean;
}

export const Part: FunctionComponent<PartProps> = (props) => {
  const { role, displayId, title, description } = props.data;
  const { popover } = props;

  return (
    <div
      className="igem-part"
      igem-part-id={props.id}
      ref={(ref) => props.clientRef?.(ref, props.id)}
      onClick={props.onClick}
      onMouseEnter={props.onMouseEnter}
      onMouseLeave={props.onMouseLeave}
    >
      <img className="igem-part-icon" src={(PartTypes[role] ?? PartTypes["unknown"]).image} />
      {!popover ? (
        <span className="igem-part-name">{title}</span>
      ) : (
        <Tooltip className={classnames(Classes.TOOLTIP_INDICATOR, "igem-part-name")} content={description}>
          {title}
        </Tooltip>
      )}
    </div>
  );
};

export interface PartDragItem {
  type: ItemTypes.PART;
  parentId?: string;
  id?: string;
  data: ComponentDefinition;
}

export const DraggablePart: FunctionComponent<PartProps> = (props) => {
  const { data, parentId, id, clientRef } = props;
  const [{ isDragging }, drag] = useDrag({
    item: { type: ItemTypes.PART, parentId, id, data },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  });

  return (
    <div ref={drag}>
      <Part data={data} clientRef={clientRef} />
    </div>
  );
};

export default Part;
