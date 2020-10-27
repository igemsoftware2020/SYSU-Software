import "core-js/stable";
import "regenerator-runtime/runtime";

import * as React from "react";
import * as ReactDOM from "react-dom";
import App from "./App";
import { PageProvider } from "./states/page";

ReactDOM.render(
  <PageProvider>
    <App />
  </PageProvider>,
  document.getElementById("root")
);
