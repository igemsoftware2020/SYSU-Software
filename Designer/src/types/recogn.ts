export interface RecognItem {
  name: string;
  type: string;
  boundingBox: {
    bottom: number;
    left: number;
    right: number;
    top: number;
  };
}

export type Recogn = RecognItem[][];
