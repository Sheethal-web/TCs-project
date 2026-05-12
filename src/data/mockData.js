// src/data/mockData.js

export const METRICS = {
  revenue:     { value: 84320,  prev: 75020,  label: 'Total Revenue',    prefix: '$', suffix: '' },
  users:       { value: 24819,  prev: 22950,  label: 'Active Users',      prefix: '',  suffix: '' },
  conversions: { value: 3204,   prev: 3280,   label: 'Conversions',       prefix: '',  suffix: '' },
  avgSession:  { value: '4m 32s', prev: null, label: 'Avg. Session',      prefix: '',  suffix: '' },
}

export const MONTHLY_DATA = [
  { month: 'Jan', revenue: 42000, users: 11200 },
  { month: 'Feb', revenue: 47000, users: 12800 },
  { month: 'Mar', revenue: 39000, users: 10900 },
  { month: 'Apr', revenue: 53000, users: 14100 },
  { month: 'May', revenue: 61000, users: 16200 },
  { month: 'Jun', revenue: 58000, users: 15700 },
  { month: 'Jul', revenue: 70000, users: 18400 },
  { month: 'Aug', revenue: 74000, users: 20100 },
  { month: 'Sep', revenue: 68000, users: 18900 },
  { month: 'Oct', revenue: 79000, users: 21800 },
  { month: 'Nov', revenue: 83000, users: 23500 },
  { month: 'Dec', revenue: 84320, users: 24819 },
]

export const TRAFFIC_SOURCES = [
  { name: 'Organic',  value: 44, color: '#6366f1' },
  { name: 'Direct',   value: 28, color: '#22d3ee' },
  { name: 'Referral', value: 16, color: '#a78bfa' },
  { name: 'Social',   value: 12, color: '#34d399' },
]

export const WEEKLY_SESSIONS = [
  { day: 'Mon', sessions: 3200 },
  { day: 'Tue', sessions: 4100 },
  { day: 'Wed', sessions: 3850 },
  { day: 'Thu', sessions: 4600 },
  { day: 'Fri', sessions: 4200 },
  { day: 'Sat', sessions: 2800 },
  { day: 'Sun', sessions: 1900 },
]

export const TOP_PAGES = [
  { path: '/home',    sessions: 9204,  change: '+4.2%' },
  { path: '/pricing', sessions: 5812,  change: '+11.8%' },
  { path: '/blog',    sessions: 4107,  change: '-1.4%' },
  { path: '/signup',  sessions: 3290,  change: '+7.0%' },
  { path: '/docs',    sessions: 2198,  change: '+2.9%' },
]

export const PROGRESS_STATS = [
  { label: 'Bounce Rate',      value: 34, color: '#6366f1' },
  { label: 'Return Visitors',  value: 62, color: '#22d3ee' },
  { label: 'Mobile Share',     value: 48, color: '#a78bfa' },
]

// Snapshot passed to Claude for analysis
export const METRICS_SNAPSHOT = {
  period: '30 days',
  revenue: { current: 84320, previous: 75020, changePercent: '+12.4%' },
  activeUsers: { current: 24819, previous: 22950, changePercent: '+8.1%' },
  conversions: { current: 3204, previous: 3280, changePercent: '-2.3%' },
  avgSessionSec: 272,
  topChannel: 'Organic (44%)',
  bounceRate: '34%',
  returnVisitors: '62%',
  mobileShare: '48%',
  topPage: { path: '/home', sessions: 9204 },
  bestDay: 'Thursday (4,600 sessions)',
  revenueGrowthTrend: 'Strong upward trend since Q1 dip in March',
}
