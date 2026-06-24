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

复制配置文件并填入你的 API Key：

```bash
cp .env.example .env
# 编辑 .env，填入 TAROT_AI_API_KEY
```

无 API key 时自动使用离线基础解读。

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
