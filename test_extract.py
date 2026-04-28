import pdfplumber
import re
import sys

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
                match = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
                if match:
                    if current_term and current_answer:
                        answer_text = ' '.join(current_answer).strip()
                        answer_text = answer_text.replace('祝顺利上岸！联系五柳指路：wuliustudy0704', '')
                        items.append({'term': current_term.strip(), 'answer': answer_text})
                    current_term = match.group(2)
                    current_answer = []
                elif current_term:
                    current_answer.append(line.strip())
            
            if current_term and current_answer:
                answer_text = ' '.join(current_answer).strip()
                answer_text = answer_text.replace('祝顺利上岸！联系五柳指路：wuliustudy0704', '')
                items.append({'term': current_term.strip(), 'answer': answer_text})
    return items

try:
    modern_path = r'C:\Users\luoyj04\AppData\Local\Temp\lobsterai\attachments\【最终定稿】现当代名词解释(1)-1777363710795-g78ud6.pdf'
    items = extract_noun_explanations(modern_path)
    print(f'Success! Found {len(items)} items')
    for item in items[:3]:
        print(f"{item['term']}: {item['answer'][:80]}...")
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
