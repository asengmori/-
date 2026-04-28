// 事件埋点 - 纯前端，数据存在 localStorage
const STORAGE_KEY = 'lit_quiz_analytics'

const defaultData = () => ({
  pageViews: {},      // { '/': 10, '/quiz/...': 5 }
  events: [],         // [{ type: 'start_quiz', timestamp, data }]
  sessionStart: Date.now(),
  lastExport: null
})

export function loadAnalytics() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved ? { ...defaultData(), ...JSON.parse(saved) } : defaultData()
  } catch {
    return defaultData()
  }
}

function saveAnalytics(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
}

// 页面访问
export function trackPageView(path) {
  const data = loadAnalytics()
  data.pageViews[path] = (data.pageViews[path] || 0) + 1
  saveAnalytics(data)
}

// 事件追踪
export function trackEvent(type, extra = {}) {
  const data = loadAnalytics()
  data.events.push({
    type,
    timestamp: Date.now(),
    ...extra
  })
  // 只保留最近 500 条
  if (data.events.length > 500) {
    data.events = data.events.slice(-500)
  }
  saveAnalytics(data)
}

// 导出数据（用于查看）
export function exportAnalytics() {
  const data = loadAnalytics()
  data.lastExport = Date.now()
  saveAnalytics(data)

  // 生成摘要
  const summary = {
    totalPageViews: Object.values(data.pageViews).reduce((a, b) => a + b, 0),
    pageViews: data.pageViews,
    totalEvents: data.events.length,
    eventsByType: {},
    sessionDuration: Math.round((Date.now() - data.sessionStart) / 1000),
    recentEvents: data.events.slice(-20)
  }

  data.events.forEach(e => {
    summary.eventsByType[e.type] = (summary.eventsByType[e.type] || 0) + 1
  })

  return summary
}

// 重置数据
export function resetAnalytics() {
  localStorage.removeItem(STORAGE_KEY)
}
