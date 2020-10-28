import {
  Tooltip,
  Button,
  Classes,
  Dialog,
  Callout,
  Intent,
  ProgressBar,
  H3,
  FormGroup,
  H5,
  InputGroup,
  MenuItem,
  RadioGroup,
  Radio,
  NumericInput,
  Toaster,
} from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import { Select } from "@blueprintjs/select";
import ReactEcharts from "echarts-for-react";
import * as React from "react";
import { useState, useCallback, useRef, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useDesignerContext } from "../states/designer";
import * as signalR from "@microsoft/signalr";
import Config from "../config";

export interface BayesProps {
  shown?: boolean;
}

export const Bayes: React.FunctionComponent<BayesProps> = (props: BayesProps) => {
  const { shown } = props;
  const [open, setOpen] = useState(shown ?? false);
  const showDialog = useCallback(() => setOpen(true), []);
  const hideDialog = useCallback(() => setOpen(false), []);
  const [conn, setConn] = useState<signalR.HubConnection | null>(null);
  const [values, setValues] = useState<number[]>([]);
  const [iters, setIters] = useState<number>(10);
  const [genes, setGenes] = useState<number>(3);

  const startSession = (iterNum: number, geneNum: number) => {
    conn?.invoke("Start", iterNum); // , geneNum);
  };

  const provideResult = (result: number) => {
    conn?.invoke("ProvideResult", result);
  };

  useEffect(() => {
    const conn = new signalR.HubConnectionBuilder()
      .withAutomaticReconnect()
      .withUrl(`${Config.regonUri}/bayes`)
      .build();

    conn.start().catch((err) => console.log(err));
    conn.on("ReceiveParameters", (x: number, y: number) => {
      setValues([x, y]);
    });
    conn.on("ReceiveFinalResult", (target: number, x: number, y: number) => {
      setValues([target, x, y]);
    });
    setConn(conn);
  }, []);

  const [param, setParam] = useState("");
  const [state, setState] = useState(0);
  const sendParam = () => {
    setValues([]);
    if (state === 0) {
      if (genes <= 5) {
        startSession(iters, genes);
      } else {
        Toaster.create().show({ message: "Gene count cannot be more than 5.", intent: "danger" });
      }
    } else {
      provideResult(parseFloat(param));
    }
    setState(state + 1);
  };

  return (
    <>
      <Tooltip content="Bayes Optimization">
        <Button className={Classes.MINIMAL} icon={IconNames.HEATMAP} onClick={showDialog} />
      </Tooltip>
      <Dialog icon={IconNames.HEATMAP} title="Bayes Optimization" isOpen={open} onClose={hideDialog}>
        <div className={Classes.DIALOG_BODY}>
          <FormGroup label="Iteration Count" labelInfo="(required)">
            <InputGroup
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                setIters(parseInt(e.target.value));
              }}
              disabled={state !== 0}
              value={iters.toString()}
            />
          </FormGroup>
          <FormGroup label="Gene Count" labelInfo="(required)">
            <InputGroup
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                setGenes(parseInt(e.target.value));
              }}
              disabled={state !== 0}
              value={genes.toString()}
            />
          </FormGroup>
          {state <= iters + 1 ? (
            [...Array(genes).keys()].map((idx) => (
              <FormGroup key={idx} label={`Express Level of ${idx + 1}`}>
                <InputGroup disabled value={values[idx]?.toString() ?? ""} />
              </FormGroup>
            ))
          ) : (
            <>
              <FormGroup label="Target">
                <InputGroup disabled value={values[0]?.toString() ?? ""} />
              </FormGroup>
              {[...Array(genes).keys()].map((idx) => (
                <FormGroup key={idx} label={`Express Level of ${idx + 1}`}>
                  <InputGroup disabled value={values[idx + 1]?.toString() ?? ""} />
                </FormGroup>
              ))}
            </>
          )}
          {state <= iters + 1 && (
            <FormGroup label="Express Score">
              <InputGroup
                value={param}
                disabled={state === 0}
                onChange={(e: React.FormEvent<HTMLInputElement>) => setParam(e.currentTarget.value)}
              />
            </FormGroup>
          )}
        </div>
        <div className={Classes.DIALOG_FOOTER}>
          <div className={Classes.DIALOG_FOOTER_ACTIONS}>
            <Button
              onClick={() => sendParam()}
              intent="primary"
              disabled={(state !== 0 && values[0] === undefined) || state > iters + 1}
            >
              {state === 0 ? "Start" : "Proceed"}
            </Button>
          </div>
        </div>
      </Dialog>
    </>
  );
};
