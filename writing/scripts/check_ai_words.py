"""按 writing/AI味规则.md 的“禁用词”一节扫描文章，列出命中位置。

用法：
    python writing/scripts/check_ai_words.py content/handbook/basics/xxx.md

只扫描正文，跳过 front matter、代码块和 HTML/SVG 标签内部。
禁用词后面括号里的说明（如“标题除外”）只作提示，不参与匹配。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "writing" / "AI味规则.md"


def load_words() -> list[str]:
    text = RULES.read_text(encoding="utf-8")
    m = re.search(r"^## 一、禁用词\s*$(.*?)^## ", text, re.S | re.M)
    if not m:
        sys.exit("AI味规则.md 里找不到“## 一、禁用词”一节")
    words = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        line = re.sub(r"[（(].*?[）)]", "", line[2:])
        for w in re.split(r"[、，,]", line):
            w = w.strip().rstrip("？?")
            if w:
                words.append(w)
    return words


def body_lines(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
    in_code = False
    for n in range(i, len(lines)):
        line = lines[n]
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # 去掉标签本身，保留标签之间的文字（SVG <text> 里的中文也要检查）
        yield n + 1, re.sub(r"<[^>]+>", " ", line)


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    words = load_words()
    hits = 0
    for arg in sys.argv[1:]:
        path = Path(arg)
        for lineno, line in body_lines(path):
            for w in words:
                if w in line:
                    hits += 1
                    print(f"{path}:{lineno}: 「{w}」 {line.strip()[:60]}")
    print(f"共 {hits} 处命中（词表 {len(words)} 个）")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
