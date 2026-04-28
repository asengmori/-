import pdfplumber
import re
import json

def extract_noun_explanations(pdf_path):
    items = []
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
                
                # Match numbered entries: "数字. 词条名"
                match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
                if match:
                    term_candidate = match.group(2).strip()
                    
                    # Skip TOC entries (they have dots like "词条.......23")
                    if '.....' in term_candidate or '..' in term_candidate:
                        continue
                    
                    # Skip very long terms (likely section headers)
                    if len(term_candidate) > 30:
                        continue
                    
                    # Save previous entry
                    if current_term and current_answer:
                        answer_text = ' '.join(current_answer).strip()
                        answer_text = answer_text.replace('祝顺利上岸！联系五柳指路：wuliustudy0704', '')
                        # Clean up answer - remove page numbers and TOC-like content
                        if len(answer_text) > 10:  # Only save if it has real content
                            items.append({
                                'term': current_term.strip(),
                                'answer': answer_text
                            })
                    
                    current_term = term_candidate
                    current_answer = []
                elif current_term:
                    current_answer.append(stripped)
            
            # Don't forget last entry on page
            if current_term and current_answer:
                answer_text = ' '.join(current_answer).strip()
                answer_text = answer_text.replace('祝顺利上岸！联系五柳指路：wuliustudy0704', '')
                if len(answer_text) > 10:
                    items.append({
                        'term': current_term.strip(),
                        'answer': answer_text
                    })
    
    return items

def convert_to_quiz_format(items, prefix):
    result = []
    for i, item in enumerate(items):
        result.append({
            'id': f'{prefix}{i+1}',
            'term': item['term'],
            'answer': item['answer']
        })
    return result

# Extract both files
ancient_path = r'C:\Users\luoyj04\AppData\Local\Temp\lobsterai\attachments\【最最终定稿】古代名词解释(1)-1777363718694-6k4qcr.pdf'
modern_path = r'C:\Users\luoyj04\AppData\Local\Temp\lobsterai\attachments\【最终定稿】现当代名词解释(1)-1777363710795-g78ud6.pdf'

print("Extracting ancient literature...")
ancient_items = extract_noun_explanations(ancient_path)
print(f"Ancient: {len(ancient_items)} items")

print("Extracting modern literature...")
modern_items = extract_noun_explanations(modern_path)
print(f"Modern: {len(modern_items)} items")

# Convert to quiz format
ancient_quiz = convert_to_quiz_format(ancient_items, 'a')
modern_quiz = convert_to_quiz_format(modern_items, 'm')

# Generate JS file
output_lines = [
    '// 自动生成的名词解释数据',
    f'// 古代文学: {len(ancient_quiz)} 条',
    f'// 现当代文学: {len(modern_quiz)} 条',
    f'// 生成时间: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")}',
    '',
    'export const nounExplanations = {',
    '  ancient: ' + json.dumps(ancient_quiz, ensure_ascii=False, indent=4) + ',',
    '  modern: ' + json.dumps(modern_quiz, ensure_ascii=False, indent=4),
    '}'
]

output_path = r'C:\Users\luoyj04\lobsterai\project\literature-quiz\src\data\noun_explanations.js'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"\nData generated: {output_path}")
print(f"Ancient: {len(ancient_quiz)} items")
print(f"Modern: {len(modern_quiz)} items")
print(f"Total: {len(ancient_quiz) + len(modern_quiz)} items")

# Show samples
print("\n=== Ancient sample ===")
for item in ancient_quiz[:3]:
    print(f"  {item['term']}: {item['answer'][:60]}...")

print("\n=== Modern sample ===")
for item in modern_quiz[:3]:
    print(f"  {item['term']}: {item['answer'][:60]}...")
