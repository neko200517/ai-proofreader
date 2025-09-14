import type { ProofreadReq, ProofreadRes } from "./types";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE?.replace(/\/$/, "") ||
  "http://localhost:8000";

export async function proofread(req: ProofreadReq): Promise<ProofreadRes> {
  const r = await fetch(`${API_BASE}/api/proofread`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!r.ok) {
    // サーバのエラー内容を拾って投げ返す
    let detail = "";
    try {
      const data: { detail?: string } = await r.json();
      detail = data.detail ?? "";
    } catch {
      // noop
    }
    throw new Error(detail || `HTTP ${r.status}`);
  }
  return r.json() as Promise<ProofreadRes>;
}
