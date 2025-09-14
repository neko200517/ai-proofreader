import type { DiffSpan } from '@/lib/types';

type Props = {
  diffs: DiffSpan[];
};

export function DiffView({ diffs }: Props) {
  return (
    <div className='font-mono whitespace-pre-wrap leading-relaxed'>
      {diffs.map((d, i) => {
        const className =
          d.op === 1
            ? 'bg-green-100'
            : d.op === -1
            ? 'bg-red-100 line-through'
            : '';
        return (
          <span key={`${i}-${d.op}`} className={className}>
            {d.text}
          </span>
        );
      })}
    </div>
  );
}
