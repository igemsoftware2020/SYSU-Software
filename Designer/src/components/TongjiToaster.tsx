import { AnchorButton, Classes, Dialog, Drawer, Intent, Position, Toast, Toaster } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import * as React from "react";
import classnames from "classnames";

const toaster = Toaster.create({
  position: Position.TOP_RIGHT,
});

export const TongjiToaster: React.FunctionComponent = () => {
  const [more, setMore] = React.useState(false);
  const onClick = React.useCallback(() => setMore(true), []);
  const onClose = React.useCallback(() => setMore(false), []);

  React.useEffect(() => {
    toaster.show({
      intent: Intent.PRIMARY,
      message: (
        <>
          Want to know how the change of enzyme will affect the metabolic status of your chassis?
          <br />
          Check <b>Synthesis Navigator</b> created by Tongji-Software
        </>
      ),
      action: { onClick, text: "Learn more" },
      timeout: 5000,
    });
  }, [onClick]);

  return (
    <Drawer isOpen={more} onClose={onClose} title="Find out about Synthesis Navigator">
      <div className={Classes.DRAWER_BODY}>
        <div className={classnames(Classes.DIALOG_BODY, Classes.UI_TEXT)}>
          <p>
            Synthesis Navigator is a toolbox for both iGEMers and those who work in synthetic biology, which inevitably
            involves the modification of cell metabolism.
          </p>
          <ul>
            <b>The Metabolism Simulation tool</b>
            <br /> observe how metabolism proceeds in a cell under different circumstances,
          </ul>
          <ul>
            <b>Pathway Finder</b>
            <br /> analyzes the target compound and its related pathways much easier than before.
          </ul>
          <p>
            The potential precursors and their pathways to a target compound can be found using this tool After design
            and modification, you can evaluate their engineering by utilizing the Metabolism Simulation, to avoid
            undesirable mistakes.
          </p>
          <AnchorButton href="https://www.tjigem.com/" icon={IconNames.GLOBE_NETWORK}>
            Visit their website
          </AnchorButton>
        </div>
      </div>
      <div className={Classes.DRAWER_FOOTER}></div>
    </Drawer>
  );
};
