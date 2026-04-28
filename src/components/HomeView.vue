<template>
  <div>
    <div class="header">
      <div class="header-title">文学考研刷题</div>
      <div class="header-subtitle">每天进步一点点</div>
    </div>

    <div class="section">
      <div class="section-title">选择方向</div>
      <div class="category-grid">
        <div
          v-for="cat in categories"
          :key="cat.id"
          class="category-card"
          :class="{ selected: selectedCategory === cat.id }"
          @click="selectedCategory = cat.id"
        >
          <div class="category-icon">{{ cat.icon }}</div>
          <div class="category-name">{{ cat.name }}</div>
          <div class="category-count">
            名词 {{ getNounCount(cat.id) }} · 填空 {{ getBlankCount(cat.id) }}
          </div>
        </div>
      </div>
    </div>

    <div class="section">
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

    <div class="section" v-if="selectedType === 'noun'">
      <label class="shuffle-label">
        <input type="checkbox" v-model="shuffleMode" />
        乱序模式
      </label>
    </div>

    <div class="section">
      <button
        class="start-btn"
        :disabled="!selectedCategory || !selectedType"
        @click="startQuiz"
      >
        开始刷题
      </button>
    </div>

    <div class="bottom-spacer"></div>

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
import { categories, questionTypes, nounExplanations, fillBlanks } from '../data/questions.js'
import { getWrongItems } from '../store.js'

const router = useRouter()
const selectedCategory = ref('')
const selectedType = ref('')
const shuffleMode = ref(false)

const wrongCount = computed(() => getWrongItems().length)

function getNounCount(catId) {
  return nounExplanations[catId]?.length || 0
}

function getBlankCount(catId) {
  return fillBlanks[catId]?.length || 0
}

function startQuiz() {
  const query = shuffleMode.value ? { shuffle: '1' } : {}
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
</style>
