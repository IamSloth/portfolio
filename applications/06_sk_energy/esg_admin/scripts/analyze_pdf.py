
import sys
import os
import fitz  # PyMuPDF

def analyze_pdf_layout(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    print(f"Analyzing PDF Layout: {pdf_path}")
    
    try:
        doc = fitz.open(pdf_path)
        print(f"Total Pages: {len(doc)}")
        
        for i, page in enumerate(doc):
            text = page.get_text()
            lines = text.split('\n')
            non_empty_lines = [l for l in lines if l.strip()]
            char_count = len(text)
            
            print(f"\n[Page {i+1}]")
            print(f"  Character Count: {char_count}")
            print(f"  Line Count: {len(non_empty_lines)}")
            
            if char_count < 200:
                print("  -> WARNING: Low content density (Potential bad break or blank page)")
                print(f"  Content: {text.strip()[:100]}...")
            elif i == len(doc) - 1 and char_count < 500:
                 print("  -> INFO: Last page has low content. Check if it's just signature/date.")
                 print(f"  Content: {text.strip()[:100]}...")

    except Exception as e:
        print(f"Error analyzing PDF: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_pdf.py <path_to_pdf>")
        sys.exit(1)
    analyze_pdf_layout(sys.argv[1])
