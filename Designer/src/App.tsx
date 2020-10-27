import * as React from "react";
import { FunctionComponent } from "react";
import { Designer, Home } from "./pages";
import { Callout } from "@blueprintjs/core";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

const App: FunctionComponent = () => {
  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
        <Route path="/designer">
          <Designer />
        </Route>
      </Switch>
    </Router>
  );
};

export default App;
