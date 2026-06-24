# CHANGELOG — 终端塔罗牌

## v0.7.5 (2026-06-24) — GitHub 发布准备

### 变更
- **统一版本号** — `pyproject.toml`、`__init__.py`、`main.py` 统一为 0.7.5
- **pyproject.toml** — 添加 authors、keywords、classifiers、project.urls
- **README.md** — 完整 GitHub 文档（特性、截图、快速开始、快捷键、AI配置、项目结构、技术栈）
- **LICENSE** — 添加 MIT 协议
- **.github/workflows/ci.yml** — GitHub Actions CI（Python 3.10-3.13）
- **.gitignore** — 允许 images/ 目录提交截图

### 优化
- **ai_reader.py** — 提取 `_build_card_info()` 和 `_build_prompt()` 方法，消除 `read()`/`read_stream()` 之间约 30 行重复代码
- **log.py** — `_prune_old_readings()` 改为单次遍历（`deque(maxlen=N)`），不再读两次文件；`get_reading_count()` 复用 `_read_all_entries()`，删除 20 行重复逻辑

### 测试
- 148 测试全部通过

---

## v0.7.4 (2026-06-22) — 稳定版本

### 功能
- **凯尔特十字终端尺寸检测** — 小终端自动降级为文字列表
  - `render_celtic_cross` 返回 `None` 当网格超出终端尺寸
  - `_show_celtic_cross_panorama` 检测返回值，降级时显示文字列表
  - 降级时显示提示 "(终端较小，使用列表模式)"

### 测试
- 新增凯尔特十字终端检测测试 (2个)
  - `test_returns_none_when_too_small` — 小终端返回 None
  - `test_returns_string_when_large_enough` — 大终端返回字符串

### 优化效果
- 测试数量：121 → 123
- 小终端用户体验提升

---

## v0.7.3 (2026-06-22) — 补充测试

### 测试
- **新增集成测试** — `test_integration.py`
  - AIService/TUIEngine 接口实现测试
  - 牌组数据完整性测试
  - 牌阵配置集成测试
  - 日志模块集成测试
- **新增 UI 测试** — `test_ui.py`
  - 渲染器测试（hex_to_rgb、render_ascii_art、render_card）
  - 动画渲染测试（card_back_raw、question_raw、text_card_raw）
  - 进度条测试
  - 三牌并排渲染测试
- **新增业务逻辑测试** — `test_business.py`
  - 卡牌业务逻辑测试
  - 牌阵配置测试
  - 占卜流程测试
  - 数据格式化测试
  - AI 服务测试
- **新增边界条件测试** — `test_edge_cases.py`
  - 输入边界测试（空字符串、CJK、Emoji）
  - 渲染边界测试（空数据、奇数高度）
  - 进度条边界测试（零宽度、负进度）
  - 缓存一致性测试
  - 文件异常测试
  - hex_to_rgb 边界测试
  - self_center_text 边界测试

### 优化效果
- 测试数量：22 → 121 (+450%)
- 测试覆盖：数据层、工具层、配置层 → +UI层、业务逻辑层、边界条件
- 全部测试通过

---

## v0.7.2 (2026-06-22) — 接口隔离

### 重构
- **创建接口定义** — 新增 `interfaces.py` 定义抽象接口
  - `AIService` — AI 服务接口（`is_configured`, `read`, `close`）
  - `TUIEngine` — TUI 引擎接口（`clear`, `print`, `print_centered`, `get_input` 等）
- **实现接口** — `AIReader` 和 `TUI` 类实现对应接口
  - `AIReader(AIService)` — 实现 AI 服务接口
  - `TUI(TUIEngine)` — 实现 TUI 引擎接口
- **依赖注入** — 模块间依赖接口而非实现

### 优化效果
- 降低耦合度 — 模块间通过接口通信
- 提升可测试性 — 可以 Mock 接口进行测试
- 提升可扩展性 — 更换实现只需实现接口
- 测试全部通过（22个）

---

## v0.7.1 (2026-06-22) — 统一常量优化

### 重构
- **统一常量定义** — 在 `style.py` 中添加卡片尺寸和动画参数常量
  - `CARD_WIDTH = 36` — 卡片宽度
  - `CARD_HEIGHT = 20` — 卡片高度
  - `FLIP_DURATION = 0.06` — 翻牌动画帧间隔
- **替换硬编码** — `animations.py` 中所有硬编码常量替换为统一常量
  - `_clip_line` 默认参数：`36` → `CARD_WIDTH`
  - `_flip_animation` 卡片宽度：`36` → `CARD_WIDTH`
  - `card_back_raw` 内容宽度：`34` → `CARD_WIDTH - 2`
  - `question_raw` 内容宽度：`34` → `CARD_WIDTH - 2`
  - `text_card_raw` 卡片宽度：`36` → `CARD_WIDTH`
  - 翻牌动画帧间隔：`0.06` → `FLIP_DURATION`

### 优化效果
- 常量定义：4 处 → 1 处 (-75%)
- 修改成本：改 4 处 → 改 1 处 (-75%)
- 测试全部通过（22个）

---

## v0.7.0 (2026-06-22) — 代码质量重构

### 重构
- **app.py 模块拆分** — 将 758 行的"上帝类"拆分为 3 个模块
  - `app.py` (294行) — 主控制器：启动、菜单、帮助、退出
  - `spreads_ui.py` (378行) — 牌阵 UI：单牌/三牌/凯尔特十字、全景渲染、AI 解读
  - `history_ui.py` (147行) — 历史 UI：历史列表、详情、关键词高亮
- **职责分离** — 每个模块只做一件事，改牌阵只改 spreads_ui.py，改历史只改 history_ui.py
- **依赖注入** — SpreadUI 和 HistoryUI 通过构造函数接收 TUI 和 AI 实例

### 优化效果
- app.py 行数：758 → 294 (-61%)
- app.py 方法数：20 → 8 (-60%)
- 修改成本降低 60%（改一个功能不需要理解整个文件）
- 测试全部通过（22个）

---

## v0.6.3 (2026-06-22)

### Bug 修复
- **居中输入修复** — 恢复 `Application` + `Window` 方案，修复 `PromptSession` 的 `get_line_prefix` 不生效导致输入不居中
- **Win32Output 恢复** — 修复 Windows 下 prompt_toolkit 渲染异常

---

## v0.6.2 (2026-06-22)

### 体验优化
- **凯尔特十字跳过功能** — 翻牌过程中按 S 可跳过剩余动画，直接显示全部牌 + AI 解读
- **三牌占卜跳过功能** — 同样支持按 S 跳过剩余翻牌动画
- **历史详情显示优化** — 移除逐字打印，改为整段显示 + 关键词高亮（牌名、方位等）
- **退出画面美化** — 星轨渐隐动画，文字渐显后逐行消失
- **居中输入 CJK 宽度修复** — 使用 `display_width()` 替代手写宽度计算，覆盖所有 Unicode 字符
- **动态居中输入** — 使用 `get_line_prefix` 动态计算居中，无论输入多长始终保持居中
- **帮助系统** — 按 ? 显示快捷键参考

### AI 稳定性
- **httpx 超时统一** — API 超时从 60s 改为 30s，与 UI 超时一致，避免线程泄漏
- **AI 错误友好化** — 移除技术细节（HTTP 状态码、异常类型），改为用户友好的提示
- **AI 重试机制** — 网络错误时自动重试 1 次，带指数退避（1s → 2s）

### Code Quality
- **参数解析重构** — `main.py` 从手写 for 循环改为 argparse，支持 --help

### Bug Fixes
- `tui.py` `pause` 方法返回值修复，支持跳过键检测
- `tui.py` `get_centered_input` CJK 宽度计算统一使用 `display_width()`
- **修复居中输入问题** — `get_centered_input` 修复 `accept_handler` 逻辑，正确返回用户输入
- **修复帮助键识别** — 支持中文全角问号 `？` 和英文半角问号 `?`

---

## v0.6.1 (2026-06-20)

### UI 优化
- **菜单页标题重设计** — 去掉 15 行 ASCII Logo，改为菱形角标 `◆─ · ─·◆` + `REVEAL DESTINY` 英文大字
- **菜单面板增强** — 分隔线 `─── ◇ ───`、列布局优化（`expand=True`、ratio 分配）
- **问题输入页极简重设计** — 去掉星轨装饰，标题居中 + ESC 返回提示
- **居中输入框** — 新增 `get_centered_input()`，用 `Application` + `get_line_prefix` 实现文字从屏幕中央向两侧流动
- **启动页文案** — "按 ENTER 开始占卜" → "按 ENTER 揭示命运"
- **启动页 Logo T 对齐** — TAROT/TERM 统一 37 字符宽度，首字母 T 对齐

### 交互优化
- **ESC 返回选牌阵** — 问题输入页按 ESC 回到牌阵选择（不再直接回菜单）
- 菜单项 `▸ [1/2/3/h/q]:` 保持不变

### Bug Fixes
- `tui.py` `build_menu_panel` `content.add_row(divider, justify="center")` → 改为 `content.add_column(justify="center")` 修复 TypeError
- 菜单面板 footer 居中对齐修复

---

## v0.6.0 (2026-06-19)

### UI 升级
- 全局居中：所有页面内容水平+垂直居中（菜单、解读、全景、历史、退出）
- `style.py` 新增 `vpad(content_lines)` — 垂直居中 helper
- 菜单页启用 `LOGO_LINES` ASCII art（中英结合：英文 ASCII + "终端塔罗牌" 中文标题）
- 菜单选项加图标装饰（🔮单牌、✦三牌、❀凯尔特十字、📜历史、🚪退出）
- 问题输入页提取 `_ask_question()` 公共方法，星轨装饰 + 居中标题
- 启动页去掉框外多余的 "按 ENTER 进入" 提示
- **启动页重设计**：像素风 `░░░` 边框 + Logo 中英结合 + 逐行动画
  - TAROT/TERM 字母宽度统一（36显示宽度），居中对齐
  - 星轨 `★ · · · · ★` 装饰
  - 分隔线 `─────── ◆ ───────`
  - 信息行 `▪ 78 张牌 ▪ 41 条记录`

### Bug Fixes
- `animations.py` `_center_plain` 未 strip ANSI → `display_width(strip_ansi(text))`
- panorama 卡片布局硬编码 2 空格缩进 → `center_line()` 逐行居中
- `_show_reading` 四个 Panel 左对齐 → `print_centered()` 居中
- 历史详情元数据/卡片行左对齐 → `print_centered()` 居中
- Logo TAROT/TERM 宽度不一致 → 统一 36 显示宽度

---

## v0.5.8 (2026-06-19)

### Bug Fixes
- `app.py` `_show_celtic_cross_panorama`/`_show_three_panorama` bare `except Exception` → `except (KeyError, ValueError, IndexError)`，不再吞编程错误

### Refactor
- `style.py` 新增 `C.rich()` 方法：`(r,g,b)` 元组 → Rich 兼容 `rgb(r,g,b)` 字符串
- `app.py`/`tui.py`/`animations.py` 全部 Rich 样式硬编码 `rgb(r,g,b)` → `S_*` 模块常量（~40 处），改主题色只需改 `style.py`
- `app.py` 提取 `_format_card_line()` 统一卡片信息格式化，消除 4 处重复逻辑
- `app.py` 删除 `spinner_frames` 死代码（定义但未引用）
- `app.py` loading spinner ANSI → `C.s(C.ACCENT)` / `C.s(C.REVERSED)`

---

## v0.5.7 (2026-06-19)

### Bug Fixes
- `log.py` 缓存命中逻辑 bug：`_cache_count` → `_cache_entries`，缓存实际条目列表而非仅计数（之前缓存命中仍全量读文件）
- `app.py` boot 后双 prompt：删除 `_show_boot()` 重复的 `input()`，由 `boot_animation()` 统一等待用户按 Enter
- `tui.py` `get_choice` 无效输入静默吞掉：改为红字提示 `⚠ 无效选项` 并重新等待，不再返回空串

### Perf
- `animations.py` `card_back_raw()`/`question_raw()` 加模块级缓存，只生成一次（之前每次调用重新生成 20 行曼陀罗花纹）

### Refactor
- `animations.py` 全部硬编码 ANSI 码 → `C.s()` / `C.bg()` 统一常量（`card_back_raw`、`question_raw`、`text_card_raw`、`_render_frame`、`_flash_effect`、`_show_keywords`）
- `tui.py` `blink_cursor`/`boot_animation`/`get_choice`/`get_input` 硬编码 ANSI → `C.s()` 常量

---

## v0.5.6 (2026-06-19)

### Bug Fixes
- `app.py` AI 调用线程无 timeout：添加 30 秒超时保护，超时后显示红色提示并返回 fallback 文本（之前 API 挂掉用户永远卡死）

### Refactor
- `ai_reader.py` 异常收窄：`except Exception` → `except httpx.RequestError`，不再吞掉 KeyError/TypeError 等编程错误
- `app.py` 移除 3 处冗余 `try/except`（`get_choice` 内部已处理所有异常）

### Perf
- `log.py` 性能优化：
  - `get_reading_count()` 添加 mtime 缓存，同一文件不重复逐行计数
  - `get_recent_readings()` 复用缓存，避免每次全量解析 JSON
  - `_prune_old_readings()` 仅超限时才触发读写（之前每次 save 都全量读写）

---

## v0.5.5 (2026-06-19)

### Bug Fixes
- `ai_reader.py` httpx.Client 资源泄漏：添加 `close()` + context manager，app.py 退出时释放连接池
- `ai_reader.py` import 副作用：`_load_dotenv()` 和 env 读取从模块级延迟到 `__init__`，import 不再改 env
- `renderer.render_card` 参数 `reversed` 遮蔽 Python 内置函数 → 重命名为 `is_reversed`

### Refactor
- 清理死代码（-72 行）：
  - 移除 `renderer.render_card_back`、`renderer.pause_for_input`、`log.format_reading_history`
  - 移除 `deck.CardDraw` TypedDict、`deck.CARD_BY_NAME`
  - 移除未使用 import：`ai_reader`(json/time)、`deck`(TypedDict)、`log`(Optional)

---

## v0.5.4 (2026-06-19)

### Bug Fixes
- `text_card_raw` CJK 居中：`str.center()` → `_center_plain()`，按显示宽度居中
- `_show_reading` 死代码："r" 重新占卜、"h" 查看历史（之前两个分支一样）
- `_show_boot` 硬编码 ANSI → `C.s(C.ACCENT)`
- `app.py` 移除重复 `sys.stdout.flush()`

### Refactor
- `animations.py`: 提取 `_clip_line`、`_flip_animation`、`_flash_effect`、`_show_keywords`、`_get_card_lines`
- `renderer.py`: 提取 `_prepare_card_renders`、`_place_card_on_grid`、`_build_position_map`、`_grid_to_lines`
- `tui.py` `boot_animation`: 复用 `render_boot_frame`，消除重复渲染（-41 行）

---

## v0.5.3 (2026-06-19)

- 修复 `TarotCard` 重复定义（Fool 同时在 major_arcana_part1 和 fool.py）
- 修复 `renderer.py` 缺少 `import re`
- 修复 Windows UTF-8 输出

---

## v0.5.2 (2026-06-19)

- 统一居中逻辑：`center_line()` in `style.py`，5 个居中函数收敛

---

## v0.5.1 (2026-06-19)

- `tui.py` 颜色快捷方式引用 `style.C` 而非裸 ANSI

---

## v0.5.0 (2026-06-19)

- 统一 `strip_ansi`/`term_width`/`term_height` 到 `style.py` 为单一来源

---

## v0.4.5 (2026-06-19)

- 历史记录自动清理（最多 200 条）

---

## v0.4.4 (2026-06-19)

- 添加 README.md 和 CONTEXT.md 文档

---

## v0.4.3 (2026-06-19)

- 添加 pyproject.toml，配置入口点和 pytest

---

## v0.4.2 (2026-06-19)

- 添加测试套件：21 个测试覆盖 deck、spreads、style、log
- 清理 `__pycache__` 跟踪

---

## v0.4.1 (2026-06-19)

- 移除 `major_arcana_part1.py` 中重复的 Fool 牌

---

## v0.4.0 (2026-06-19)

- 提取重复的 PALETTE 到 `cards/palette.py`

---

## v0.3.9 (2026-06-19)

- `import re` 从函数内联移到模块顶层

---

## v0.3.8 (2026-06-19)

- 提取魔法数字 0.35 为 `REVERSED_PROBABILITY` 常量

---

## v0.3.7 (2026-06-19)

- 重命名遮蔽的 `reversed` 参数为 `is_reversed`

---

## v0.3.6 (2026-06-19)

- 提取动画到 `animations.py`，app.py 880→579 行

---

## v0.3.5 (2026-06-19)

- 移除重复的 `term_width`/`auto_scale` 死代码

---

## v0.3.4 (2026-06-19)

- 提取重复的 `_display_width` 为 `style.display_width`

---

## v0.3.3 (2026-06-19)

- 修复版本不一致，菜单动态读取 `__version__`

---

## v0.3.2 (2026-06-19)

- 修复 .env API key 泄漏，添加 `.gitignore`

---

## v0.3.1 (2026-06-19)

- 加载动画（移动点动画）
- 边框对齐修复
- 菜单 flush 修复
- 阅读 UI 升级

---

## v0.3.0 (2026-06-19)

- 翻牌动画（牌背收缩→卡片展开）
- 曼陀罗花纹牌背
- 发光问号帧
- 洗牌进度条
- CJK 对齐修复

---

## v0.2.0 (2026-06-19)

- 8-bit 开机画面
- 闪烁光标
- `--skip-boot` 参数
- 版本管理

---

## v0.1.0 (2026-06-19)

- 初始版本
- 78 张完整塔罗牌（Rider-Waite）
- 3 种牌阵（单牌/三牌/凯尔特十字）
- AI 解读（DeepSeek + 月影 persona）
- TUI 界面（Rich + prompt_toolkit）
- 像素艺术渲染（半块字符 ▀）
- 占卜历史记录（JSONL）
