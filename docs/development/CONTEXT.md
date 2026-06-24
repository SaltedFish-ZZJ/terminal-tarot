# CONTEXT.md — 领域术语表

## 塔罗牌

- **Major Arcana（大阿尔卡那）**: 22 张主牌（0-21），代表人生重大主题
- **Minor Arcana（小阿尔卡那）**: 56 张副牌，分四元素（权杖/圣杯/宝剑/星币）
- **正位（Upright）**: 牌面正常朝上，正面含义
- **逆位（Reversed）**: 牌面倒置，含义反转或削弱
- **牌阵（Spread）**: 抽牌的布局方式，决定每张牌的位置含义

## 牌阵类型

- **单牌指引（Single）**: 抽一张牌，快速指引
- **三牌占卜（Three Card）**: 过去-现在-未来
- **凯尔特十字（Celtic Cross）**: 10 张牌深度解读

## 渲染

- **半块字符（Half-block）**: `▀` 字符，一个终端格子 = 上下两个像素
- **ANSI 24-bit 真彩色**: `\033[38;2;R;G;Bm` 格式，16M 色
- **像素艺术**: 32×40 网格，用 ASCII 字符 + 色板映射渲染

## AI

- **月影（Moon Shadow）**: AI 解读 persona，20 年经验塔罗师人设
- **DeepSeek**: AI 后端，model = `deepseek-chat`

## 项目结构

- `tarot/app.py`: 主应用流程
- `tarot/animations.py`: 洗牌/翻牌动画
- `tarot/tui.py`: TUI 引擎（Rich + prompt_toolkit）
- `tarot/renderer.py`: 像素艺术渲染引擎
- `tarot/deck.py`: 78 张牌数据
- `tarot/cards/`: 像素艺术数据
- `tarot/ai_reader.py`: AI 解读接口
- `tarot/log.py`: 历史记录（JSONL）
