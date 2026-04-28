<template>
  <div class="app">
    <router-view />
    <TaoYuanming />
  </div>
</template>

<script setup>
import TaoYuanming from './components/TaoYuanming.vue'
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  background: #f5f3ef;
  color: #2c2c2c;
  -webkit-font-smoothing: antialiased;
  -webkit-tap-highlight-color: transparent;
}

.app {
  min-height: 100vh;
  max-width: 480px;
  margin: 0 auto;
  background: #faf9f7;
  position: relative;
}

/* Header */
.header {
  background: linear-gradient(135deg, #4a3728 0%, #6b4c3b 100%);
  color: #fff;
  padding: 24px 20px 20px 56px;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.header::after {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 200px;
  height: 200px;
  background: rgba(255,255,255,0.05);
  border-radius: 50%;
}

.header-subtitle {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 4px;
}

.back-btn {
  position: absolute;
  top: 24px;
  left: 16px;
  background: none;
  border: none;
  color: #fff;
  font-size: 24px;
  cursor: pointer;
  padding: 4px 8px;
  opacity: 0.8;
  z-index: 2;
}

.back-btn:active { opacity: 1; }

.header-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 1px;
  text-align: center;
}

/* Category Cards */
.section {
  padding: 20px;
}

.section-title {
  font-size: 14px;
  color: #8a7a6d;
  font-weight: 600;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.category-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.category-card {
  background: #fff;
  border-radius: 16px;
  padding: 24px 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  border: 2px solid transparent;
}

.category-card:active {
  transform: scale(0.97);
}

.category-card.selected {
  border-color: #6b4c3b;
  background: #fdf8f4;
}

.category-icon {
  font-size: 36px;
  margin-bottom: 8px;
}

.category-name {
  font-size: 16px;
  font-weight: 600;
  color: #3a2f28;
}

.category-count {
  font-size: 12px;
  color: #a89b8e;
  margin-top: 4px;
}

/* Type Selector */
.type-list {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.type-btn {
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

.type-btn:active { transform: scale(0.97); }

.type-btn.selected {
  border-color: #6b4c3b;
  background: #6b4c3b;
  color: #fff;
}

/* Start Button */
.start-btn {
  width: 100%;
  padding: 16px;
  border-radius: 14px;
  border: none;
  background: linear-gradient(135deg, #4a3728 0%, #6b4c3b 100%);
  color: #fff;
  font-size: 17px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 24px;
  letter-spacing: 2px;
  transition: all 0.2s;
}

.start-btn:active {
  transform: scale(0.98);
  opacity: 0.9;
}

.start-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Quiz Card */
.quiz-container {
  padding: 20px;
  min-height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}

.progress-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  font-size: 13px;
  color: #8a7a6d;
}

.progress-track {
  flex: 1;
  height: 4px;
  background: #e8e2da;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #6b4c3b;
  border-radius: 2px;
  transition: width 0.3s;
}

.question-card {
  background: #fff;
  border-radius: 16px;
  padding: 28px 20px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.06);
  flex: 1;
}

.question-label {
  font-size: 13px;
  color: #a89b8e;
  margin-bottom: 12px;
  font-weight: 500;
}

.question-term {
  font-size: 26px;
  font-weight: 700;
  color: #2c2520;
  line-height: 1.4;
  margin-bottom: 20px;
}

.reveal-btn {
  width: 100%;
  padding: 14px;
  border-radius: 12px;
  border: 2px dashed #d4c9bb;
  background: transparent;
  color: #8a7a6d;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.reveal-btn:active {
  border-color: #6b4c3b;
  color: #6b4c3b;
}

.answer-section {
  margin-top: 20px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.answer-label {
  font-size: 13px;
  color: #6b4c3b;
  font-weight: 600;
  margin-bottom: 10px;
}

.answer-text {
  font-size: 15px;
  line-height: 1.8;
  color: #4a4238;
  text-align: justify;
  background: #fdf8f4;
  padding: 16px;
  border-radius: 10px;
  border-left: 3px solid #6b4c3b;
}

.nav-buttons {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.nav-btn {
  flex: 1;
  padding: 14px;
  border-radius: 12px;
  border: none;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-btn:active { transform: scale(0.97); }

.nav-btn.prev {
  background: #e8e2da;
  color: #5a4d42;
}

.nav-btn.next {
  background: #6b4c3b;
  color: #fff;
}

.nav-btn.wrong-btn {
  background: #fff;
  border: 2px solid #e8e2da;
  color: #8a7a6d;
}

.nav-btn.wrong-btn.is-wrong {
  border-color: #c0392b;
  color: #c0392b;
}

/* Fill in blanks */
.blank-question {
  font-size: 18px;
  line-height: 2;
  color: #2c2520;
  margin-bottom: 24px;
}

.blank-input-area {
  margin-top: 16px;
}

.blank-input-group {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.blank-num {
  font-size: 13px;
  color: #a89b8e;
  min-width: 28px;
}

.blank-input {
  flex: 1;
  padding: 10px 14px;
  border: 2px solid #e8e2da;
  border-radius: 10px;
  font-size: 15px;
  outline: none;
  transition: border-color 0.2s;
}

.blank-input:focus { border-color: #6b4c3b; }

.blank-input.correct {
  border-color: #27ae60;
  background: #f0faf3;
}

.blank-input.incorrect {
  border-color: #c0392b;
  background: #fdf2f0;
}

.check-btn {
  width: 100%;
  padding: 14px;
  border-radius: 12px;
  border: none;
  background: #6b4c3b;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
}

.result-text {
  margin-top: 16px;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.8;
}

.result-text.correct {
  background: #f0faf3;
  color: #1e7e46;
}

.result-text.incorrect {
  background: #fdf2f0;
  color: #c0392b;
}

/* Wrong list */
.wrong-list {
  padding: 16px 20px;
}

.wrong-item {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 10px;
  box-shadow: 0 1px 8px rgba(0,0,0,0.04);
}

.wrong-term {
  font-size: 16px;
  font-weight: 600;
  color: #2c2520;
  margin-bottom: 6px;
}

.wrong-category {
  font-size: 12px;
  color: #a89b8e;
}

.wrong-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.wrong-action-btn {
  padding: 6px 12px;
  border-radius: 8px;
  border: none;
  font-size: 13px;
  cursor: pointer;
}

.wrong-action-btn.view {
  background: #fdf8f4;
  color: #6b4c3b;
}

.wrong-action-btn.remove {
  background: #fdf2f0;
  color: #c0392b;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #a89b8e;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-text {
  font-size: 15px;
}

/* Tab bar */
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 480px;
  background: #fff;
  display: flex;
  border-top: 1px solid #e8e2da;
  z-index: 10;
}

.tab-item {
  flex: 1;
  padding: 10px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-item.active {
  color: #6b4c3b;
}

.tab-icon {
  font-size: 22px;
}

.tab-label {
  font-size: 11px;
  margin-top: 2px;
}

.bottom-spacer {
  height: 60px;
}
</style>
