# Terminal Tarot 终端塔罗牌占卜

终端像素艺术塔罗牌占卜工具，支持 AI 解读。

## 功能

- 78 张完整 Rider-Waite 塔罗牌
- 像素艺术渲染（ANSI 24-bit 真彩色半块字符）
- 三种牌阵：单牌指引、三牌占卜、凯尔特十字
- DeepSeek AI 解读（月影 persona）
- 占卜历史记录

## 安装

```bash
pip install -e .
```

或直接运行：

```bash
pip install -r requirements.txt
python main.py
```

## 使用

```bash
python main.py              # 交互模式
python main.py --skip-boot  # 跳过开机动画
python main.py --test       # 测试渲染愚者卡
python main.py --version    # 版本号
python main.py --help       # 查看帮助
```

## 快捷键

- `ESC` — 返回上一级菜单
- `S` — 跳过翻牌动画（凯尔特十字/三牌占卜）
- `R` — 重新占卜
- `H` — 查看历史记录
- `?` — 显示帮助

## AI 解读

本项目支持 DeepSeek API 进行智能塔罗解读。配置步骤：

1. 注册 [DeepSeek](https://platform.deepseek.com/) 账号，获取 API Key
2. 复制配置模板：
   ```bash
   cp .env.example .env
   ```
3. 编辑 `.env`，填入你的 Key：
   ```
   TAROT_AI_API_KEY=sk-xxxxxxxxxxxxxxxx
   ```

> **提示**：无 API Key 时自动使用离线基础解读，无需配置也能体验完整功能。

## 测试

```bash
python -m pytest tests/ -v
```

## 技术栈

- Python 3.10+
- Rich — 终端格式化
- prompt_toolkit — 键盘输入
- httpx — HTTP 客户端
- DeepSeek API — AI 解读
