import { useState, useCallback } from "react";
import constate from "constate";

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
const usePage = () => {
  const [page, setPage] = useState("Designer");

  const updatePage = (page?: string): void => setPage(page ?? "");

  return { page, updatePage };
};

export const [PageProvider, usePageContext] = constate(usePage);
