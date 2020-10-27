/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import useFetch from "use-http";
import Config from "../config";
import { ComponentDefinition, Design } from "../types/design";
import { GenenetSResponse, GenenetTask } from "../types/genenet";
import { Recogn } from "../types/recogn";
import { SimiliarResponse } from "../types/similiar";

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export function useGet<T>(endpoint: string, dependencies: unknown[] = []) {
  const { data, loading, error } = useFetch<T>(endpoint, dependencies);

  return {
    data,
    loading,
    error: error?.message,
  };
}

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export function usePost<T>(endpoint: string, method: "POST" | "PATCH" | "PUT" | "DELETE") {
  const { post, put, patch, del, data, loading, error } = useFetch<T>(endpoint);

  // eslint-disable-next-line @typescript-eslint/ban-types
  const fire = <R extends object>(data?: R): void => {
    if (method === "POST") post(data);
    else if (method === "PUT") put(data);
    else if (method === "PATCH") patch(data);
    else if (method === "DELETE") del();
  };

  return {
    fire,
    data,
    loading,
    error: error?.message,
  };
}

export const useGenenetReq = () => usePost<GenenetTask>(`${Config.regonUri}/api/genenet_req`, "POST");
export const fetchGenenetRes = (id: string) => fetch(`${Config.regonUri}/api/genenet_res?id=${id}`);
export const useDetect = () => usePost<Recogn>(`${Config.regonUri}/api/detect`, "POST");
export const fetchElementWithRole = async (
  name: string,
  role: string
): Promise<{
  response: Record<string, ComponentDefinition>;
}> =>
  await (await fetch(`${Config.searchUri}/api/element/fuzzy/name=${encodeURIComponent(name || "*")}&limit=1`)).json();
export const useNewElement = () => usePost(`${Config.searchUri}/api/element/add`, "POST");
export const useElement = (query: string) =>
  useGet<{ response: Record<string, ComponentDefinition> }>(
    `${Config.searchUri}/api/element/like/name=${encodeURIComponent(query || "*")}&limit=50`,
    [query]
  );
export const useSimulate = () => usePost(`${Config.regonUri}/api/simulate`, "POST");

export const useGenenetSReq = () => usePost<GenenetTask>(`${Config.regonUri}/api/genenet_s_req`, "POST");
export const fetchGenenetSRes = (id: string): Promise<GenenetSResponse> =>
  fetch(`${Config.regonUri}/api/genenet_s_res?id=${id}`).then((r) => r.json());

export const fetchDesignSearch = (
  data: Design,
  mode: ("structure" | "rstructure" | "element" | "relement")[],
  limit = 5
): Promise<SimiliarResponse> =>
  fetch(`${Config.searchUri}/api/gene-circuit/search/mode=${mode.join("-")}&limit=${limit}`, {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  }).then((res) => res.json());
