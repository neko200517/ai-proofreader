import DiffMatchPatch from "diff-match-patch";
import type { DiffOp, DiffSpan } from "./types";

const dmp = new DiffMatchPatch();

export function makeDiffs(original: string, revised: string): DiffSpan[] {
  const raw = dmp.diff_main(original, revised);
  dmp.diff_cleanupSemantic(raw);

  return raw.map(([op, text]) => ({ op: op as DiffOp, text }));
}
