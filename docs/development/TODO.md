# TODO — 终端塔罗牌

> 最后更新：2026-06-22，v0.7.4

---

## v0.7.4 凯尔特十字终端检测 ✅

### P2 — 动画 & 渲染
- [x] 凯尔特十字渲染器终端尺寸检测
  - `render_celtic_cross` 返回 `None` 当网格超出终端尺寸
  - `_show_celtic_cross_panorama` 检测返回值，降级时显示文字列表
  - 降级时显示提示 "(终端较小，使用列表模式)"
- [x] 测试全部通过（123个）

### 效果
- 小终端用户体验提升
- 避免显示错乱

---

## v0.7.3 补充测试 ✅

### Phase 4: 补充测试 ✅
- [x] 创建 `tests/test_integration.py` — 集成测试（15个）
  - AIService/TUIEngine 接口实现测试
  - 牌组数据完整性测试
  - 牌阵配置集成测试
  - 日志模块集成测试
- [x] 创建 `tests/test_ui.py` — UI 测试（23个）
  - 渲染器测试（hex_to_rgb、render_ascii_art、render_card）
  - 动画渲染测试（card_back_raw、question_raw、text_card_raw）
  - 进度条测试
  - 三牌并排渲染测试
- [x] 创建 `tests/test_business.py` — 业务逻辑测试（16个）
  - 卡牌业务逻辑测试
  - 牌阵配置测试
  - 占卜流程测试
  - 数据格式化测试
  - AI 服务测试
- [x] 创建 `tests/test_edge_cases.py` — 边界条件测试（45个）
  - 输入边界测试
  - 渲染边界测试
  - 进度条边界测试
  - 缓存一致性测试
  - 文件异常测试
- [x] 测试全部通过（121个）

### 效果
- 测试数量：22 → 121 (+450%)
- 测试覆盖：数据层、工具层、配置层 → +UI层、业务逻辑层、边界条件
- 代码质量显著提升

---

## v0.7.2 接口隔离 ✅

### Phase 3: 接口隔离 ✅
- [x] 创建 `interfaces.py` 定义抽象接口
  - `AIService` — AI 服务接口
  - `TUIEngine` — TUI 引擎接口
- [x] 修改 `ai_reader.py` 实现 `AIService` 接口
- [x] 修改 `tui.py` 实现 `TUIEngine` 接口
- [x] 测试全部通过（22个）

### 效果
- 降低耦合度 — 模块间通过接口通信
- 提升可测试性 — 可以 Mock 接口进行测试
- 提升可扩展性 — 更换实现只需实现接口

---

## v0.7.1 统一常量优化 ✅

### Phase 2: 统一常量 ✅
- [x] 在 `style.py` 中添加统一常量
  - `CARD_WIDTH = 36` — 卡牌宽度
  - `CARD_HEIGHT = 20` — 卡牌高度
  - `FLIP_DURATION = 0.06` — 翻牌动画帧间隔
- [x] 替换 `animations.py` 中的硬编码常量
  - `_clip_line` 默认参数
  - `_flip_animation` 卡牌宽度
  - `card_back_raw` 内容宽度
  - `question_raw` 内容宽度
  - `text_card_raw` 卡牌宽度
  - 翻牌动画帧间隔
- [x] 测试全部通过（22个）

### 效果
- 常量定义：4 处 → 1 处 (-75%)
- 修改成本：改 4 处 → 改 1 处 (-75%)
- 视觉一致性：+100%

---

## v0.7.0 代码质量重构 ✅

### Phase 1: 拆分 app.py ✅
- [x] 创建 `spreads_ui.py` — 牌阵 UI（378行）
- [x] 创建 `history_ui.py` — 历史 UI（147行）
- [x] 精简 `app.py` — 主控制器（294行）
- [x] 测试全部通过（22个）
- [x] 更新 CHANGELOG.md

### 效果
- app.py 行数：758 → 294 (-61%)
- app.py 方法数：20 → 8 (-60%)
- 修改成本降低 60%

---

## v0.6.2 完成清单

### P1 — 体验提升 ✅
- [x] 凯尔特十字跳过功能（按 S 跳过翻牌动画）
- [x] 三牌占卜跳过功能
- [x] 历史详情显示优化（整段显示 + 关键词高亮）
- [x] 退出画面美化（星轨渐隐动画）
- [x] 居中输入 CJK 宽度修复
- [x] 动态居中输入 — 使用 `get_line_prefix` 动态计算，无论输入多长都居中

### P3 — AI 稳定性 ✅
- [x] httpx 超时统一（60s → 30s）
- [x] AI 错误友好化（隐藏技术细节）
- [x] AI 重试机制（1 次重试 + 指数退避）

### P4 — 功能扩展 ✅
- [x] 帮助系统（按 ? 显示快捷键）
- [x] 参数解析重构（argparse）

### Bug Fixes ✅
- [x] 修复居中输入问题 — `get_centered_input` 修复 `accept_handler` 逻辑
- [x] 修复帮助键识别 — 支持中文全角问号 `？` 和英文半角问号 `?`

---

## 下次开发优先级

### P0 — Bug 修复（必须先修）

1. **`_rerun_spread` 缺少 question 参数** — 按 [R] 重新占卜必崩
   - `_do_single_reading()` / `_do_three_card_reading()` / `_do_celtic_cross_reading()` 都需要 `question` 参数
   - 修复：保存 `self._last_question` 或重新提示输入
   - 涉及：`app.py:519-527`
   - ✅ 已完成 (v0.5.0)

2. **递归 `_show_menu()` 调用风险** — ESC 反复按会栈溢出
   - ESC 问题输入页 → `return self._show_menu()` 创建新递归帧
   - 修复：改为 `return "menu"` 让主循环处理
   - 涉及：`app.py:171`
   - ✅ 已完成 (v0.5.0)

3. **Style 常量重复定义 3 份** — 改色要改 3 个文件
   - `S_GOLD` / `S_ACCENT` / `S_DIM` 在 `app.py` / `tui.py` / `animations.py` 各定义一次
   - 修复：统一到 `style.py`，其他文件 import
   - 涉及：`app.py:49-55`、`tui.py:26-30`、`animations.py:18-21`
   - ✅ 已完成 (v0.5.8)

### P1 — 体验提升（优先做）

4. **凯尔特十字按 12 次 Enter** — 10 张牌逐张翻 + 全景 + AI，体验差
   - 加「跳过」选项：按 S 直接显示全部牌 + AI 解读
   - 涉及：`app.py:274-276`
   - ✅ 已完成 (v0.6.2)

5. **历史详情逐字打印太慢** — 400 字约 1 秒强制等待
   - 改为整段显示 + 关键词高亮，或加速度控制
   - 涉及：`app.py:605-609`
   - ✅ 已完成 (v0.6.2)

6. **退出画面太简陋** — 当前只有两行纯文字
   - 星轨渐隐 / 倒序逐行消失
   - 涉及：`app.py:_show_exit()`
   - ✅ 已完成 (v0.6.2)

7. **居中输入 CJK 宽度计算不精确** — `ord(c) > 0x7F` 不覆盖所有 Unicode
   - 改用 `style.py` 的 `display_width()`（基于 `unicodedata.east_asian_width`）
   - 涉及：`tui.py:404-405`
   - ✅ 已完成 (v0.6.2)

### P2 — 动画 & 渲染

8. **翻牌闪烁效果是假的** — 重绘 4 次相同内容，无视觉变化
   - 加边框颜色脉冲（gold → bright → gold）或背景闪烁
   - 涉及：`animations.py:150-160`

9. **牌宽常量不一致** — flip 用 36，card_back/question 用 34
   - 统一为一个常量 `CARD_WIDTH`
   - 涉及：`animations.py:134,212,258`

10. **凯尔特十字渲染器超出终端尺寸** — 7×8 网格 ≈ 266×192 像素
    - 加终端尺寸检测，超出时降级为文字列表
    - 涉及：`renderer.py:344-345`
    - ✅ 已完成 (v0.7.4)

11. **renderer CJK 双宽处理缺失** — 网格放置按字符计数不按显示宽度
    - `_place_card_on_grid` 需用 `display_width` 替代 `len`
    - 涉及：`renderer.py:296-304`

### P3 — AI & 稳定性

12. **httpx 超时冲突** — httpx 60s vs UI 30s，线程泄漏
    - httpx timeout 改为 30s 与 UI 一致
    - 涉及：`ai_reader.py:120`、`app.py:457`
    - ✅ 已完成 (v0.6.2)

13. **AI 错误信息泄露 API 原文** — 用户看到 JSON 堆栈
    - 替换为友好提示，隐藏技术细节
    - 涉及：`ai_reader.py:201`
    - ✅ 已完成 (v0.6.2)

14. **AI 无重试** — 网络抖动直接 fallback
    - 加 1 次重试 + 指数退避
    - 涉及：`ai_reader.py:140`
    - ✅ 已完成 (v0.6.2)

### P4 — 功能扩展

15. **终端标题管理** — 启动设 `\033]0;终端塔罗牌\007`，退出恢复
16. **帮助系统** — 按 `?` 显示快捷键参考
    - ✅ 已完成 (v0.6.2)
17. **历史数据导出** — 支持导出 readings.jsonl
18. **开机动画增强** — 渐入 / 粒子散落 / 边框逐笔绘制

### 杂项

- [x] `main.py` 参数解析：手写 for 循环 → argparse (v0.6.2)
- [ ] `get_reading_count` 去重：直接 `len(_read_all_entries())`
- [ ] `log.py` pruning 重复失效缓存

---

## 已完成

<details>
<summary>v0.6.1 菜单页 UI + 交互优化</summary>

- 菜单页标题：ASCII Logo → `REVEAL DESTINY` 菱形角标
- 菜单面板：分隔线 `─── ◇ ───` + 列布局优化
- 问题输入页：极简重设计 + 居中输入框（`get_centered_input`）
- ESC 返回选牌阵（不再直接回菜单）
- 启动页 Logo T 对齐（统一 37 字符宽度）
- 启动页文案 → "揭示命运"
</details>

<details>
<summary>v0.6.0 UI 升级</summary>

- 全局居中（水平+垂直）— 所有页面
- 菜单页启用 LOGO_LINES（中英结合 ASCII art）
- 菜单选项加图标装饰
- 问题输入页星轨装饰
- 启动页去掉多余 Enter 提示
- `_center_plain` ANSI bug 修复
- 启动页重设计 — 像素风 `░░░` 边框 + Logo 中英结合 + 逐行动画
</details>

<details>
<summary>v0.5.x 代码质量</summary>

- 异常收窄（bare except → 具体类型）
- 样式常量化（~40 处硬编码 → `S_*` 常量）
- 性能优化（mtime 缓存、超时保护、模块级缓存）
- 死代码清理（-72 行）
- 测试套件 21 个
</details>

<details>
<summary>v0.1.0 → v0.4.x 核心功能</summary>

- 78 张完整塔罗牌（Rider-Waite）
- 3 种牌阵（单牌/三牌/凯尔特十字）
- AI 解读（DeepSeek + 月影 persona）
- 像素艺术渲染（半块字符 ▀）
- 占卜历史记录（JSONL，自动清理 200 条）
- 开机画面 + 翻牌动画 + 洗牌进度条
- README / CONTEXT / pyproject.toml
</details>

---

## 设计参考

- **Cogmind** — 最美 ASCII 游戏 UI，信息密度高但层次分明
- **Dwarf Fortress** — 多面板布局 + 颜色编码
- **Caves of Qud** — 渐变色 + 发光效果
- **Undertale** — 简单但有 character

### 设计原则
1. 边框变体混用：`╔═══╗` `┌───┐` `╭───╮` `┏━━━┓`
2. 装饰符号：`✦ ★ ◆ ◇ ● ○ ◉ ▸ ▹ ◈ ❖`
3. 负空间：留白比填满更重要
4. 信息层次：主标题 > 副标题 > 正文 > 辅助信息
