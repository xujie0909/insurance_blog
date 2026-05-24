---
name: insurance-product-page
description: 从保险产品条款PDF一键生成博客文章 + 精美H5详解页，并自动推送到Git。Use when user says "帮我生成XXX产品页"、"分析这个保险产品条款"、"给XXX写一篇博客"，或指定了 product/ 目录下的PDF文件时。
---

# 保险产品页一键生成

## 快速开始

用户说"帮我分析 product/XXX/保险条款.pdf 并生成产品页"时，按以下顺序执行。

## 执行清单

### Step 1 — 提取 PDF 文本

```bash
python .claude/skills/insurance-product-page/scripts/extract_pdf.py \
  "product/<产品目录>/保险条款.pdf" \
  "product/<产品目录>/条款文本.txt"
```

读取输出的 `条款文本.txt`，重点提取：
- 险种全名、承保公司
- 保障责任（必选 + 可选）：病种数、赔付比例、赔付次数
- 等待期 / 犹豫期 / 宽限期
- 责任免除（不赔清单）
- 理赔流程与材料

### Step 2 — 生成博客文章

文件路径：`content/posts/<slug>.md`

写作要求：
- Front Matter 参考：`howtopost.txt`
- 语言口语化，减少术语，多用"你"、"我"
- 开篇用痛点/场景勾住读者，制造紧迫感
- 用 Mermaid 脑图/流程图可视化保障结构和赔付流程
- 结尾有行动召唤（CTA）
- 详细规范见 [REFERENCE.md](REFERENCE.md#blog-article)

### Step 3 — 生成 H5 详解页

文件路径：`static/pages/<slug>/index.html`

设计要求（单 HTML 文件，无外部依赖）：
- 移动端优先（max-width: 480px 居中）
- 深色背景 + 玻璃拟态卡片 + 渐变光晕动画
- 必含：保障脑图（Bento Grid）、病种手风琴列表、赔付场景测算、理赔流程步骤
- 底部固定 CTA 栏、顶部导航丸子
- 微动效：数字滚动计数、进度条动画、滚动淡入
- 详细设计规范见 [REFERENCE.md](REFERENCE.md#h5-design)

### Step 4 — 链接 H5 到博客文章

在博客文章 Front Matter 之后、第一个 `##` 之前插入：

```markdown
{{< rawhtml >}}
<a href="/pages/<slug>/" target="_blank" style="display:block;margin:0 0 28px;padding:16px 20px;background:linear-gradient(135deg,#0d1b2e,#0a1628);border:1px solid rgba(79,172,254,0.35);border-radius:14px;text-decoration:none;color:inherit;">
  <div style="font-size:11px;color:#4facfe;font-weight:600;letter-spacing:.5px;margin-bottom:6px;">📊 互动版保障详解</div>
  <div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:4px;"><产品名> · 完整责任解析 H5 页面</div>
  <div style="font-size:13px;color:rgba(255,255,255,0.55);">点击查看精美互动版 →</div>
</a>
{{< /rawhtml >}}
```

### Step 5 — 检查基础配置

确认以下两项存在，不存在则创建：

**`layouts/shortcodes/rawhtml.html`**（若不存在）：
```
{{- .Inner | safeHTML -}}
```

**`hugo.toml`** 末尾需包含：
```toml
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
```

### Step 6 — 构建验证

```bash
hugo --minify
```

确认无 ERROR，`Static files` 计数 ≥ 1。

### Step 7 — Git 提交推送

```bash
git add content/posts/<slug>.md \
        static/pages/<slug>/index.html \
        layouts/shortcodes/rawhtml.html \
        hugo.toml
git commit -m "feat: 新增<产品名>博客文章与H5详解页"
git push origin master
```

## 常见问题

| 问题 | 解决 |
|------|------|
| PDF 提取乱码 | 改用 `encoding='latin-1'` 重新写入，或让用户确认 PDF 是否扫描版 |
| rawhtml 不渲染 | 检查 hugo.toml 的 `unsafe=true` 和 shortcode 文件是否存在 |
| Hugo build ERROR | 检查 Mermaid 代码块缩进，`--minify` 会压缩缩进导致解析失败 |
| H5 页面在手机上字太小 | 检查 viewport meta 标签是否含 `maximum-scale=1.0` |
