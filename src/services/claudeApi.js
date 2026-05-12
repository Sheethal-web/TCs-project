// src/services/claudeApi.js
// Calls the Anthropic Claude API to generate AI-powered analytics insights.
// Set your VITE_ANTHROPIC_API_KEY in a .env file at the project root.

const ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/messages'
const MODEL = 'claude-sonnet-4-20250514'

/**
 * Ask Claude to analyze dashboard metrics and return insights.
 * @param {Object} metrics - The current dashboard metrics snapshot
 * @param {string} prompt - Optional custom question from the user
 * @returns {Promise<string>} - Claude's analysis text
 */
export async function getClaudeInsight(metrics, prompt = '') {
  const apiKey = import.meta.env.VITE_ANTHROPIC_API_KEY

  if (!apiKey) {
    throw new Error(
      'Missing VITE_ANTHROPIC_API_KEY. Create a .env file and add:\nVITE_ANTHROPIC_API_KEY=your_key_here'
    )
  }

  const systemPrompt = `You are an expert data analyst embedded in an analytics dashboard.
You receive metrics snapshots and provide concise, actionable insights.
Always respond in 2–4 short paragraphs. Be specific, data-driven, and direct.
Highlight anomalies, trends, and concrete recommendations.
Do not use bullet lists — write in clear prose.`

  const userMessage = prompt.trim()
    ? `Here are the current dashboard metrics:\n${JSON.stringify(metrics, null, 2)}\n\nUser question: ${prompt}`
    : `Analyze these dashboard metrics and give me the most important insights:\n${JSON.stringify(metrics, null, 2)}`

  const response = await fetch(ANTHROPIC_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 1000,
      system: systemPrompt,
      messages: [{ role: 'user', content: userMessage }],
    }),
  })

  if (!response.ok) {
    const err = await response.json().catch(() => ({}))
    throw new Error(err?.error?.message || `API error: ${response.status}`)
  }

  const data = await response.json()
  return data.content?.[0]?.text ?? 'No insight returned.'
}
