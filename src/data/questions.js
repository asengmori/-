export const categories = [
  { id: 'ancient', name: '古代文学', icon: '📜' },
  { id: 'modern', name: '现当代文学', icon: '📖' }
]

export const questionTypes = [
  { id: 'noun', name: '名词解释' },
  { id: 'blank', name: '填空题' }
]

// 名词解释数据 - 从 PDF 自动生成 (640条)
export { nounExplanations } from './noun_explanations.js'

// 填空题数据 - 手动维护
export const fillBlanks = {
  ancient: [
    {
      id: 'ab1',
      question: '《诗经》分为____、____、____三个部分。',
      answers: ['风', '雅', '颂']
    },
    {
      id: 'ab2',
      question: '楚辞的代表作家是____，其代表作有《离骚》《____》《____》等。',
      answers: ['屈原', '九歌', '天问']
    },
    {
      id: 'ab3',
      question: '唐代"初唐四杰"是指____、____、____、____。',
      answers: ['王勃', '杨炯', '卢照邻', '骆宾王']
    },
    {
      id: 'ab4',
      question: '白居易与____并称"元白"，共同倡导了____运动。',
      answers: ['元稹', '新乐府']
    },
    {
      id: 'ab5',
      question: '《文心雕龙》的作者是南朝____，这是中国第一部系统的____著作。',
      answers: ['刘勰', '文学理论']
    }
  ],
  modern: [
    {
      id: 'mb1',
      question: '鲁迅的第一篇白话小说是《____》，发表于____年，载于《____》杂志。',
      answers: ['狂人日记', '1918', '新青年']
    },
    {
      id: 'mb2',
      question: '茅盾的《____》是中国现代文学史上第一部现实主义长篇小说，其"农村三部曲"包括《____》《____》《____》。',
      answers: ['子夜', '春蚕', '秋收', '残冬']
    },
    {
      id: 'mb3',
      question: '沈从文的代表作是《____》，以____为背景，描写了湘西的风土人情。',
      answers: ['边城', '湘西']
    },
    {
      id: 'mb4',
      question: '张爱玲的代表作有《____》《____》《____》等。',
      answers: ['金锁记', '倾城之恋', '红玫瑰与白玫瑰']
    },
    {
      id: 'mb5',
      question: '钱钟书的长篇小说《____》被誉为"新____"，其散文集《____》也是经典之作。',
      answers: ['围城', '儒林外史', '写在人生边上']
    }
  ]
}
