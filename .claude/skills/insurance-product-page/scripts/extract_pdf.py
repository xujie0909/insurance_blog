"""
extract_pdf.py — 保险条款 PDF 文字提取工具
用法: python extract_pdf.py <input.pdf> <output.txt>
依赖: pdfplumber（pip install pdfplumber）
"""
import sys
import os

def extract(pdf_path: str, out_path: str) -> None:
    try:
        import pdfplumber
    except ImportError:
        print("正在安装 pdfplumber...", flush=True)
        os.system(f'"{sys.executable}" -m pip install pdfplumber -q')
        import pdfplumber

    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        print(f"总页数: {total}", flush=True)
        with open(out_path, "w", encoding="utf-8") as f:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    f.write(f"--- 第{i+1}页 ---\n{text}\n\n")
                if (i + 1) % 10 == 0 or i + 1 == total:
                    print(f"已处理 {i+1}/{total} 页...", flush=True)
    print(f"完成！输出: {out_path}", flush=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python extract_pdf.py <input.pdf> <output.txt>")
        sys.exit(1)
    extract(sys.argv[1], sys.argv[2])
