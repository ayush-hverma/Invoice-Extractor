import re

def extract_invoice_number(text):
    match = re.search(r"(Invoice\s*Number|Inv\s*#)[:\s]*([A-Z0-9\-]+)", text, re.IGNORECASE)
    return match.group(2) if match else None

def extract_invoice_date(text):
    match = re.search(r"(Invoice\s*Date|Date)[:\s]*([0-9./-]+)", text, re.IGNORECASE)
    return match.group(2) if match else None

def extract_line_items(text):
    lines = text.split('\n')
    items = []
    for line in lines:
        if re.search(r'\d+\s+[a-zA-Z].*\d+\.\d+', line):
            items.append(line.strip())
    return items
