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
import { useState, useCallback, useMemo } from "react";
import { useForm } from "react-hook-form";
import { useSimulate } from "../hooks/api";
import { useDesignerContext } from "../states/designer";

export interface SimulationProps {
  shown?: boolean;
}

export const Simulation: React.FunctionComponent<SimulationProps> = (props) => {
  const { shown } = props;
  const [open, setOpen] = useState(shown ?? false);
  const showDialog = useCallback(() => setOpen(true), []);
  const hideDialog = useCallback(() => setOpen(false), []);

  const { data, loading, error, fire } = useSimulate();
  const { devices, links } = useDesignerContext();

  const proteins = useMemo(() => {
    return Object.values(devices).flatMap((d) => d.parts.filter((p) => p.data.role === "protein"));
  }, [devices]);

  const [targetData, setTargetData] = useState(["", ""]);
  const [mode, setMode] = useState("simulation");
  const onChangeMode: React.FormEventHandler<HTMLInputElement> = useCallback((e) => setMode(e.currentTarget.value), []);

  const { register, handleSubmit } = useForm<{
    parts: number[];
    ks: number[];
    ns: number[];
    ds: number[];
    is: number[];
    time: number;
    targetAmount: number;
  }>();
  const onSubmit = handleSubmit((data) => {
    const lookup = Object.fromEntries(data.is.map((i, id) => [i, id]));
    console.log(lookup);
    const parts = Object.fromEntries(data.parts.map((v, id) => [id, v]));
    const ks = Object.fromEntries(data.ks.map((v, id) => [id, v]));
    const ns = Object.fromEntries(data.ns.map((v, id) => [id, v]));
    const ds = Object.fromEntries(data.ds.map((v, id) => [id, v]));
    const lines = links
      .map(
        ([s, e, t]) =>
          lookup[s] &&
          lookup[e] && {
            start: lookup[s].toString(),
            end: lookup[e].toString(),
            type: t === "arrow" ? "stimulation" : "inhibition",
          }
      )
      .filter((v) => v);
    const time = data.time ?? 0;
    console.log(targetData);
    const target = lookup[targetData[0]].toString();
    const targetAmount = data.targetAmount ?? 0;
    const type = mode;
    fire({
      parts,
      ks,
      ns,
      ds,
      lines,
      time,
      target,
      targetAmount,
      type,
    });
  });

  return (
    <>
      <Tooltip content="Simulation">
        <Button className={Classes.MINIMAL} icon={IconNames.LAB_TEST} onClick={showDialog} />
      </Tooltip>
      <Dialog icon={IconNames.LAB_TEST} title="Simulation" isOpen={open} onClose={hideDialog}>
        <form onSubmit={onSubmit}>
          <div className={Classes.DIALOG_BODY}>
            <Callout intent={Intent.PRIMARY}>Click &quot;Start&quot; to {!data ? "run" : "rerun"} simulation.</Callout>
            {proteins.map((p, idx) => (
              <div key={p.id} className="igem-ptop-small">
                <H5>{p.data.title}</H5>
                <FormGroup label="Amount" labelInfo="umol">
                  <NumericInput
                    fill
                    name={`parts[${idx}]`}
                    placeholder={`Amount of ${p.data.title}`}
                    inputRef={register}
                  />
                </FormGroup>
                <FormGroup label="K" labelInfo="Kinetic Parameter">
                  <NumericInput
                    fill
                    name={`ks[${idx}]`}
                    placeholder={`Kinetic Parameter of ${p.data.title}`}
                    inputRef={register}
                  />
                </FormGroup>
                <FormGroup label="N" labelInfo="Repression Rate">
                  <NumericInput
                    fill
                    name={`ns[${idx}]`}
                    placeholder={`Repression Rate of ${p.data.title}`}
                    inputRef={register}
                  />
                </FormGroup>
                <FormGroup label="D" labelInfo="Degradation Rate">
                  <NumericInput
                    fill
                    name={`ds[${idx}]`}
                    placeholder={`Degradation Rate of ${p.data.title}`}
                    inputRef={register}
                  />
                </FormGroup>
                <input type="hidden" name={`is[${idx}]`} value={p.id} ref={register} />
              </div>
            ))}
            <Select
              items={proteins.map((p) => [p.id ?? "", p.data.title])}
              itemRenderer={(item, { handleClick, modifiers }) => (
                <MenuItem
                  key={item[0]}
                  text={item[1]}
                  active={modifiers.active}
                  disabled={modifiers.disabled}
                  onClick={handleClick}
                />
              )}
              onItemSelect={(item) => setTargetData(item)}
              filterable={false}
            >
              <Button
                rightIcon="caret-down"
                text={targetData[0].length > 0 ? `${targetData[1]} (${targetData[0]})` : "Select Target"}
              />
            </Select>
            <RadioGroup label="Mode" name="mode" onChange={onChangeMode} selectedValue={mode} inline>
              <Radio label="Simulation" value="simulation" />
              <Radio label="Optimization" value="optimization" />
            </RadioGroup>
            <FormGroup label="Reaction Time" labelInfo="hours">
              <NumericInput fill name="time" placeholder="Reaction Time" inputRef={register} />
            </FormGroup>
            {mode === "optimization" && (
              <FormGroup label="Target Amount" labelInfo="umol">
                <NumericInput fill name="targetAmount" placeholder="Target Amount" inputRef={register} />
              </FormGroup>
            )}
            {!loading && !data ? null : loading ? (
              <>
                <H3>Analyzing...</H3>
                <ProgressBar intent={Intent.PRIMARY} />
              </>
            ) : error ? (
              <Callout intent={Intent.DANGER}>{error}</Callout>
            ) : (
              <ReactEcharts option={data} />
            )}
          </div>
          <div className={Classes.DIALOG_FOOTER}>
            <div className={Classes.DIALOG_FOOTER_ACTIONS}>
              <Button type="submit">Start</Button>
              <Button onClick={hideDialog}>Close</Button>
            </div>
          </div>
        </form>
      </Dialog>
    </>
  );
};
