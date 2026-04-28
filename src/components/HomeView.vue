<template>
  <div>
    <div class="header">
      <div class="header-title">文学考研刷题</div>
      <div class="header-subtitle">每天进步一点点</div>
    </div>

    <!-- 选择方向 -->
    <div class="section">
      <div class="section-title">选择方向</div>
      <div class="category-grid">
        <div
          v-for="cat in categories"
          :key="cat.id"
          class="category-card"
          :class="{ selected: selectedCategory === cat.id }"
          @click="selectCategory(cat.id)"
        >
          <div class="category-icon">{{ cat.icon }}</div>
          <div class="category-name">{{ cat.name }}</div>
          <div class="category-count">
            名词 {{ getNounCount(cat.id) }} · 填空 {{ getBlankCount(cat.id) }}
          </div>
        </div>
      </div>
    </div>

    <!-- 选择题型 -->
    <div class="section" v-if="selectedCategory">
      <div class="section-title">选择题型</div>
      <div class="type-list">
        <button
          v-for="type in questionTypes"
          :key="type.id"
          class="type-btn"
          :class="{ selected: selectedType === type.id }"
          @click="selectedType = type.id"
        >
          {{ type.name }}
        </button>
      </div>
    </div>

    <!-- 选择学习模式 -->
    <div class="section" v-if="selectedType === 'noun'">
      <div class="section-title">学习模式</div>
      <div class="mode-list">
        <button
          class="mode-btn"
          :class="{ selected: mode === 'shuffle' }"
          @click="mode = 'shuffle'"
        >
          🔀 随机
        </button>
        <button
          class="mode-btn"
          :class="{ selected: mode === 'sequential' }"
          @click="mode = 'sequential'"
        >
          📖 正序
        </button>
      </div>
    </div>

    <!-- 正序模式下选择单元 -->
    <div class="section" v-if="mode === 'sequential' && selectedCategory">
      <div class="section-title">选择单元</div>
      <div class="chapter-list">
        <div
          v-for="ch in chapters"
          :key="ch.id"
          class="chapter-item"
          :class="{ selected: selectedChapter === ch.id }"
          @click="selectedChapter = ch.id"
        >
          <span class="chapter-idx">{{ ch.idx }}</span>
          <span class="chapter-name">{{ ch.name }}</span>
          <span class="chapter-count">{{ ch.count }}题</span>
        </div>
      </div>
    </div>

    <!-- 开始按钮 -->
    <div class="section">
      <button
        class="start-btn"
        :disabled="!canStart"
        @click="startQuiz"
      >
        开始刷题
      </button>
    </div>

    <div class="bottom-spacer"></div>

    <!-- 底部 Tab -->
    <div class="tab-bar">
      <div class="tab-item active" @click="$router.push('/')">
        <div class="tab-icon">📚</div>
        <div class="tab-label">刷题</div>
      </div>
      <div class="tab-item" @click="$router.push('/wrong')">
        <div class="tab-icon">📝</div>
        <div class="tab-label">错题本 <span v-if="wrongCount" style="color:#c0392b">({{ wrongCount }})</span></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  categories, questionTypes,
  nounExplanations, fillBlanks, chapterInfo
} from '../data/questions.js'
import { getWrongItems } from '../store.js'
import { trackEvent } from '../analytics.js'

const router = useRouter()
const selectedCategory = ref('')
const selectedType = ref('')
const mode = ref('shuffle')
const selectedChapter = ref('')

const wrongCount = computed(() => getWrongItems().length)

const chapters = computed(() => {
  return chapterInfo[selectedCategory.value] || []
})

const canStart = computed(() => {
  if (!selectedCategory.value || !selectedType.value) return false
  if (mode.value === 'sequential') return !!selectedChapter.value
  return true
})

function selectCategory(catId) {
  trackEvent('select_category', { category: catId })
  selectedCategory.value = catId
  selectedType.value = ''
  selectedChapter.value = ''
  mode.value = 'shuffle'
}

function getNounCount(catId) {
  return nounExplanations[catId]?.length || 0
}

function getBlankCount(catId) {
  return fillBlanks[catId]?.length || 0
}

function startQuiz() {
  trackEvent('start_quiz', {
    category: selectedCategory.value,
    type: selectedType.value,
    mode: mode.value,
    chapter: selectedChapter.value || null
  })
  const query = {}
  if (mode.value === 'shuffle') query.shuffle = '1'
  if (mode.value === 'sequential' && selectedChapter.value) {
    query.chapter = selectedChapter.value
  }
  router.push({ path: `/quiz/${selectedCategory.value}/${selectedType.value}`, query })
}
</script>

<style scoped>
.shuffle-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  color: #5a4d42;
  cursor: pointer;
}

.shuffle-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #6b4c3b;
}

.mode-list {
  display: flex;
  gap: 12px;
}

.mode-btn {
  flex: 1;
  padding: 14px;
  border-radius: 12px;
  border: 2px solid #e8e2da;
  background: #fff;
  font-size: 15px;
  font-weight: 600;
  color: #5a4d42;
  cursor: pointer;
  transition: all 0.2s;
}

.mode-btn:active { transform: scale(0.97); }

.mode-btn.selected {
  border-color: #6b4c3b;
  background: #6b4c3b;
  color: #fff;
}

.chapter-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chapter-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  border: 2px solid #e8e2da;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s;
}

.chapter-item:active { transform: scale(0.98); }

.chapter-item.selected {
  border-color: #6b4c3b;
  background: #fdf8f4;
}

.chapter-idx {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e8e2da;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: #6b4c3b;
  flex-shrink: 0;
}

.chapter-item.selected .chapter-idx {
  background: #6b4c3b;
  color: #fff;
}

.chapter-name {
  flex: 1;
  font-size: 15px;
  font-weight: 600;
  color: #3a2f28;
}

.chapter-count {
  font-size: 13px;
  color: #a89b8e;
}
</style>
