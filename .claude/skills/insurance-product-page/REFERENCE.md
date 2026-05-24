# Reference — 保险产品页生成规范

## blog-article

### Front Matter 模板

```yaml
---
title: "<产品名>深度解析：<核心卖点>"
date: YYYY-MM-DD
draft: false
categories: ["重疾险"]          # 或 医疗险 / 寿险 / 少儿保险
tags: ["<产品名>", "<公司名>", "重疾险", "保障解析"]
description: "<100字以内摘要，含核心数字>"
cover:
  image: ""
  alt: "<产品名>深度解析"
---
```

### 文章结构（顺序不要乱）

1. **痛点开篇**（≤200字）— 用真实数字/场景让读者感受到风险，制造紧迫感
2. **产品简介** — 公司背景、产品定位一句话
3. **保障全景 Mermaid 脑图** — mindmap，必选+可选分支
4. **必选责任逐条拆解** — 每条含"白话解释"和举例金额
5. **可选责任** — 表格对比，标注适合人群
6. **高发病种列表** — Markdown 表格，前10种
7. **不赔清单** — 免责条款，用流程图或列表
8. **赔付场景对比表** — 以具体保额举例（如50万），多个场景
9. **理赔流程** — Mermaid flowchart，4~5步
10. **投保须知** — 等待期、犹豫期、如实告知
11. **CTA 结尾** — 情感收尾 + 行动召唤

### Mermaid 使用规则

- 脑图用 `mindmap`，流程图用 `flowchart LR` 或 `flowchart TD`
- 节点文字不要有特殊符号（括号除外），避免解析错误
- Hugo `--minify` 会破坏缩进，**不要使用 `--minify` 构建含 Mermaid 的文章**（或确认站点已有 Mermaid 修复脚本）

---

## h5-design

### CSS 变量（复用此配置，保持视觉统一）

```css
:root {
  --bg-deep:     #060812;
  --bg-card:     rgba(255,255,255,0.05);
  --border:      rgba(255,255,255,0.10);
  --blue-a:  #4facfe; --blue-b:  #00f2fe;
  --purple-a:#667eea; --purple-b:#764ba2;
  --gold-a:  #f6d365; --gold-b:  #fda085;
  --green-a: #43e97b; --green-b: #38f9d7;
  --red-a:   #ff6b6b; --red-b:   #ee0979;
  --text-1: #fff; --text-2: rgba(255,255,255,.75); --text-3: rgba(255,255,255,.50);
}
```

### 色彩语义规范

| 场景 | 使用色系 | 理由 |
|------|---------|------|
| 重大疾病 / 核心保障 | blue | 信任感、专业感 |
| 可选高价值责任 | gold | 价值感、稀缺感 |
| 轻症 / 豁免 / 正向 | green | 安全感 |
| 中度疾病 | purple | 中性、区分层级 |
| 免责 / 警示 / 风险 | red | 警示 |

### 必含模块（缺一不可）

| 模块 | 实现方式 |
|------|---------|
| 顶部导航丸子 | `position:sticky` + IntersectionObserver 高亮 |
| Hero 保障总览 | 数字滚动计数（data-count + setInterval） |
| Bento Grid 保障卡片 | `grid-template-columns: 1fr 1fr`，wide 项 `grid-column: span 2` |
| 病种手风琴列表 | `max-height: 0 → 800px` CSS transition |
| 可选责任卡片 | 顶部 2px 彩色 border + 玻璃卡片 |
| 赔付场景测算 | 横向进度条 + IntersectionObserver 触发动画 |
| 理赔流程 | 竖向步骤条，圆形序号 |
| 底部固定 CTA 栏 | `position:fixed; bottom:0` + backdrop-filter |

### 动效规范

```js
// 数字滚动（复用模板）
function animateCount(el) {
  const target = parseInt(el.dataset.count);
  let cur = 0, inc = target / (1200 / 16);
  const t = setInterval(() => {
    cur = Math.min(cur + inc, target);
    el.textContent = Math.floor(cur);
    if (cur >= target) clearInterval(t);
  }, 16);
}

// 滚动淡入（复用模板）
new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 }).observe(document.querySelectorAll('.fade-up'));
```

### 渐变光晕背景（固定模板）

```css
.orb { position:absolute; border-radius:50%; filter:blur(80px); opacity:.45;
       animation: orb-drift 18s ease-in-out infinite; }
@keyframes orb-drift {
  0%,100% { transform:translate(0,0) scale(1); }
  33%      { transform:translate(40px,-30px) scale(1.08); }
  66%      { transform:translate(-25px,45px) scale(.95); }
}
```

4个光晕球：左上蓝、右中紫、下中金、左下绿（opacity 0.30）。

---

## 内容质量检查清单

生成完成后逐项确认：

- [ ] 博客文章：有 Mermaid 脑图 + 至少一张流程图
- [ ] 博客文章：有"以50万保额举例"的具体赔付金额
- [ ] 博客文章：开头有 H5 跳转卡片
- [ ] H5 页面：手机端 max-width: 480px，viewport 含 maximum-scale
- [ ] H5 页面：至少3个 IntersectionObserver 动效
- [ ] H5 页面：病种列表可折叠展开
- [ ] H5 页面：底部 CTA 栏固定显示
- [ ] hugo --minify 构建无 ERROR
- [ ] git push 成功，终端显示 master → master
