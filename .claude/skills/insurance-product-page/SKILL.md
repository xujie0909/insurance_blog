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

**⚠️ 先读完 [REFERENCE.md § blog-writing-style](REFERENCE.md#blog-writing-style) 再动笔。**

核心原则：
- **读者是谁**：保险小白，对医学/保险术语没有概念。所有专有名词必须用大白话解释。
- **目的是什么**：让读者深切感受到这款产品能在什么生活场景下帮到他，不是做学术分析。
- **优势重点突出，劣势一笔带过**。公司背景不需要展开。
- Front Matter 参考：`howtopost.txt`
- 详细写作规范见 [REFERENCE.md](REFERENCE.md#blog-article)
- **AI 写作避坑清单**见 [REFERENCE.md](REFERENCE.md#ai-anti-patterns)

### Step 3 — 生成 H5 详解页

文件路径：`static/pages/<slug>/index.html`

**以 `static/pages/zhongan-zunxiang-esheng-2026/index.html` 为模板，复制后替换内容。**

设计要求（单 HTML 文件，无外部依赖）：
- **浅色系 + 卡片式布局**：白色背景（`#f7f8fa`），白色卡片，无玻璃拟态
- **主色按产品类型**：医疗险绿色（`#1a6e5c`）/ 成人重疾蓝色（`#1a4a6e`）/ 少儿重疾紫色（`#7b4a9e`）
- **Hero 头图**：渐变背景 + 产品名 + 公司名，用 SVG 纹理点缀
- **必含模块**：TOC 目录 / 产品概览参数卡片 / 保障责任卡片（顶部色条区分必选可选）/ 理赔流程步骤条 / 关键参数表格 / 责任免除（红色面板） / 要点总结（优势+风险）
- **响应式**：`max-width: 960px`，`@media max-width:768px` 适配手机
- **无复杂动效**：不需要数字滚动、IntersectionObserver、进度条动画、渐变光晕
- 详细设计规范见 [REFERENCE.md](REFERENCE.md#h5-design)

### Step 4 — 链接 H5 到博客文章

在博客文章 Front Matter 之后、第一个 `##` 之前插入 H5 跳转卡片。**卡片配色与产品主色保持一致**：

医疗险（绿色）示例：
```markdown
{{< rawhtml >}}
<a href="/pages/<slug>/" target="_blank" style="display:block;margin:0 0 28px;padding:16px 20px;background:linear-gradient(135deg,#0d4f41,#1a6e5c);border:1px solid rgba(26,110,92,0.35);border-radius:14px;text-decoration:none;color:inherit;">
  ...
</a>
{{< /rawhtml >}}
```

成人重疾险用蓝色渐变（`#0d2e4f,#1a4a6e`），少儿重疾险用紫色渐变（`#4a1a6e,#7b4a9e`）。

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
