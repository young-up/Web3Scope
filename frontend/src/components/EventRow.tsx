import { ChainEvent } from "@/lib/api";

function shortAddr(addr: string) {
  return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
}

function importanceColor(imp: string) {
  switch (imp) {
    case "high": return "text-red-400 bg-red-400/10";
    case "medium": return "text-yellow-400 bg-yellow-400/10";
    default: return "text-gray-400 bg-gray-400/10";
  }
}

export function EventRow({ event }: { event: ChainEvent }) {
  const imp = event.analysis?.importance || "low";
  return (
    <div className="bg-white/5 rounded-lg p-3 border border-white/10 hover:border-white/20 transition-all">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className={`px-2 py-0.5 rounded text-xs font-medium ${importanceColor(imp)}`}>
            {imp === "high" ? "🔴" : imp === "medium" ? "🟡" : "🟢"}{" "}
            {imp === "high" ? "重要" : imp === "medium" ? "关注" : "一般"}
          </span>
          <span className="text-white font-medium">{event.token}</span>
          <span className="text-gray-400 text-sm">
            {shortAddr(event.from_address)} → {shortAddr(event.to_address)}
          </span>
        </div>
        <div className="text-right">
          <p className="text-white font-medium">
            ${event.amount_usd.toLocaleString()}
          </p>
          <p className="text-gray-500 text-xs">{event.amount} {event.token}</p>
        </div>
      </div>
      {event.analysis?.summary && (
        <p className="text-gray-300 text-sm mt-2 ml-2">{event.analysis.summary}</p>
      )}
      <a
        href={`https://etherscan.io/tx/${event.hash}`}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-400 text-xs mt-1 ml-2 hover:underline block"
      >
        Etherscan →
      </a>
    </div>
  );
}
