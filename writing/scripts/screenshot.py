"""视觉审阅用截图脚本。

对指定页面分别截取 明/暗 × 手机(375)/电脑(1280) 四张整页截图，
并检查横向溢出和图示里过小的文字，结果写入 report.json。

用法（先在另一个终端运行 hugo server）：
    python writing/scripts/screenshot.py handbook/basics/is-insurance-a-scam/ [更多路径...]
    python writing/scripts/screenshot.py --base http://localhost:1313 pages/tools/xxx/

路径不要带开头的斜杠：Git Bash 会把 /handbook/ 改写成 Windows 路径。

输出目录：writing/screenshots/<页面路径>/
"""

import argparse
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "writing" / "screenshots"

VIEWPORTS = {"mobile": (375, 812), "desktop": (1280, 900)}
THEMES = ("light", "dark")

CHECK_JS = """
() => {
  const doc = document.documentElement;
  const overflowX = doc.scrollWidth - doc.clientWidth;
  const offenders = [];
  if (overflowX > 1) {
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.right > doc.clientWidth + 1 && !el.closest('.fig-scroll') && !el.closest('pre')) {
        offenders.push((el.tagName + '.' + el.className).slice(0, 80));
        if (offenders.length >= 8) break;
      }
    }
  }
  // 图示里渲染后小于 11px 的文字
  const tinyText = [];
  for (const t of document.querySelectorAll('figure.fig svg text')) {
    const h = t.getBoundingClientRect().height;
    if (h > 0 && h < 11) tinyText.push({ text: t.textContent.trim().slice(0, 20), px: +h.toFixed(1) });
  }
  return { overflowX, offenders, tinyText: tinyText.slice(0, 20), figures: document.querySelectorAll('figure.fig').length };
}
"""


def slugify(path: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_-]+", "_", path.strip("/")) or "home"
    return s


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--base", default="http://localhost:1313")
    args = ap.parse_args()

    report = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for path in args.paths:
            path = "/" + path.strip("/") + "/" if path.strip("/") else "/"
            out_dir = OUT / slugify(path)
            out_dir.mkdir(parents=True, exist_ok=True)
            page_report = {}
            for vp_name, (w, h) in VIEWPORTS.items():
                for theme in THEMES:
                    ctx = browser.new_context(
                        viewport={"width": w, "height": h},
                        device_scale_factor=2 if vp_name == "mobile" else 1,
                        color_scheme=theme,
                    )
                    ctx.add_init_script(f"localStorage.setItem('pref-theme', '{theme}')")
                    page = ctx.new_page()
                    page.goto(args.base.rstrip("/") + path, wait_until="load")
                    page.wait_for_timeout(500)
                    shot = out_dir / f"{vp_name}-{theme}.png"
                    page.screenshot(path=str(shot), full_page=True)
                    page_report[f"{vp_name}-{theme}"] = {"screenshot": str(shot.relative_to(ROOT)), **page.evaluate(CHECK_JS)}
                    ctx.close()
            report[path] = page_report
            (out_dir / "report.json").write_text(json.dumps(page_report, ensure_ascii=False, indent=2), encoding="utf-8")
        browser.close()

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
