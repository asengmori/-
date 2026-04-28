import pdfplumber
import re
import json

def extract_noun_explanations(pdf_path):
    """Extract noun explanations from PDF, returns list of {term, answer}"""
    items = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            # Find entries like "27. 学衡派\n1922年，围绕..."
            # Pattern: number. term\ncontent
            # Split by numbered entries
            lines = text.split('\n')
            current_term = None
            current_answer = []
            
            for line in lines:
                # Match pattern: "数字. 词条名"
                match = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
                if match:
                    # Save previous entry
                    if current_term and current_answer:
                        answer_text = ' '.join(current_answer).strip()
                        # Remove page headers/footers
                        answer_text = re.sub(r'祝顺利上岸！联系五柳指路：wuliustudy0704', '', answer_text)
                        items.append({
                            'term': current_term.strip(),
                            'answer': answer_text
                        })
                    current_term = match.group(2)
                    current_answer = []
                elif current_term:
                    current_answer.append(line.strip())
            
            # Don't forget last entry on page
            if current_term and current_answer:
                answer_text = ' '.join(current_answer).strip()
                answer_text = re.sub(r'祝顺利上岸！联系五柳指路：wuliustudy0704', '', answer_text)
                items.append({
                    'term': current_term.strip(),
                    'answer': answer_text
                })
    
    return items

# Extract both files
ancient_path = r'C:\Users\luoyj04\AppData\Local\Temp\lobsterai\attachments\【最最终定稿】古代名词解释(1)-1777363718694-6k4qcr.pdf'
modern_path = r'C:\Users\luoyj04\AppData\Local\Temp\lobsterai\attachments\【最终定稿】现当代名词解释(1)-1777363710795-g78ud6.pdf'

print("Extracting ancient literature...")
ancient_items = extract_noun_explanations(ancient_path)
print(f"Ancient: {len(ancient_items)} items")

print("Extracting modern literature...")
modern_items = extract_noun_explanations(modern_path)
print(f"Modern: {len(modern_items)} items")

# Show samples
print("\n=== 古代示例 ===")
for item in ancient_items[:3]:
    print(f"{item['term']}: {item['answer'][:100]}...")

print("\n=== 现当代示例 ===")
for item in modern_items[:3]:
    print(f"{item['term']}: {item['answer'][:100]}...")
