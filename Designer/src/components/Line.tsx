import * as React from "react";

const convertToBoundingBox = (rect: DOMRect): [number, number, number, number] => [
  rect.left,
  rect.top,
  rect.left + rect.width,
  rect.top + rect.height,
];

export type LineType = "arrow" | "line" | "none";

export interface LineProps {
  lines: {
    startBox: [number, number, number, number];
    endBox: [number, number, number, number];
    marker?: LineType;
    isPhantom?: boolean;
  }[];
}

const MARKER_MAP = {
  arrow: "url(#arrow)",
  line: "url(#line)",
  none: undefined,
};

const COLOR_MAP = {
  arrow: "red",
  line: "blue",
  none: "black",
};

export const Lines: React.FunctionComponent<LineProps> = (props) => {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" className="designer-canvas-svg">
      <defs>
        <marker id="arrow" orient="auto" markerWidth="2" markerHeight="4" refX="1" refY="2">
          <path d="M0,0 V4 L2,2 Z" fill="red" />
        </marker>
        <marker id="line" orient="auto" markerWidth="1" markerHeight="4" refX="0" refY="2">
          <line x1="0" y1="0" x2="0" y2="4" stroke="blue" strokeWidth="3" />
        </marker>
      </defs>
      {props.lines.map((line, idx) => {
        const [Sx0, Sy0, Sx1, Sy1] = line.startBox;
        const [Ex0, Ey0, Ex1, Ey1] = line.endBox;

        const Sxm = (Sx0 + Sx1) / 2;
        const [A0x, A0y, A1x, A1y] = [Sxm, Sy0, Sxm, Sy1];
        const Exm = (Ex0 + Ex1) / 2;
        const [B0x, B0y, B1x, B1y] = [Exm, Ey0, Exm, Ey1];

        const points = [
          [0, 0],
          [0, 0],
          [0, 0],
          [0, 0],
        ];
        const DELTA = -30;
        if (B1y < A0y) {
          points[0] = [B1x, B1y];
          points[1] = [B1x, (B1y + A0y) / 2];
          points[2] = [A0x, (B1y + A0y) / 2];
          points[3] = [A0x, A0y];
        } else if (B0y <= A1y && B0y <= A0y) {
          points[0] = [B0x, B0y];
          points[1] = [B0x, B0y + DELTA];
          points[2] = [A0x, B0y + DELTA];
          points[3] = [A0x, A0y];
        } else if (B0y <= A1y) {
          points[0] = [B1x, B1y];
          points[1] = [B1x, B1y - DELTA];
          points[2] = [A1x, B1y - DELTA];
          points[3] = [A1x, A1y];
        } else {
          points[0] = [B0x, B0y];
          points[1] = [B0x, (B0y + A1y) / 2];
          points[2] = [A1x, (B0y + A1y) / 2];
          points[3] = [A1x, A1y];
        }

        return (
          <polyline
            key={idx}
            markerEnd={MARKER_MAP[line.marker ?? "none"]}
            stroke={COLOR_MAP[line.marker ?? "none"]}
            strokeWidth="3"
            fill="none"
            points={points.map((p) => p.join(",")).join(" ")}
            strokeDasharray={line.isPhantom ? "2 2" : undefined}
            // strokeDasharray="2 2"
          />
        );
      })}
    </svg>
  );
};

export interface PartLinesProps {
  lines: [Element | null, Element | null, LineType, boolean][];
}

export const PartLines: React.FunctionComponent<PartLinesProps> = (props) => {
  const { lines } = props;

  const [boxes, setBoxes] = React.useState<LineProps["lines"]>([]);

  React.useLayoutEffect(
    () =>
      setBoxes(
        lines
          .map(
            ([e, s, t, p]) =>
              s &&
              e && {
                startBox: convertToBoundingBox(s.getBoundingClientRect()),
                endBox: convertToBoundingBox(e.getBoundingClientRect()),
                marker: t,
                isPhantom: p,
              }
          )
          .filter((e) => e !== null) as LineProps["lines"]
      ),
    [lines]
  );

  return <Lines lines={boxes} />;
};

export default Lines;
