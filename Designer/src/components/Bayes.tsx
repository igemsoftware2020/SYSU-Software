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

    const startSession = (iterNum: number) => {
        conn?.invoke("Start", iterNum);
    }

    const provideResult = (result: number) => {
        conn?.invoke("ProvideResult", result);
    }

    useEffect(() => {
        const conn = new signalR.HubConnectionBuilder()
            .withAutomaticReconnect()
            .withUrl(`${Config.regonUri}/bayes`)
            .build();

        conn.start().catch(err => console.log(err));
        conn.on("ReceiveParameters", (x: number, y: number) => {
            console.log(`${x} ${y}`);
        });
        conn.on("ReceiveFinalResult", (target: number, x: number, y: number) => {
            console.log(`${target} ${x} ${y}`);
        });
        setConn(conn);
    }, []);

    const [param, setParam] = useState("");
    const [state, setState] = useState(0);
    const sendParam = () => {
        if (state === 0) {
            startSession(parseInt(param));
        }
        else {
            provideResult(parseFloat(param));
        }
        setState(state + 1);
    }

    return (
        <>
            <Tooltip content="Bayes Optimization">
                <Button className={Classes.MINIMAL} icon={IconNames.HEATMAP} onClick={showDialog} />
            </Tooltip>
            <Dialog icon={IconNames.LAB_TEST} title="Bayes Optimization" isOpen={open} onClose={hideDialog}>
                <InputGroup onChange={(e: React.ChangeEvent<HTMLInputElement>) => setParam(e.target.value)} />
                <Button onClick={() => sendParam()} />
            </Dialog>
        </>
    );
};
