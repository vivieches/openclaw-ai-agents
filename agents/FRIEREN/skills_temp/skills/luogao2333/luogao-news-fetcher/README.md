# News Fetcher 📰

**绕过付费墙，获取新闻文章的 OpenClaw 技能**

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ 功能特点

- 🔄 **两阶段工作流** - 先浏览新闻列表，再深挖感兴趣的文章
- 🛠️ **5种绕过策略** - smry.ai、12ft.io、禁用JS、归档工具、找替代信源
- 📊 **10大领域覆盖** - 财经、科技、体育、政治、科学、娱乐、国际、中文、环境、加密货币
- 🎯 **付费墙分级** - 根据难度自动选择最佳策略
- 📚 **70+专业网站** - 整理了各领域顶级新闻源

---

## 📦 安装

### ClawHub（推荐）

```bash
clawhub install news-fetcher
```

### 手动安装

```bash
git clone https://github.com/openclaw/news-fetcher-skill.git
cd news-fetcher-skill
# 复制到你的 skills 目录
cp -r . /path/to/.openclaw/workspace/skills/news-fetcher
```

---

## 🚀 快速开始

### 场景 1：浏览新闻

```
用户：看看华尔街日报有哪些新闻
我：[访问 cn.wsj.com，展示新闻列表]
用户：我对"伊朗导弹城"感兴趣
我：[使用绕过技巧获取文章内容]
```

### 场景 2：获取特定文章

```
用户：帮我获取这篇 NYT 文章：https://nytimes.com/...
我：[尝试 smry.ai → 12ft.io → 找替代]
```

---

## 🛠️ 绕过策略

### 策略 A：直接访问（免费信源）
- BBC、Reuters、AP、NPR

### 策略 B：绕过工具（中等难度）
- smry.ai（推荐）
- 12ft.io
- removepaywalls.com
- r.jina.ai

### 策略 C：高级技术（较难付费墙）
- 禁用 JavaScript
- User-Agent 切换
- 归档工具（Google Cache、Wayback Machine）

### 策略 D：找替代信源（硬付费墙）
- 搜索 BBC/Reuters/AP 等免费报道

### 策略 E：浏览器访问（最后手段）
- 可能只能获取开头部分

---

## 📊 付费墙难度分级

| 难度 | 媒体 | 策略 |
|------|------|------|
| ⭐ | BBC, Reuters, AP | 直接访问 |
| ⭐⭐ | Medium, Substack | 12ft.io / smry.ai |
| ⭐⭐⭐ | NYT, WaPo, Guardian | smry.ai / 禁用JS |
| ⭐⭐⭐⭐ | Bloomberg, Economist | BPC扩展 / 找替代 |
| ⭐⭐⭐⭐⭐ | WSJ, FT | **必须找替代信源** |

---

## 📂 文件结构

```
news-fetcher/
├── SKILL.md                      # 主文档
├── README.md                     # 本文件
├── scripts/
│   └── fetch_news.mjs            # 自动获取脚本
└── references/
    ├── news-sources.md           # 专业网站资源（70+）
    ├── paywall-matrix.md         # 付费墙难度分析
    ├── bypass-tools.md           # 绕过工具详细对比
    ├── advanced-techniques.md    # 进阶技巧
    └── free-sources.md           # 免费信源+RSS订阅
```

---

## 🌍 覆盖领域

| 领域 | 主要信源 |
|------|---------|
| 📊 财经 | Bloomberg, WSJ, FT, Reuters, CNBC |
| 💻 科技 | TechCrunch, The Verge, Wired, Ars Technica |
| ⚽ 体育 | ESPN, BBC Sport, CBS Sports |
| 🏛️ 政治 | Politico, Axios, ProPublica, The Hill |
| 🔬 科学 | Nature, Science, ScienceDaily |
| 🎬 娱乐 | Variety, Hollywood Reporter, Vulture |
| 🌍 国际 | BBC, Reuters, AP, Al Jazeera |
| 🇨🇳 中文 | 财新, 端传媒, BBC中文, 日经中文 |
| 🌱 环境 | Carbon Brief, Inside Climate News |
| 💰 加密 | CoinDesk, CoinTelegraph, Decrypt |

---

## ⚙️ 依赖

- **可选**: Tavily API（用于搜索和提取）
- **内置**: Browser 工具（用于访问新闻网站）

---

## 📝 使用示例

### 命令行脚本

```bash
# 使用 smry.ai 获取文章
node scripts/fetch_news.mjs https://example.com/article --method smry

# 尝试所有方法
node scripts/fetch_news.mjs https://example.com/article --all

# 搜索替代文章
node scripts/fetch_news.mjs --search "伊朗导弹城"
```

### 在 OpenClaw 中

```
用户：看看日经中文网有哪些新闻
我：[访问 cn.nikkei.com，展示新闻列表]

用户：我想看"中国2026年GDP目标"这篇文章
我：[尝试获取，如果失败则找替代信源]
```

---

## ⚠️ 注意事项

1. **尊重版权** - 仅供个人学习研究
2. **优先免费信源** - BBC/Reuters/AP 是第一选择
3. **诚实透明** - 失败时明确告知
4. **合法合规** - 不用于商业用途

---

## 🤝 贡献

欢迎贡献新的：
- 绕过技巧
- 新闻网站资源
- 付费墙分析

请提交 Pull Request 或创建 Issue。

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🔗 相关链接

- [OpenClaw 官网](https://openclaw.ai)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [ClawHub 技能市场](https://clawhub.com)
- [GitHub 仓库](https://github.com/openclaw/news-fetcher-skill)

---

## 📊 版本历史

- **v2.0** (2026-03-05)
  - 添加两阶段工作流
  - 新增 70+ 专业网站资源
  - 优化绕过策略
  - 添加详细参考文档

- **v1.0** (2026-03-05)
  - 初始版本

---

_Made with ❤️ for OpenClaw_
