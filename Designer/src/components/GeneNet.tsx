import * as React from "react";
import { useCallback, useState, useEffect } from "react";
import { v4 as uuid } from "uuid";

import {
  Button,
  Callout,
  Classes,
  Dialog,
  FormGroup,
  H3,
  HTMLTable,
  InputGroup,
  Intent,
  ProgressBar,
  Switch,
} from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";

import { fetchGenenetRes, fetchGenenetSRes, useGenenetReq, useGenenetSReq } from "../hooks/api";
import { GenenetRequest, GenenetResponse, GenenetSResponse } from "../types/genenet";
import update from "immutability-helper";
import classnames from "classnames";
import { waitFor } from "../types/utils";
import { DeviceProps, SimpleDevice } from "./Device";
import { ComponentDefinition } from "../types/design";
import { useDesignerContext } from "../states/designer";
import { PartProps } from "./Part";
import { LineType } from "./Line";

export interface GeneNetProps {
  shown?: boolean;
}

export const GeneNet: React.FunctionComponent<GeneNetProps> = (props) => {
  const { shown } = props;

  const { setDevices, setLinks } = useDesignerContext();

  const [genenetDialogOpen, setGenenetDialogOpen] = React.useState(shown ?? false);
  const handleOpenGenenetDialog = useCallback(() => setGenenetDialogOpen(true), []);
  const handleCloseGenenetDialog = useCallback(() => {
    setGenenetDialogOpen(false);
    setGeneState(0);
  }, []);
  const { fire: fireTask, loading: loadingTask, data: dataTask, error: errorTask } = useGenenetReq();
  const [result, setResult] = useState<GenenetResponse | null>(null);
  const [timerHandler, setTimerHandler] = useState<number>(0);
  const [geneState, setGeneState] = useState<number>(0);

  const [geneNetReq, setGeneNetReq] = useState<GenenetRequest>({
    species: 3,
    iterations: 1000,
    regularize: false,
    prune: false,
    pruneLimit: 1,
    start: 0,
    end: 2,
    curve: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
  });

  const handleStartGenenetTask = useCallback(() => {
    setResult(null);
    setGeneState(1);
    fireTask(geneNetReq);
  }, [fireTask, geneNetReq]);

  useEffect(() => {
    if (!loadingTask && dataTask?.id) {
      const work = async () => {
        const res = await fetchGenenetRes(dataTask.id);
        const data = await res.json();
        if (data.finished) {
          setResult(data);
        }
      };
      setTimerHandler(setInterval(work as TimerHandler, 5000));
    }
  }, [loadingTask, dataTask]);

  useEffect(() => {
    if (result?.finished) {
      setGeneState(2);
      if (timerHandler !== 0) {
        clearInterval(timerHandler);
        setTimerHandler(0);
      }
    }
  }, [result, timerHandler]);

  const inputStage = (
    <>
      <div className={Classes.DIALOG_BODY}>
        <FormGroup label="Species" labelFor="species-input" labelInfo="(required)">
          <InputGroup
            id="species-input"
            placeholder="Number of species"
            type="number"
            defaultValue={geneNetReq.species.toString()}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setGeneNetReq(
                update(geneNetReq, {
                  species: { $set: parseInt(e.target.value) },
                })
              )
            }
          />
        </FormGroup>
        <FormGroup label="Iterations" labelFor="iterations-input" labelInfo="(required)">
          <InputGroup
            id="iterations-input"
            placeholder="Time of iterations"
            type="number"
            defaultValue={geneNetReq.iterations.toString()}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setGeneNetReq(
                update(geneNetReq, {
                  iterations: { $set: parseInt(e.target.value) },
                })
              )
            }
          />
        </FormGroup>
        <Switch
          label="Regularize"
          defaultChecked={geneNetReq.regularize}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setGeneNetReq(update(geneNetReq, { regularize: { $set: e.target.checked } }))
          }
        />
        <Switch
          label="Prune"
          defaultChecked={geneNetReq.prune}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setGeneNetReq(update(geneNetReq, { prune: { $set: e.target.checked } }))
          }
        />
        <FormGroup label="Prune Limit" labelFor="prune-limit-input" labelInfo="(only required if [Prune] is on)">
          <InputGroup
            id="prune-limit-input"
            placeholder="Limit of prune"
            type="number"
            defaultValue={geneNetReq.pruneLimit.toString()}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setGeneNetReq(
                update(geneNetReq, {
                  pruneLimit: { $set: parseFloat(e.target.value) },
                })
              )
            }
          />
        </FormGroup>
        <FormGroup label="X-axis left" labelFor="start-input" labelInfo="(required)">
          <InputGroup
            id="start-input"
            placeholder="Left position on X-axis"
            type="number"
            defaultValue={geneNetReq.start.toString()}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setGeneNetReq(
                update(geneNetReq, {
                  start: { $set: parseFloat(e.target.value) },
                })
              )
            }
          />
        </FormGroup>
        <FormGroup label="X-axis right" labelFor="end-input" labelInfo="(required)">
          <InputGroup
            id="end-input"
            placeholder="Right position on X-axis"
            type="number"
            defaultValue={geneNetReq.end.toString()}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setGeneNetReq(
                update(geneNetReq, {
                  end: { $set: parseFloat(e.target.value) },
                })
              )
            }
          />
        </FormGroup>
        <FormGroup label="Y-axis values" labelFor="curve-input" labelInfo="(required)">
          <InputGroup
            id="curve-input"
            placeholder="Values on Y-axis, exmaple: 1.0,1.2,1.4,1.6"
            defaultValue={geneNetReq.curve.toString()}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setGeneNetReq(
                update(geneNetReq, {
                  curve: {
                    $set: e.target.value.split(",").map((i) => parseFloat(i.trim())),
                  },
                })
              )
            }
          />
        </FormGroup>
      </div>
      <div className={Classes.DIALOG_FOOTER}>
        <div className={Classes.DIALOG_FOOTER_ACTIONS}>
          <Button onClick={handleStartGenenetTask} intent={Intent.PRIMARY}>
            Start
          </Button>
          <Button onClick={handleCloseGenenetDialog}>Close</Button>
        </div>
      </div>
    </>
  );

  const analyzingStage = (
    <div className={Classes.DIALOG_BODY}>
      <H3>Analyzing...</H3>
      <ProgressBar intent={"primary"} />
    </div>
  );

  // result stage: display matrix and run search

  const [isl, setIsl] = useState("0");
  const onIslChange: React.FormEventHandler<HTMLInputElement> = (e) => {
    setIsl(e.currentTarget.value);
  };
  const { fire: fireSearch, loading: loadingSearch, data: dataSearch, error: errorSearch } = useGenenetSReq();
  const handleMatrixProceed = useCallback(() => {
    fireSearch({
      matrix: result?.matrix,
      initSeqLen: Number.parseInt(isl, 10),
    });
  }, [fireSearch, isl, result?.matrix]);

  const [sResult, setSResult] = useState<GenenetSResponse | null>(null);

  useEffect(() => {
    if (!loadingSearch && dataSearch?.id) {
      const work = async () => {
        setSResult(null);
        for (;;) {
          await waitFor(1000);
          const data = await fetchGenenetSRes(dataSearch.id);
          if (data.Proposals) {
            setSResult(data);
            break;
          }
        }
      };

      work();
    }
  }, [loadingSearch, dataSearch]);

  const resultStage = (
    <>
      <div className={Classes.DIALOG_BODY}>
        <H3>Analysis result</H3>
        <HTMLTable className={classnames(Classes.HTML_TABLE_BORDERED, Classes.HTML_TABLE_CONDENSED)}>
          <thead>
            <tr>
              <th></th>
              {result?.matrix?.[0].map((_, idx) => (
                <th key={idx}>{idx}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {result?.matrix.map((row, idx) => (
              <tr key={idx}>
                <td>{idx}</td>
                {row.map((cell, idc) => (
                  <td key={idc}>{Math.abs(cell) >= 0.5 ? <b>{cell}</b> : cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </HTMLTable>
        <FormGroup helperText="which will be added to the gene length limit" label="Initial Sequence Length">
          <InputGroup placeholder="Initial Sequence Length" onChange={onIslChange} value={isl.toString()} />
        </FormGroup>
        {!loadingSearch && sResult && (
          <Callout className="igem-mt-small" intent={Intent.SUCCESS}>
            Circuit added to canvas.
          </Callout>
        )}
      </div>
      <div className={Classes.DIALOG_FOOTER}>
        <div className={Classes.DIALOG_FOOTER_ACTIONS}>
          <Button onClick={handleMatrixProceed} intent={Intent.PRIMARY} loading={loadingSearch}>
            Proceed
          </Button>
          <Button onClick={handleCloseGenenetDialog}>Close</Button>
        </div>
      </div>
    </>
  );

  useEffect(() => {
    if (sResult?.Proposals) {
      const promoters = sResult.Proposals.Promoters;
      const cdss = sResult.Proposals.CDSs;
      const n = sResult.Proposals.n;

      const all = promoters.map((i) => [{ id: uuid(), data: (i as any) as ComponentDefinition }]);
      const links: [string, string, LineType, boolean][] = [];
      for (const c of cdss) {
        const [i, j] = [Math.floor(c.genenet_cds_id / n), c.genenet_cds_id % n];
        const id = uuid();
        all[j].push({ id, data: (c as any) as ComponentDefinition });
        links.push([id, all[i][0].id, (result?.matrix[i][j] ?? 0) > 0 ? "arrow" : "line", false]);
      }
      console.log(links);
      setDevices((pv) =>
        update(
          pv,
          Object.fromEntries(
            all.map((v, idx) => {
              const id = uuid();
              const device: DeviceProps = {
                parts: v.map((pv) => ({ ...pv, parentId: id })),
                position: [100 + 200 * idx, 100],
                id,
              };
              return [id, { $set: device }];
            })
          )
        )
      );
      setLinks((pv) => update(pv, { $push: links }));
    }
  }, [result?.matrix, sResult, setDevices, setLinks]);

  return (
    <>
      {" "}
      <Button className={Classes.MINIMAL} icon={IconNames.PREDICTIVE_ANALYSIS} onClick={handleOpenGenenetDialog}>
        Genenet Automation
      </Button>
      <Dialog
        icon={IconNames.PREDICTIVE_ANALYSIS}
        title="GeneNet Automation Analysis"
        isOpen={genenetDialogOpen}
        onClose={handleCloseGenenetDialog}
      >
        {/* eslint-disable indent */}
        {geneState === 0 ? inputStage : geneState === 1 ? analyzingStage : resultStage}
        {/* eslint-enable indent */}
      </Dialog>
    </>
  );
};
