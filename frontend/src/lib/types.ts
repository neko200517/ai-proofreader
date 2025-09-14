export type Tone = "社外-丁寧" | "社外-強フォーマル" | "社内-カジュアル";
export type Style = "依頼" | "連絡" | "報告" | "謝罪";

export type ProofreadReq = {
  text: string;
  tone?: Tone;
  style?: Style;
};

export type ProofreadRes = {
  revised: string;
  reasons: string[];
};

export type DiffOp = -1 | 0 | 1;

export type DiffSpan = {
  op: DiffOp;
  text: string;
};
