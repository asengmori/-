// 陪学助手 - 陶渊明
const STORAGE_KEY = 'tao_state'

const defaultState = () => ({
  silver: 0,
  wineLevel: 0,        // 0 sober, 1 tipsy, 2 drunk, 3 very drunk
  totalCorrect: 0,     // 答对总数
  totalWrong: 0,
  lastInteraction: '',  // 最后一次互动
  unlockedEvents: []   // 已触发的事件
})

export function loadTaoState() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved ? { ...defaultState(), ...JSON.parse(saved) } : defaultState()
  } catch {
    return defaultState()
  }
}

export function saveTaoState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
}

export function earnSilver(amount) {
  const state = loadTaoState()
  state.silver += amount
  state.totalCorrect += 1
  saveTaoState(state)
  return state
}

export function spendWine() {
  const state = loadTaoState()
  const wineCost = [5, 10, 20] // 每瓶酒价格
  const level = state.wineLevel
  const cost = wineCost[level] || 50

  if (state.silver >= cost) {
    state.silver -= cost
    state.wineLevel = Math.min(level + 1, 3)
    saveTaoState(state)
    return { success: true, cost, newState: state }
  }
  return { success: false, cost }
}

export function getWineCost(level) {
  return [5, 10, 20, 50][level] || 50
}

export function getRandomInteraction(level) {
  const interactions = {
    1: [ // 微醺
      { text: '采菊东篱下，悠然见南山……', type: 'poem' },
      { text: '这酒甚好，比彭泽县的浊酒还香。', type: 'talk' },
      { text: '先生今日读书如何？', type: 'ask' },
      { text: '悟已往之不谏，知来者之可追……', type: 'poem' },
      { text: '人生得意须尽欢……不对，那是李白的词。', type: 'funny' },
    ],
    2: [ // 醉
      { text: '（摇头晃脑）归去来兮！田园将芜胡不归！', type: 'poem' },
      { text: '吾不能为五斗米折腰！这题……我也不会。', type: 'funny' },
      { text: '（开始乱弹琴）叮叮咚咚……好听好听！', type: 'qin' },
      { text: '你看这无弦琴，虽然没有弦，但心中有声。', type: 'talk' },
      { text: '（站起来转圈）我醉欲眠卿且去！', type: 'funny' },
    ],
    3: [ // 大醉
      { text: '（抱着无弦琴在院子里跑）哈哈哈！此中有真意，欲辨已忘言！', type: 'qin' },
      { text: '（醉倒在菊花丛中）呼噜呼噜……💤', type: 'sleep' },
      { text: '（突然坐起来）对了！桃花源里可有考研人？', type: 'funny' },
      { text: '（手舞足蹈）五柳先生今天高兴，送你一个彩蛋！', type: 'reward' },
      { text: '（迷迷糊糊）少无适俗韵……性本爱丘山……你背下一句？', type: 'ask' },
    ]
  }

  const list = interactions[level] || interactions[1]
  return list[Math.floor(Math.random() * list.length)]
}
