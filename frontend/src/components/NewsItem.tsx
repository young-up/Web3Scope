import { NewsArticle } from "@/lib/api";

export function NewsItem({ article }: { article: NewsArticle }) {
  return (
    <div className="bg-white/5 rounded-lg p-3 border border-white/10 hover:border-white/20 transition-all">
      <div className="flex items-start gap-3">
        <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 text-xs font-medium whitespace-nowrap mt-0.5">
          {article.source}
        </span>
        <div className="flex-1 min-w-0">
          <a
            href={article.link}
            target="_blank"
            rel="noopener noreferrer"
            className="text-white hover:text-blue-400 transition-colors line-clamp-2"
          >
            {article.title}
          </a>
          {article.published_at && (
            <p className="text-gray-500 text-xs mt-1">{article.published_at.slice(0, 10)}</p>
          )}
        </div>
      </div>
    </div>
  );
}
