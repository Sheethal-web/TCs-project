# Analytics Dashboard

A production-grade React + Tailwind CSS analytics dashboard powered by **Claude AI** (Anthropic).

## Features

- 📊 Revenue & users area chart (Recharts)
- 🍩 Traffic sources donut chart
- 📅 Weekly sessions bar chart
- 📄 Top pages table with trend indicators
- 📈 Engagement progress bars
- 🤖 **AI Insights panel** — asks Claude to analyze your metrics in real time

## Tech Stack

| Tool | Purpose |
|------|---------|
| React 18 | UI framework |
| Vite | Dev server & bundler |
| Tailwind CSS | Styling |
| Recharts | Charts |
| Lucide React | Icons |
| Anthropic Claude API | AI-powered insights |

## Setup

### 1. Install dependencies

```bash
npm install
```

### 2. Add your Claude API key

Create a `.env` file at the project root:

```env
VITE_ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
```

Get your key at https://console.anthropic.com

### 3. Start the dev server

```bash
npm run dev
```

Open http://localhost:3000

## How the Claude Integration Works

The **AI Insights** panel at the bottom of the dashboard calls the Anthropic `/v1/messages` endpoint directly from the browser. It passes a snapshot of current dashboard metrics and asks Claude to surface key trends, anomalies, and recommendations.

You can also type follow-up questions like:
- *"Why might conversions be down?"*
- *"What day should we run our next campaign?"*
- *"Summarize the revenue trend in one sentence."*

Claude responds in real time with contextual, data-driven analysis.

## Project Structure

```
src/
├── components/
│   ├── MetricCard.jsx      # KPI cards with trend indicators
│   ├── RevenueChart.jsx    # Dual-axis area chart
│   ├── TrafficChart.jsx    # Donut chart by channel
│   ├── WeeklyChart.jsx     # Bar chart by day
│   ├── TopPages.jsx        # Session table
│   ├── ProgressStats.jsx   # Engagement bars
│   └── AIInsights.jsx      # Claude-powered analysis panel
├── data/
│   └── mockData.js         # Sample metrics + snapshot for Claude
├── services/
│   └── claudeApi.js        # Anthropic API wrapper
├── App.jsx                 # Main layout
├── main.jsx                # Entry point
└── index.css               # Tailwind + global styles
```

## Build for Production

```bash
npm run build
```

> ⚠️ Note: Your API key is embedded in the frontend bundle. For production, proxy Claude API calls through your own backend to keep the key secret.
