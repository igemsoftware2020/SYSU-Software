export interface GenenetTask {
  id: string;
}

export interface GenenetRequest {
  species: number;
  iterations: number;
  regularize: boolean;
  prune: boolean;
  pruneLimit: number;
  start: number;
  end: number;
  curve: number[];
}

export interface GenenetResponse {
  finished: boolean;
  matrix: number[][];
}

export interface GenenetSResponse {
  Proposals?: {
    CDSs: {
      displayId: string;
      genenet_cds_id: number;
      role: string;
      title: string;
    }[];
    Promoters: {
      displayId: string;
      genenet_promoter_id: number;
      role: string;
      title: string;
    }[];
    n: number;
  };
}
