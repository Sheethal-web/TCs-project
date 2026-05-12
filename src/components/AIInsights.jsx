// src/components/AIInsights.jsx
import { useState } from 'react'
import { Sparkles, Send, AlertCircle, RefreshCw } from 'lucide-react'
import { getClaudeInsight } from '../services/claudeApi'
import { METRICS_SNAPSHOT } from '../data/mockData'

export default function AIInsights() {
  const [insight, setInsight]   = useState('')
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState('')
  const [question, setQuestion] = useState('')
  const [asked, setAsked]       = useState(false)

  async function fetchInsight(prompt = '') {
    setLoading(true)
    setError('')
    setInsight('')
    try {
      const text = await getClaudeInsight(METRICS_SNAPSHOT, prompt)
      setInsight(text)
      setAsked(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function handleAsk(e) {
    e.preventDefault()
    if (!question.trim() && !asked) return fetchInsight()
    fetchInsight(question)
    setQuestion('')
  }

  return (
    <div className="bg-surface-card border border-brand-600/40 rounded-2xl p-6 animate-slide-up animate-delay-400 relative overflow-hidden">
      {/* Glow accent */}
      <div className="absolute -top-12 -right-12 w-48 h-48 bg-brand-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="flex items-center gap-2 mb-4">
        <Sparkles size={16} className="text-brand-400" />
        <h3 className="text-sm font-semibold text-white">AI Insights</h3>
        <span className="ml-auto text-[10px] bg-brand-600/20 text-brand-400 border border-brand-600/30 px-2 py-0.5 rounded-full font-medium">
          Powered by Claude
        </span>
      </div>

      {/* Empty state */}
      {!insight && !loading && !error && (
        <div className="text-center py-6">
          <Sparkles size={28} className="text-brand-500/50 mx-auto mb-3" />
          <p className="text-sm text-zinc-500">
            Ask Claude to analyze your dashboard data and surface key insights.
          </p>
          <button
            onClick={() => fetchInsight()}
            className="mt-4 px-5 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-sm font-medium transition-colors"
          >
            Analyze now
          </button>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex items-center gap-3 py-6 text-zinc-400 text-sm">
          <RefreshCw size={16} className="animate-spin text-brand-400" />
          Claude is analyzing your metrics…
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="flex items-start gap-3 text-sm text-red-400 bg-red-500/10 border border-red-500/20 rounded-xl p-4">
          <AlertCircle size={16} className="mt-0.5 flex-shrink-0" />
          <span className="whitespace-pre-line">{error}</span>
        </div>
      )}

      {/* Insight text */}
      {insight && (
        <div className="text-sm text-zinc-300 leading-relaxed whitespace-pre-line mb-4">
          {insight}
        </div>
      )}

      {/* Input bar */}
      <form onSubmit={handleAsk} className="flex gap-2 mt-4">
        <input
          type="text"
          value={question}
          onChange={e => setQuestion(e.target.value)}
          placeholder="Ask a follow-up question…"
          className="flex-1 bg-surface-muted border border-surface-border rounded-xl px-4 py-2.5 text-sm text-white placeholder-zinc-600 outline-none focus:border-brand-600 transition-colors"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 disabled:opacity-50 disabled:cursor-not-allowed text-white transition-colors flex items-center gap-1.5"
        >
          <Send size={14} />
        </button>
      </form>
    </div>
  )
}
