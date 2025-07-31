from .utils import extract_invoice_number, extract_invoice_date, extract_line_items

def extract_fields_from_text(text):
    return {
        "invoice_number": extract_invoice_number(text),
        "invoice_date": extract_invoice_date(text),
        "line_items": extract_line_items(text)
    }
