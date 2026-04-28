<template>
  <div>
    <div class="header">
      <button class="back-btn" @click="$router.back()">←</button>
      <div class="header-title">错题本</div>
      <div class="header-subtitle">{{ items.length }} 道错题</div>
    </div>

    <div v-if="items.length === 0" class="empty-state">
      <div class="empty-icon">🎉</div>
      <div class="empty-text">暂无错题，继续保持！</div>
    </div>

    <div v-else class="wrong-list">
      <div v-for="item in items" :key="item.id" class="wrong-item">
        <div class="wrong-term">
          {{ item.type === 'noun' ? item.term : '填空：' + item.question?.substring(0, 30) + '...' }}
        </div>
        <div class="wrong-category">
          {{ getCategoryName(item.category) }} · {{ item.type === 'noun' ? '名词解释' : '填空题' }}
        </div>
        <div class="wrong-actions">
          <button class="wrong-action-btn view" @click="viewDetail(item)">查看</button>
          <button class="wrong-action-btn remove" @click="remove(item.id)">已掌握</button>
        </div>
      </div>
    </div>

    <div class="bottom-spacer"></div>

    <div class="tab-bar">
      <div class="tab-item" @click="$router.push('/')">
        <div class="tab-icon">📚</div>
        <div class="tab-label">刷题</div>
      </div>
      <div class="tab-item active" @click="$router.push('/wrong')">
        <div class="tab-icon">📝</div>
        <div class="tab-label">错题本 <span v-if="items.length" style="color:#c0392b">({{ items.length }})</span></div>
      </div>
    </div>

    <!-- Detail modal -->
    <div v-if="showDetail" class="modal-overlay" @click="showDetail = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <span>{{ detailItem.type === 'noun' ? detailItem.term : '填空题' }}</span>
          <button class="modal-close" @click="showDetail = false">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="detailItem.type === 'noun'">
            <div class="answer-text">{{ detailItem.answer }}</div>
          </div>
          <div v-else>
            <div class="blank-question">{{ detailItem.question }}</div>
            <div style="color: #6b4c3b; font-weight: 600;">
              正确答案：{{ detailItem.answers?.join('、') }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { getWrongItems, removeWrongItem } from '../store.js'
import { categories } from '../data/questions.js'

const showDetail = ref(false)
const detailItem = ref({})

const items = computed(() => getWrongItems())

function getCategoryName(catId) {
  return categories.find(c => c.id === catId)?.name || catId
}

function viewDetail(item) {
  detailItem.value = item
  showDetail.value = true
}

function remove(id) {
  removeWrongItem(id)
  // Force re-render
  items.value.length // just accessing to trigger computed
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}

.modal-content {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 400px;
  max-height: 70vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e8e2da;
  font-size: 17px;
  font-weight: 600;
}

.modal-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #8a7a6d;
}

.modal-body {
  padding: 20px;
}
</style>
