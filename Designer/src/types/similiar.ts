import { ComponentDefinition } from "./design";

export interface SimiliarResponse {
  message: string;
  status: number;
  response: SimiliarData;
}

export interface SimiliarData {
  "recursive-structure": SimiliarDataClass;
  structure: SimiliarDataClass;
  "recursive-element": SimiliarDataClass;
  element: SimiliarDataClass;
}

export interface SimiliarDataClass {
  iGEM: Record<string, SimiliarDataPoint>;
  paper: Record<string, SimiliarDataPoint>;
}

export interface SimiliarDataPoint {
  ComponentDefinition: ComponentDefinition[];
  description?: string;
  persistentIdentity?: string;
  article?: {
    abstract: string;
    authors: string;
    date: string;
    issue: number;
    jourName: string;
    title: string;
    type: number;
    url: string;
    vol: number;
  };
}
