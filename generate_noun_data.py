import pdfplumber
import re
import json

def extract_with_chapters(pdf_path):
    items = []
    current_chapter = ''
    chapter_num = 0
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split('\n')
            current_term = None
            current_answer = []
            
            for line in lines:
                stripped = line.strip()
                
                # Detect chapter headers: "第X编：XXXX"
                chapter_match = re.match(r'^第([一二三四五六七八九十]+)编[:：]\s*(.+)$', stripped)
                if chapter_match:
                    if current_term and current_answer:
                        answer_text = ' '.join(current_answer).strip()
                        answer_text = answer_text.replace('祝顺利上岸！联系五柳指路：wuliustudy0704', '')
                        if len(answer_text) > 10:
                            items.append({
                                'term': current_term.strip(),
                                'answer': answer_text,
                                'chapter': current_chapter,
                            })
                    
                    chapter_num += 1
                    current_chapter = chapter_match.group(2).strip()
                    current_term = None
                    current_answer = []
                    continue
                
                # Match numbered entries
                match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
                if match:
                    term_candidate = match.group(2).strip()
                    
                    # Skip TOC entries
                    if '.....' in term_candidate or '..' in term_candidate:
                        continue
                    if len(term_candidate) > 30:
                        continue
                    
                    # Save previous entry
                    if current_term and current_answer:
                        answer_text = ' '.join(current_answer).strip()
                        answer_text = answer_text.replace('祝顺利上岸！联系五柳指路：wuliustudy0704', '')
                        if len(answer_text) > 10:
                            items.append({
                                'term': current_term.strip(),
                                'answer': answer_text,
                                'chapter': current_chapter,
                            })
                    
                    current_term = term_candidate
                    current_answer = []
                elif current_term:
                    current_answer.append(stripped)
            
            # Last entry on page
            if current_term and current_answer:
                answer_text = ' '.join(current_answer).strip()
                answer_text = answer_text.replace('祝顺利上岸！联系五柳指路：wuliustudy0704', '')
                if len(answer_text) > 10:
                    items.append({
                        'term': current_term.strip(),
                        'answer': answer_text,
                        'chapter': current_chapter,
                    })
    
    return items, chapter_num

# Extract
ancient_path = r'C:\Users\luoyj04\AppData\Local\Temp\lobsterai\attachments\【最最终定稿】古代名词解释(1)-1777363718694-6k4qcr.pdf'
modern_path = r'C:\Users\luoyj04\AppData\Local\Temp\lobsterai\attachments\【最终定稿】现当代名词解释(1)-1777363710795-g78ud6.pdf'

ancient_items, _ = extract_with_chapters(ancient_path)
modern_items, _ = extract_with_chapters(modern_path)

# Fix modern: first batch has no chapter (chapter_num was 0), assign it as "现代文学"
for item in modern_items:
    if not item['chapter']:
        item['chapter'] = '现代文学'

# Re-index chapters starting from 1
def reindex_chapters(items, prefix):
    chapter_map = {}
    idx = 1
    for item in items:
        ch = item['chapter']
        if ch not in chapter_map:
            chapter_map[ch] = idx
            idx += 1
        item['chapter'] = ch
        item['chapter_idx'] = chapter_map[ch]
    return items, chapter_map

ancient_items, ancient_chapters = reindex_chapters(ancient_items, 'a')
modern_items, modern_chapters = reindex_chapters(modern_items, 'm')

# Build chapter info
ancient_chapter_info = []
for ch, idx in sorted(ancient_chapters.items(), key=lambda x: x[1]):
    count = sum(1 for i in ancient_items if i['chapter'] == ch)
    ancient_chapter_info.append({'id': f'ancient_{idx}', 'name': ch, 'count': count, 'idx': idx})

modern_chapter_info = []
for ch, idx in sorted(modern_chapters.items(), key=lambda x: x[1]):
    count = sum(1 for i in modern_items if i['chapter'] == ch)
    modern_chapter_info.append({'id': f'modern_{idx}', 'name': ch, 'count': count, 'idx': idx})

# Add IDs
for i, item in enumerate(ancient_items):
    item['id'] = f'a{i+1}'
for i, item in enumerate(modern_items):
    item['id'] = f'm{i+1}'

# Generate JS
import datetime
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

js_lines = [
    '// 名词解释数据 - 自动生成 (含章节信息)',
    f'// 生成时间: {now}',
    '',
    'export const nounExplanations = {',
    '  ancient: ' + json.dumps(ancient_items, ensure_ascii=False, indent=4) + ',',
    '  modern: ' + json.dumps(modern_items, ensure_ascii=False, indent=4),
    '}',
    '',
    'export const chapterInfo = {',
    '  ancient: ' + json.dumps(ancient_chapter_info, ensure_ascii=False, indent=4) + ',',
    '  modern: ' + json.dumps(modern_chapter_info, ensure_ascii=False, indent=4),
    '}',
]

output_path = r'C:\Users\luoyj04\lobsterai\project\literature-quiz\src\data\noun_explanations.js'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(js_lines))

print(f'Done! {output_path}')
print(f'Ancient: {len(ancient_items)} items, {len(ancient_chapter_info)} chapters')
print(f'Modern: {len(modern_items)} items, {len(modern_chapter_info)} chapters')

for ci in ancient_chapter_info:
    print(f'  Ancient ch{ci["idx"]}: {ci["name"]} ({ci["count"]} items)')
for ci in modern_chapter_info:
    print(f'  Modern ch{ci["idx"]}: {ci["name"]} ({ci["count"]} items)')
