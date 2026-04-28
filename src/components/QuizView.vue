<template>
  <div>
    <div class="header">
      <button class="back-btn" @click="$router.back()">←</button>
      <div class="header-title">{{ title }}</div>
      <div class="header-subtitle">{{ currentIndex + 1 }} / {{ questions.length }}</div>
    </div>

    <!-- 名词解释 - 卡片模式 -->
    <div v-if="type === 'noun'" class="quiz-container">
      <div class="progress-bar">
        <span>{{ Math.round(((currentIndex + 1) / questions.length) * 100) }}%</span>
        <div class="progress-track">
          <div class="progress-fill" :style="{ width: ((currentIndex + 1) / questions.length) * 100 + '%' }"></div>
        </div>
      </div>

      <div class="question-card">
        <div class="question-label">请解释以下名词</div>
        <div class="question-term">{{ currentQuestion.term }}</div>

        <button v-if="!showAnswer" class="reveal-btn" @click="revealAnswer">
          点击查看答案
        </button>

        <div v-else class="answer-section">
          <div class="answer-label">📖 参考答案</div>
          <div class="answer-text">{{ currentQuestion.answer }}</div>
        </div>
      </div>

      <div class="nav-buttons">
        <button class="nav-btn prev" @click="prev" :disabled="currentIndex === 0">上一题</button>
        <button
          class="nav-btn wrong-btn"
          :class="{ 'is-wrong': isWrong }"
          @click="toggleWrong"
        >
          {{ isWrong ? '✓ 已标记' : '✗ 标为错题' }}
        </button>
        <button class="nav-btn next" @click="next" :disabled="currentIndex === questions.length - 1">下一题</button>
      </div>
    </div>

    <!-- 填空题 -->
    <div v-if="type === 'blank'" class="quiz-container">
      <div class="progress-bar">
        <span>{{ Math.round(((currentIndex + 1) / questions.length) * 100) }}%</span>
        <div class="progress-track">
          <div class="progress-fill" :style="{ width: ((currentIndex + 1) / questions.length) * 100 + '%' }"></div>
        </div>
      </div>

      <div class="question-card">
        <div class="blank-question">{{ currentQuestion.question }}</div>

        <div class="blank-input-area" v-if="!checked">
          <div
            v-for="(answer, idx) in currentQuestion.answers"
            :key="idx"
            class="blank-input-group"
          >
            <span class="blank-num">空{{ idx + 1 }}</span>
            <input
              class="blank-input"
              v-model="userAnswers[idx]"
              :placeholder="'请输入第' + (idx + 1) + '个空'"
              @keyup.enter="checkAnswer"
            />
          </div>
          <button class="check-btn" @click="checkAnswer">提交答案</button>
        </div>

        <div v-else>
          <div
            v-for="(answer, idx) in currentQuestion.answers"
            :key="idx"
            class="blank-input-group"
          >
            <span class="blank-num">空{{ idx + 1 }}</span>
            <input
              class="blank-input"
              :class="getResultClass(idx)"
              :value="userAnswers[idx]"
              readonly
            />
          </div>

          <div class="result-text" :class="allCorrect ? 'correct' : 'incorrect'">
            <div v-if="allCorrect">✅ 全部正确！</div>
            <div v-else>
              ❌ 有错误，正确答案：
              <strong>{{ currentQuestion.answers.join('、') }}</strong>
            </div>
          </div>

          <button class="check-btn" style="margin-top: 12px; background: #e8e2da; color: #5a4d42;" @click="resetCurrent">
            重新作答
          </button>
        </div>
      </div>

      <div class="nav-buttons">
        <button class="nav-btn prev" @click="prev" :disabled="currentIndex === 0">上一题</button>
        <button
          v-if="checked && !allCorrect"
          class="nav-btn wrong-btn"
          :class="{ 'is-wrong': isWrong }"
          @click="toggleWrong"
        >
          {{ isWrong ? '✓ 已标记' : '✗ 标为错题' }}
        </button>
        <button class="nav-btn next" @click="next" :disabled="currentIndex === questions.length - 1">下一题</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { nounExplanations, fillBlanks, categories, chapterInfo } from '../data/questions.js'
import { getWrongItems, saveWrongItem, removeWrongItem } from '../store.js'
import { earnSilver, loadTaoState, saveTaoState } from '../tao.js'

const props = defineProps({
  category: String,
  type: String
})

const route = useRoute()
const currentIndex = ref(0)
const showAnswer = ref(false)
const userAnswers = ref([])
const checked = ref(false)

function shuffleArray(arr) {
  const shuffled = [...arr]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

const isShuffle = computed(() => route.query.shuffle === '1')
const selectedChapter = computed(() => route.query.chapter || '')

const questions = computed(() => {
  let base
  if (props.type === 'noun') {
    base = nounExplanations[props.category] || []
  } else {
    base = fillBlanks[props.category] || []
  }
  // Filter by chapter if selected
  if (selectedChapter.value) {
    base = base.filter(item => item.chapter === selectedChapter.value)
  }
  return isShuffle.value ? shuffleArray(base) : base
})

const currentQuestion = computed(() => questions.value[currentIndex.value])

const title = computed(() => {
  const cat = categories.find(c => c.id === props.category)
  let modeTag = ''
  if (isShuffle.value) modeTag = ' (乱序)'
  else if (selectedChapter.value) modeTag = ` (${selectedChapter.value})`
  else modeTag = ' (正序)'
  return (cat?.name || '') + ' · ' + (props.type === 'noun' ? '名词解释' : '填空题') + modeTag
})

const isWrong = computed(() => {
  return getWrongItems().some(i => i.id === currentQuestion.value?.id)
})

const allCorrect = computed(() => {
  if (!checked.value) return false
  return currentQuestion.value.answers.every((a, i) =>
    a.trim() === (userAnswers.value[i] || '').trim()
  )
})

function getResultClass(idx) {
  if (!checked.value) return ''
  return currentQuestion.value.answers[idx].trim() === (userAnswers.value[idx] || '').trim()
    ? 'correct' : 'incorrect'
}

function checkAnswer() {
  checked.value = true
  if (allCorrect.value) {
    // 答对了，从错题本移除 + 赚银两
    removeWrongItem(currentQuestion.value.id)
    const newState = earnSilver(2)
    window.dispatchEvent(new CustomEvent('tao-earn', { detail: newState }))
  } else {
    // 答错了，加入错题本 + 陶渊明失望
    saveWrongItem({
      id: currentQuestion.value.id,
      type: 'blank',
      category: props.category,
      question: currentQuestion.value.question,
      answers: currentQuestion.value.answers
    })
    const state = loadTaoState()
    state.totalWrong += 1
    saveTaoState(state)
    window.dispatchEvent(new CustomEvent('tao-wrong'))
  }
}

function resetCurrent() {
  userAnswers.value = new Array(currentQuestion.value.answers.length).fill('')
  checked.value = false
}

function toggleWrong() {
  const q = currentQuestion.value
  if (isWrong.value) {
    removeWrongItem(q.id)
  } else {
    saveWrongItem({
      id: q.id,
      type: props.type,
      category: props.category,
      term: q.term,
      answer: q.answer,
      question: q.question,
      answers: q.answers
    })
  }
}

function next() {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    resetState()
  }
}

function prev() {
  if (currentIndex.value > 0) {
    currentIndex.value--
    resetState()
  }
}

function resetState() {
  showAnswer.value = false
  checked.value = false
  if (currentQuestion.value?.answers) {
    userAnswers.value = new Array(currentQuestion.value.answers.length).fill('')
  }
}

// 名词解释 - 查看答案赚银两
function revealAnswer() {
  showAnswer.value = true
  const newState = earnSilver(1)
  window.dispatchEvent(new CustomEvent('tao-earn', { detail: newState }))
}

watch(() => [props.category, props.type], () => {
  currentIndex.value = 0
  resetState()
})

// Init
if (currentQuestion.value?.answers) {
  userAnswers.value = new Array(currentQuestion.value.answers.length).fill('')
}
</script>
