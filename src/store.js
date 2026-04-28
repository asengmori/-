const STORAGE_KEY = 'lit_quiz_wrong'

export function getWrongItems() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  } catch {
    return []
  }
}

export function saveWrongItem(item) {
  const items = getWrongItems()
  if (!items.find(i => i.id === item.id)) {
    items.push({ ...item, addedAt: Date.now() })
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
  }
}

export function removeWrongItem(id) {
  let items = getWrongItems()
  items = items.filter(i => i.id !== id)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
}

export function clearWrongItems() {
  localStorage.removeItem(STORAGE_KEY)
}
