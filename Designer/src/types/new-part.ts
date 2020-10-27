export interface INewPart {
  displayId: string; // 必填，应与数据库中其它元件的名字不同
  wasGeneratedBy: string;
  title: string;
  description?: string;
  mutableProvenance: string;
  mutableDescription: string;
  mutableNotes: string;
  creator: string; // 必填, 给个用户名
  // 必填，给个用户专属的url
  ownedBy: string[];
  // 必填，可给出列表让用户选
  role: string;
  // 可有0或1个Sequence，基本不会录入
  Sequence: {
    // 对于一个Sequence, elements必填
    elements: string;
    // 提供列表让用户选择，列表详见Sequence_encoding.png。默认是”http://www.chem.qmul.ac.uk/iubmb/misc/naseq.html“
    encoding: string;
  }[];
}
