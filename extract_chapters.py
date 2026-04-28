import pdfplumber
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

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
                
                # Detect chapter headers
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
                                'chapter_num': chapter_num
                            })
                    
                    chapter_num += 1
                    current_chapter = chapter_match.group(2).strip()
                    current_term = None
                    current_answer = []
                    continue
                
                match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
                if match:
                    term_candidate = match.group(2).strip()
                    
                    if '.....' in term_candidate or '..' in term_candidate:
                        continue
                    if len(term_candidate) > 30:
                        continue
                    
                    if current_term and current_answer:
                        answer_text = ' '.join(current_answer).strip()
                        answer_text = answer_text.replace('祝顺利上岸！联系五柳指路：wuliustudy0704', '')
                        if len(answer_text) > 10:
                            items.append({
                                'term': current_term.strip(),
                                'answer': answer_text,
                                'chapter': current_chapter,
                                'chapter_num': chapter_num
                            })
                    
                    current_term = term_candidate
                    current_answer = []
                elif current_term:
                    current_answer.append(stripped)
            
            if current_term and current_answer:
                answer_text = ' '.join(current_answer).strip()
                answer_text = answer_text.replace('祝顺利上岸！联系五柳指路：wuliustudy0704', '')
                if len(answer_text) > 10:
                    items.append({
                        'term': current_term.strip(),
                        'answer': answer_text,
                        'chapter': current_chapter,
                        'chapter_num': chapter_num
                    })
    
    return items

ancient_path = r'C:\Users\luoyj04\AppData\Local\Temp\lobsterai\attachments\【最最终定稿】古代名词解释(1)-1777363718694-6k4qcr.pdf'
modern_path = r'C:\Users\luoyj04\AppData\Local\Temp\lobsterai\attachments\【最终定稿】现当代名词解释(1)-1777363710795-g78ud6.pdf'

out = open('extract_out.txt', 'w', encoding='utf-8')

out.write('Extracting ancient...\n')
ancient_items = extract_with_chapters(ancient_path)
out.write(f'  {len(ancient_items)} items\n')

chapters_seen = {}
for item in ancient_items:
    key = item['chapter']
    if key not in chapters_seen:
        chapters_seen[key] = {'count': 0, 'num': item['chapter_num']}
    chapters_seen[key]['count'] += 1

out.write('\nAncient chapters:\n')
for ch, info in sorted(chapters_seen.items(), key=lambda x: x[1]['num']):
    out.write(f'  [{info["num"]}] {ch}: {info["count"]} items\n')

out.write('\nExtracting modern...\n')
modern_items = extract_with_chapters(modern_path)
out.write(f'  {len(modern_items)} items\n')

chapters_seen = {}
for item in modern_items:
    key = item['chapter']
    if key not in chapters_seen:
        chapters_seen[key] = {'count': 0, 'num': item['chapter_num']}
    chapters_seen[key]['count'] += 1

out.write('\nModern chapters:\n')
for ch, info in sorted(chapters_seen.items(), key=lambda x: x[1]['num']):
    out.write(f'  [{info["num"]}] {ch}: {info["count"]} items\n')

out.write('\nDone!\n')
out.close()

# Also save JSON
with open('ancient_items.json', 'w', encoding='utf-8') as f:
    json.dump(ancient_items, f, ensure_ascii=False, indent=2)
with open('modern_items.json', 'w', encoding='utf-8') as f:
    json.dump(modern_items, f, ensure_ascii=False, indent=2)

print('Done! Check extract_out.txt and JSON files')
