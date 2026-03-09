---
name: news-fetcher
description: 绕过付费墙获取新闻文章的工具。用于当用户想要阅读某个付费新闻文章时。支持 WSJ、NYT、Bloomberg、Medium 等主流媒体。使用场景：(1) 用户提供新闻链接要求获取内容 (2) 用户询问某篇新闻报道的详细内容 (3) 用户想绕过付费墙阅读文章。触发词：新闻、付费墙、paywall、文章、阅读、获取、绕过。
---

# News Fetcher - 新闻获取工具

绕过付费墙，获取新闻文章完整内容。

## 核心流程

### ⚠️ 重要：两阶段工作流

**第一阶段：浏览**
1. 访问新闻网站首页（如 cn.wsj.com、cn.nikkei.com）
2. 使用 browser 工具获取页面快照
3. 提取新闻标题、摘要、链接
4. 整理成清晰列表展示给用户

**第二阶段：深挖（仅在用户请求时）**
1. 用户指出感兴趣的文章
2. 对该文章使用绕过技巧获取完整内容
3. 如果无法绕过，找替代信源

### 为什么分两阶段？

- **效率**：首页新闻列表通常可以直接获取，无需绕过
- **用户主导**：让用户决定想看什么，而不是盲目获取
- **资源节约**：只对真正需要的文章使用绕过技巧

## 详细流程

**1. 识别信源 → 2. 选择策略 → 3. 执行获取 → 4. 回退方案**

---

## Step 1: 识别信源类型

### 付费墙难度分级

| 难度 | 媒体 | 策略 |
|------|------|------|
| ⭐ | BBC, Reuters, AP, NPR | 直接访问 |
| ⭐⭐ | Medium, Substack | 12ft.io / Reader Mode |
| ⭐⭐⭐ | NYT, WaPo, Guardian | smry.ai / 禁用JS |
| ⭐⭐⭐⭐ | Bloomberg, Economist | smry.ai → BPC扩展 → 找替代 |
| ⭐⭐⭐⭐⭐ | WSJ, FT | **直接找替代信源** |

详见 [付费墙难度矩阵](references/paywall-matrix.md)

---

## Step 2: 选择获取策略

### 策略 A: 直接访问（免费信源）

**首选信源：**
- BBC.com
- Reuters.com
- APNews.com
- NPR.org
- ProPublica.org

**操作:** 直接 `web_fetch`

### 策略 B: 绕过工具（中等难度）

**推荐顺序：**

```
1. smry.ai/{链接}          # 推荐，带总结
2. 12ft.io/{链接}          # 博客类效果好
3. removepaywalls.com/{链接} # 搜索多个归档
4. r.jina.ai/http://{链接}   # 纯文本提取
```

**操作示例:**
```
web_fetch url="https://smry.ai/www.example.com/article"
```

### 策略 C: 高级技术（较难付费墙）

详见 [进阶技巧](references/advanced-techniques.md)

**快速方法：**

1. **禁用 JavaScript**
   - F12 → Settings → Disable JavaScript
   - 刷新页面

2. **切换 User-Agent**
   - F12 → Network conditions → User agent: Googlebot
   - 某些网站允许爬虫完整访问

3. **归档工具**
   ```
   https://webcache.googleusercontent.com/search?q=cache:{链接}
   https://web.archive.org/web/*/{链接}
   https://archive.today/{链接}
   ```

4. **无痕模式 + 清除 Cookies**
   - 重置月度阅读计数

### 策略 D: 找替代信源（硬付费墙）

**WSJ/FT/经济学人 → 直接搜索替代**

**搜索策略:**

```bash
# 使用 Tavily 搜索
TAVILY_API_KEY=xxx node {baseDir}/../tavily-search/scripts/search.mjs "标题关键词 (site:bbc.com OR site:reuters.com OR site:apnews.com)" -n 5

# 或搜索 Twitter
"标题 site:twitter.com"
```

**替代信源优先级:**
1. BBC / Reuters / AP（国际新闻）
2. CNN / Al Jazeera（深度报道）
3. 本地媒体（区域新闻）
4. Twitter/X（记者链接）

### 策略 E: 浏览器访问（最后手段）

**适用场景:** 
- 其他方法都失败
- 需要查看图片/图表

**操作:**
```
browser action=open url="{链接}" profile=openclaw
browser action=snapshot
```

**注意:** 只能拿到开头部分

---

## Step 3: 执行获取

### 推荐执行顺序

```
1. 检查是否免费信源 → 直接获取
2. 尝试 smry.ai → 如果成功，返回
3. 尝试 12ft.io → 如果成功，返回
4. 尝试禁用 JS / 切换 UA
5. 搜索替代信源
6. 使用浏览器获取开头部分
7. 诚实告知无法获取
```

### 命令速查

```bash
# smry.ai
web_fetch url="https://smry.ai/{编码后的链接}"

# 直接提取
TAVILY_API_KEY=xxx node {baseDir}/../tavily-search/scripts/extract.mjs "{链接}"

# 搜索替代
TAVILY_API_KEY=xxx node {baseDir}/../tavily-search/scripts/search.mjs "关键词" -n 10
```

---

## Step 4: 回退方案

### 如果所有方法都失败

1. **诚实告知** - "无法绕过该网站的付费墙"
2. **提供替代** - 找到的相关免费链接
3. **总结片段** - 已获取的摘要内容
4. **建议方案** - 试用浏览器扩展、RSS 订阅等

### 免费替代信源

| 类型 | 推荐 |
|------|------|
| 国际新闻 | BBC, Reuters, AP, Al Jazeera |
| 财经新闻 | CNBC, MarketWatch (部分免费) |
| 科技新闻 | TechCrunch, Ars Technica (部分免费) |
| 调查报道 | ProPublica, Reveal |

---

## 工具对比

详见 [绕过工具对比](references/bypass-tools.md)

**快速参考:**

| 工具 | 效果 | 速度 | 稳定性 |
|------|------|------|--------|
| smry.ai | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 12ft.io | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| removepaywalls | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| r.jina.ai | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 注意事项

1. **尊重版权** - 仅供个人学习研究
2. **优先免费信源** - BBC/Reuters/AP 是第一选择
3. **诚实透明** - 失败时明确告知
4. **提供替代** - 即使失败也要提供相关链接
5. **合法合规** - 不用于商业用途

---

## 相关资源

- [专业新闻网站资源列表](references/news-sources.md) - 各领域专业新闻网站汇总
- [付费墙难度矩阵](references/paywall-matrix.md) - 各媒体付费墙详细分析
- [绕过工具对比](references/bypass-tools.md) - smry/12ft 等工具效果对比
- [进阶技巧](references/advanced-techniques.md) - 浏览器扩展、User-Agent、归档工具等
- [免费信源](references/free-sources.md) - 免费信源和 RSS 订阅

---

_此技能持续优化中。发现新的付费墙类型或更好的绕过方法，请更新相关文件。_
