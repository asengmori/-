<template>
  <div class="tao-companion">
    <!-- Floating character -->
    <div class="tao-float" @click="togglePanel">
      <div class="tao-avatar" :class="'wine-' + state.wineLevel">
        {{ taoEmoji }}
      </div>
      <div class="tao-badge" v-if="state.silver > 0">{{ state.silver }}</div>
    </div>

    <!-- Panel -->
    <div class="tao-panel" v-if="panelOpen" @click.self="panelOpen = false">
      <div class="panel-inner">
        <!-- Header -->
        <div class="panel-header">
          <div class="tao-big" :class="'wine-' + state.wineLevel">{{ taoEmoji }}</div>
          <div>
            <div class="tao-name">陶渊明</div>
            <div class="tao-mood">{{ wineLabel }}</div>
          </div>
          <button class="panel-close" @click="panelOpen = false">✕</button>
        </div>

        <!-- Stats -->
        <div class="tao-stats">
          <div class="stat-item">
            <span class="stat-icon">💰</span>
            <span class="stat-value">{{ state.silver }} 两</span>
          </div>
          <div class="stat-item">
            <span class="stat-icon">✅</span>
            <span class="stat-value">{{ state.totalCorrect }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-icon">❌</span>
            <span class="stat-value">{{ state.totalWrong }}</span>
          </div>
        </div>

        <!-- Wine shop -->
        <div class="wine-section">
          <div class="section-label">🍶 换酒</div>
          <button
            class="wine-btn"
            :disabled="!canBuyWine"
            @click="buyWine"
          >
            {{ wineBtnText }}
          </button>
        </div>

        <!-- Interaction area -->
        <div v-if="lastInteraction" class="interaction-area">
          <div class="bubble">{{ lastInteraction.text }}</div>
          <div class="interaction-type">{{ interactionLabel }}</div>
        </div>

        <!-- Quick actions -->
        <div v-if="state.wineLevel > 0" class="quick-actions">
          <button class="action-btn" @click="triggerInteraction">再聊两句</button>
          <button class="action-btn" @click="resetWine">醒醒酒</button>
        </div>

        <!-- Analytics -->
        <div class="analytics-section">
          <button class="analytics-btn" @click="showAnalytics"> 查看数据</button>
        </div>

        <!-- Analytics modal -->
        <div v-if="analyticsVisible" class="analytics-modal" @click.self="analyticsVisible = false">
          <div class="analytics-content">
            <div class="analytics-header">
              <span>📊 数据概览</span>
              <button class="modal-close" @click="analyticsVisible = false">✕</button>
            </div>
            <div class="analytics-body">
              <div class="stat-row">
                <span>总访问量</span>
                <strong>{{ analyticsSummary?.totalPageViews || 0 }}</strong>
              </div>
              <div class="stat-row">
                <span>开始刷题</span>
                <strong>{{ analyticsSummary?.eventsByType?.start_quiz || 0 }} 次</strong>
              </div>
              <div class="stat-row">
                <span>查看答案</span>
                <strong>{{ analyticsSummary?.eventsByType?.view_answer || 0 }} 次</strong>
              </div>
              <div class="stat-row">
                <span>答对</span>
                <strong>{{ analyticsSummary?.eventsByType?.answer_correct || 0 }} 次</strong>
              </div>
              <div class="stat-row">
                <span>答错</span>
                <strong>{{ analyticsSummary?.eventsByType?.answer_wrong || 0 }} 次</strong>
              </div>
              <div class="stat-row">
                <span>正确率</span>
                <strong>{{ accuracy }}</strong>
              </div>
              <div class="stat-row">
                <span>买酒次数</span>
                <strong>{{ analyticsSummary?.eventsByType?.buy_wine || 0 }}</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  loadTaoState, saveTaoState, spendWine,
  getRandomInteraction, getWineCost, earnSilver
} from '../tao.js'
import { trackEvent, exportAnalytics } from '../analytics.js'

const panelOpen = ref(false)
const state = ref(loadTaoState())
const lastInteraction = ref(null)
const analyticsVisible = ref(false)
const analyticsSummary = ref(null)

const taoEmoji = computed(() => {
  switch (state.value.wineLevel) {
    case 0: return '🧑‍🌾'
    case 1: return '😊'
    case 2: return '🥴'
    case 3: return '🤪'
    default: return '🧑‍🌾'
  }
})

const wineLabel = computed(() => {
  switch (state.value.wineLevel) {
    case 0: return '清醒中'
    case 1: return '微醺'
    case 2: return '醉了'
    case 3: return '大醉'
    default: return '清醒中'
  }
})

const canBuyWine = computed(() => {
  return state.value.silver >= getWineCost(state.value.wineLevel)
})

const wineBtnText = computed(() => {
  const cost = getWineCost(state.value.wineLevel)
  const labels = ['来壶淡酒', '再来一壶', '上好的！', '继续喝！']
  return `${labels[state.value.wineLevel] || '喝酒'} (${cost}两)`
})

const interactionLabel = computed(() => {
  if (!lastInteraction.value) return ''
  const map = {
    poem: '吟诗',
    talk: '闲聊',
    funny: '逗乐',
    qin: '弹琴',
    ask: '考你',
    sleep: '睡着了',
    reward: '彩蛋'
  }
  return map[lastInteraction.value.type] || ''
})

function togglePanel() {
  panelOpen.value = !panelOpen.value
  if (panelOpen.value) {
    trackEvent('tao_panel_open', { wineLevel: state.value.wineLevel })
    if (state.value.wineLevel > 0 && !lastInteraction.value) {
      triggerInteraction()
    }
  }
}

function buyWine() {
  const result = spendWine()
  if (result.success) {
    trackEvent('buy_wine', { cost: result.cost, newLevel: result.newState.wineLevel })
    state.value = result.newState
    triggerInteraction()
  }
}

function triggerInteraction() {
  if (state.value.wineLevel > 0) {
    lastInteraction.value = getRandomInteraction(state.value.wineLevel)
    trackEvent('tao_interaction', {
      wineLevel: state.value.wineLevel,
      type: lastInteraction.value.type
    })
  }
}

function resetWine() {
  state.value.wineLevel = 0
  lastInteraction.value = { text: '（喝口茶）清醒了清醒了……继续读书吧。', type: 'talk' }
  saveTaoState(state.value)
}

function showAnalytics() {
  analyticsSummary.value = exportAnalytics()
  analyticsVisible.value = true
  trackEvent('view_analytics')
}

const accuracy = computed(() => {
  const s = analyticsSummary.value
  if (!s) return '0%'
  const correct = s.eventsByType?.answer_correct || 0
  const wrong = s.eventsByType?.answer_wrong || 0
  const total = correct + wrong
  return total > 0 ? Math.round((correct / total) * 100) + '%' : '0%'
})

// Listen for events from quiz
window.addEventListener('tao-earn', (e) => {
  state.value = e.detail
})

window.addEventListener('tao-wrong', () => {
  state.value = loadTaoState()
})

onMounted(() => {
  state.value = loadTaoState()
})
</script>

<style scoped>
.tao-float {
  position: fixed;
  bottom: 70px;
  right: 16px;
  z-index: 50;
  cursor: pointer;
}

.tao-avatar {
  width: 52px;
  height: 52px;
  background: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  box-shadow: 0 3px 12px rgba(0,0,0,0.12);
  transition: all 0.3s;
  position: relative;
}

.tao-avatar:active {
  transform: scale(0.9);
}

.tao-avatar.wine-1 { animation: sway 2s infinite; }
.tao-avatar.wine-2 { animation: sway 1s infinite; }
.tao-avatar.wine-3 { animation: sway 0.5s infinite; }

@keyframes sway {
  0%, 100% { transform: rotate(-3deg); }
  50% { transform: rotate(3deg); }
}

.tao-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #6b4c3b;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  min-width: 20px;
  height: 20px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}

/* Panel */
.tao-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.4);
  z-index: 60;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.panel-inner {
  background: #faf9f7;
  border-radius: 24px 24px 0 0;
  width: 100%;
  max-width: 480px;
  max-height: 75vh;
  overflow-y: auto;
  padding: 20px;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  position: relative;
}

.tao-big {
  width: 56px;
  height: 56px;
  background: #fdf8f4;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
}

.tao-big.wine-1 { animation: sway 2s infinite; }
.tao-big.wine-2 { animation: sway 1s infinite; }
.tao-big.wine-3 { animation: sway 0.5s infinite; }

.tao-name {
  font-size: 18px;
  font-weight: 700;
  color: #2c2520;
}

.tao-mood {
  font-size: 13px;
  color: #8a7a6d;
}

.panel-close {
  position: absolute;
  right: 0;
  top: 0;
  background: none;
  border: none;
  font-size: 22px;
  cursor: pointer;
  color: #8a7a6d;
}

/* Stats */
.tao-stats {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.stat-item {
  flex: 1;
  background: #fff;
  border-radius: 12px;
  padding: 12px;
  text-align: center;
  box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}

.stat-icon {
  font-size: 18px;
  display: block;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 16px;
  font-weight: 700;
  color: #2c2520;
}

/* Wine section */
.wine-section {
  margin-bottom: 16px;
}

.section-label {
  font-size: 14px;
  color: #8a7a6d;
  font-weight: 600;
  margin-bottom: 8px;
}

.wine-btn {
  width: 100%;
  padding: 14px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #8B4513, #A0522D);
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.wine-btn:active { transform: scale(0.97); }
.wine-btn:disabled {
  background: #d4c9bb;
  cursor: not-allowed;
}

/* Interaction */
.interaction-area {
  background: #fdf8f4;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
}

.bubble {
  font-size: 16px;
  line-height: 1.7;
  color: #4a4238;
  margin-bottom: 6px;
}

.interaction-type {
  font-size: 12px;
  color: #a89b8e;
}

/* Quick actions */
.quick-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  flex: 1;
  padding: 12px;
  border-radius: 10px;
  border: 2px solid #e8e2da;
  background: #fff;
  font-size: 14px;
  color: #5a4d42;
  cursor: pointer;
  font-weight: 500;
}

.action-btn:active {
  border-color: #6b4c3b;
  color: #6b4c3b;
}

/* Analytics */
.analytics-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e8e2da;
}

.analytics-btn {
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  border: 2px dashed #e8e2da;
  background: transparent;
  font-size: 13px;
  color: #8a7a6d;
  cursor: pointer;
}

.analytics-btn:active {
  border-color: #6b4c3b;
  color: #6b4c3b;
}

.analytics-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 70;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.analytics-content {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 360px;
  overflow: hidden;
}

.analytics-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e8e2da;
  font-size: 16px;
  font-weight: 600;
}

.analytics-body {
  padding: 16px 20px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f0ede8;
  font-size: 14px;
}

.stat-row:last-child {
  border-bottom: none;
}

.stat-row strong {
  color: #6b4c3b;
}
</style>
