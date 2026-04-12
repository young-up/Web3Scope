import { PriceData } from "@/lib/api";

export function PriceCard({ data }: { data: PriceData }) {
  const isUp = data.change_24h >= 0;
  return (
    <div className="bg-white/5 rounded-xl p-4 border border-white/10 hover:border-white/20 transition-all">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-400">{data.name || data.symbol}</p>
          <p className="text-xl font-bold mt-1">
            ${data.price?.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
        </div>
        <div className="flex flex-col items-end">
          <span className={`text-sm font-semibold ${isUp ? "text-green-400" : "text-red-400"}`}>
            {isUp ? "↑" : "↓"} {Math.abs(data.change_24h).toFixed(2)}%
          </span>
          <span className="text-xs text-gray-500 mt-1">
            MC: ${((data.market_cap || 0) / 1e9).toFixed(1)}B
          </span>
        </div>
      </div>
    </div>
  );
}
