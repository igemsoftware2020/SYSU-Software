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
  const [genes, setGenes] = useState<string>("3");
  const genesNum = React.useMemo(() => {
    const value = parseInt(genes);
    if (value > 0 && value < 6) {
      return value;
    } else {
      return 3;
    }
  }, [genes]);

  const startSession = (iterNum: number, geneNum: number) => {
    conn?.invoke("Start", geneNum, iterNum);
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
    conn.on("ReceiveParameters", (v: number[]) => {
      setValues(v);
    });
    conn.on("ReceiveFinalResult", (target: number, v: number[]) => {
      setValues([target, ...v]);
    });
    setConn(conn);
  }, []);

  const [param, setParam] = useState("");
  const [state, setState] = useState(0);
  const sendParam = () => {
    setValues([]);
    if (state === 0) {
      if (genesNum <= 5) {
        startSession(iters, genesNum);
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
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setGenes(e.target.value)}
              disabled={state !== 0}
              value={genes.toString()}
            />
          </FormGroup>
          {state <= iters + 1 ? (
            [...Array(genesNum).keys()].map((idx) => (
              <FormGroup key={idx} label={`Express Level of ${idx + 1}`}>
                <InputGroup disabled value={values[idx]?.toString() ?? ""} />
              </FormGroup>
            ))
          ) : (
            <>
              <FormGroup label="Target">
                <InputGroup disabled value={values[0]?.toString() ?? ""} />
              </FormGroup>
              {[...Array(genesNum).keys()].map((idx) => (
                <FormGroup key={idx} label={`Express Level of ${idx + 1}`}>
                  <InputGroup disabled value={values[idx + 1]?.toString() ?? ""} />
                </FormGroup>
              ))}
            </>
          )}
          {state <= iters + 1 && (
            <FormGroup
              label="Express Score"
              helperText="Express Score is used to describe the performance of your system, such as yield. The value range of Express level is [0,50], which linearly representes the genes expression level."
            >
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
