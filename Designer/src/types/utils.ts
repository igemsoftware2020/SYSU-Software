export type ArrayElement<ArrayType extends readonly unknown[]> = ArrayType[number];
export const waitFor = (timeMs: number): Promise<void> =>
  new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    }, timeMs);
  });
