"use client";

import { DiffView } from "@/components/DiffView";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { proofread } from "@/lib/api";
import { makeDiffs } from "@/lib/diffs";
import type { ProofreadRes, Style, Tone } from "@/lib/types";
import { useMemo, useState } from "react";

const INPUT_LIMIT = Number(process.env.NEXT_PUBLIC_INPUT_LIMIT ?? 1200);

const TONES: Tone[] = ["社外-丁寧", "社外-強フォーマル", "社内-カジュアル"];
const STYLES: Style[] = ["依頼", "連絡", "報告", "謝罪"];

export default function Page() {
  const [text, setText] = useState<string>("");
  const [tone, setTone] = useState<Tone>("社外-丁寧");
  const [style, setStyle] = useState<Style>("依頼");
  const [result, setResult] = useState<ProofreadRes | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const diffs = useMemo(() => {
    if (!result) return [];
    return makeDiffs(text, result.revised);
  }, [text, result]);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!text.trim()) {
      setError("文章を入力してください。");
      return;
    }
    if (text.length > INPUT_LIMIT) {
      setError(
        `入力が長すぎます。${INPUT_LIMIT}文字以内でお試しください（無料体験の暫定制限）。`
      );
      return;
    }

    setLoading(true);
    try {
      const r = await proofread({ text, tone, style });
      setResult(r);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "エラーが発生しました。";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-5xl space-y-6 p-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">AI 文書校正（MVP）</h1>
        <Badge variant="secondary">体験版</Badge>
      </header>

      <Card>
        <CardHeader>
          <CardTitle>文章を入力</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={onSubmit} className="space-y-4">
            <div className="grid gap-3 md:grid-cols-3">
              <div className="space-y-1">
                <label className="text-sm text-slate-600">トーン</label>
                <Select value={tone} onValueChange={(v) => setTone(v as Tone)}>
                  <SelectTrigger>
                    <SelectValue placeholder="選択" />
                  </SelectTrigger>
                  <SelectContent>
                    {TONES.map((t) => (
                      <SelectItem key={t} value={t}>
                        {t}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1">
                <label className="text-sm text-slate-600">スタイル</label>
                <Select
                  value={style}
                  onValueChange={(v) => setStyle(v as Style)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="選択" />
                  </SelectTrigger>
                  <SelectContent>
                    {STYLES.map((s) => (
                      <SelectItem key={s} value={s}>
                        {s}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1">
                <label className="text-sm text-slate-600">文字数</label>
                <Input readOnly value={`${text.length}/${INPUT_LIMIT}`} />
              </div>
            </div>

            <Textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="ここに文章を貼り付けてください"
              className="h-44"
            />

            <div className="flex items-center gap-3">
              <Button type="submit" disabled={loading}>
                {loading ? "校正中…" : "校正する"}
              </Button>
              {error && <span className="text-sm text-red-600">{error}</span>}
            </div>
          </form>
        </CardContent>
      </Card>

      {result && (
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>原文</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="font-mono whitespace-pre-wrap">{text}</pre>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>修正文（差分）</CardTitle>
            </CardHeader>
            <CardContent>
              <DiffView diffs={diffs} />
              {result.reasons.length > 0 && (
                <ul className="mt-4 list-disc pl-5 text-sm text-slate-600">
                  {result.reasons.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </main>
  );
}
