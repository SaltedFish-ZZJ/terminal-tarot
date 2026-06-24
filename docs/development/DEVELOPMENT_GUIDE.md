# 开发指南 — 终端塔罗牌

> **用途**：下一次启动开发时的完整参考指南
> **最后更新**：2026-06-22
> **当前版本**：v0.7.2

---

## 一、快速启动

### 1.1 项目概览

```
tarot-cli/
├── tarot/                    # 核心代码
│   ├── app.py               # 主控制器 (294行)
│   ├── spreads_ui.py        # 牌阵 UI (378行)
│   ├── history_ui.py        # 历史 UI (147行)
│   ├── interfaces.py        # 接口定义 (125行)
│   ├── tui.py               # TUI 引擎 (490行)
│   ├── renderer.py          # 卡片渲染 (417行)
│   ├── animations.py        # 动画效果 (418行)
│   ├── style.py             # 样式常量 (120行)
│   ├── ai_reader.py         # AI 集成 (242行)
│   ├── deck.py              # 牌组数据 (588行)
│   └── log.py               # 历史记录 (164行)
├── tests/                   # 测试套件
├── docs/                    # 文档目录
├── main.py                  # 入口点
└── README.md                # 项目说明
```

### 1.2 运行项目

```bash
# 进入项目目录
cd D:/agent_workspace/tarot-cli

# 运行项目
python -m tarot

# 跳过启动动画
python -m tarot --skip-boot

# 查看版本
python -m tarot --version

# 查看帮助
python -m tarot --help
```

### 1.3 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行并显示详细输出
python -m pytest -v

# 运行并显示覆盖率
python -m pytest --cov=tarot
```

---

## 二、文档导航

### 2.1 核心文档

| 文档 | 用途 | 优先级 |
|------|------|--------|
| **README.md** | 项目介绍 | ⭐⭐⭐ |
| **TODO.md** | 开发任务清单 | ⭐⭐⭐ |
| **CHANGELOG.md** | 版本更新记录 | ⭐⭐⭐ |
| **DEVELOPMENT_GUIDE.md** | 本指南 | ⭐⭐⭐ |

### 2.2 优化文档

| 文档 | 用途 | 优先级 |
|------|------|--------|
| **CODE_OPTIMIZATION.md** | 代码质量分析 | ⭐⭐ |
| **PHASE2_EXPLAIN.md** | 统一常量优化解释 | ⭐⭐ |
| **PHASE4_EXPLAIN.md** | 补充测试计划 | ⭐⭐ |

### 2.3 测试文档

| 文档 | 用途 | 优先级 |
|------|------|--------|
| **TEST_PLAN.md** | 完整测试计划 | ⭐⭐ |
| **TEST_REPORT.md** | 测试结果报告 | ⭐⭐ |

### 2.4 项目文档

| 文档 | 用途 | 优先级 |
|------|------|--------|
| **CONTEXT.md** | 项目背景 | ⭐ |
| **.env** | 环境变量 | ⭐⭐⭐ |

---

## 三、代码架构

### 3.1 模块职责

```
┌─────────────────────────────────────────────────────────────┐
│                         app.py (294行)                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ 启动流程 │ │ 菜单逻辑 │ │ 帮助系统 │ │ 退出画面 │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │  tui.py │          │spreads_ui│          │history_ui│
   │  (490行)│          │ (378行) │          │ (147行)  │
   └─────────┘          └─────────┘          └─────────┘
        │                     │                     │
        ▼                     ▼                     ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │interfaces│          │renderer │          │   log   │
   │ (125行) │          │ (417行) │          │ (164行) │
   └─────────┘          └─────────┘          └─────────┘
```

### 3.2 依赖关系

```python
# app.py 依赖
from tarot.tui import TUI
from tarot.spreads_ui import SpreadUI
from tarot.history_ui import HistoryUI
from tarot.ai_reader import AIReader

# spreads_ui.py 依赖
from tarot.tui import TUI
from tarot.ai_reader import AIReader
from tarot.animations import shuffle_animation, reveal_card
from tarot.renderer import render_three_cards_horizontal, render_celtic_cross
from tarot.log import save_reading
from tarot.style import CARD_WIDTH, CARD_HEIGHT

# history_ui.py 依赖
from tarot.tui import TUI
from tarot.log import get_recent_readings
from tarot.style import S_GOLD, S_ACCENT, S_DIM
```

### 3.3 接口定义

```python
# interfaces.py
class AIService(ABC):
    """AI 服务接口"""
    @abstractmethod
    def is_configured(self) -> bool: ...
    @abstractmethod
    def read(self, question, cards, spread_name) -> str: ...
    @abstractmethod
    def close(self) -> None: ...

class TUIEngine(ABC):
    """TUI 引擎接口"""
    @abstractmethod
    def clear(self) -> None: ...
    @abstractmethod
    def print(self, *args, **kwargs) -> None: ...
    @abstractmethod
    def print_centered(self, text, style=None) -> None: ...
    # ... 更多方法
```

---

## 四、开发流程

### 4.1 新功能开发

**步骤 1：确定模块**
```
- 牌阵相关 → spreads_ui.py
- 历史相关 → history_ui.py
- 主流程 → app.py
- 渲染 → renderer.py
- 动画 → animations.py
- 样式 → style.py
```

**步骤 2：编写代码**
```python
# 示例：在 spreads_ui.py 中添加新牌阵
def do_new_spread(self, question: str) -> str:
    """新牌阵流程"""
    # 1. 洗牌动画
    shuffle_animation(self.tui.console)

    # 2. 抽牌逻辑
    drawn = random.sample(ALL_CARDS, 5)
    reversed_flags = [random.random() < REVERSED_PROBABILITY for _ in range(5)]

    # 3. 翻牌动画
    for i, (card, rev) in enumerate(zip(drawn, reversed_flags)):
        reveal_card(card, rev, position=f"位置{i+1}")

    # 4. 全景渲染
    self._show_new_spread_panorama(drawn, reversed_flags)

    # 5. AI 解读
    return self._show_reading(
        question=question,
        cards=[{"card": c, "reversed": r, "position": f"位置{i+1}"} 
               for i, (c, r) in enumerate(zip(drawn, reversed_flags))],
        spread_name="新牌阵",
    )
```

**步骤 3：添加到菜单**
```python
# 在 app.py 的 _show_menu 方法中
options = [
    ("1", "单牌指引", "快速抽一张牌"),
    ("2", "三牌占卜", "过去 · 现在 · 未来"),
    ("3", "凯尔特十字", "深度解读（10张牌）"),
    ("4", "新牌阵", "新牌阵描述"),  # 添加新选项
    ("h", "历史记录", f"共 {count} 条"),
    ("q", "退出", ""),
]

# 在选择处理中
if choice == "4":
    return self.spread_ui.do_new_spread(question)
```

**步骤 4：编写测试**
```python
# tests/test_spreads.py
def test_new_spread():
    """测试新牌阵"""
    spread_ui = SpreadUI(MockTUI(), MockAI())
    result = spread_ui.do_new_spread("测试问题")
    assert result == "menu"
```

**步骤 5：更新文档**
```bash
# 更新 CHANGELOG.md
## v0.8.0 (2026-XX-XX) — 新牌阵
- **新牌阵** — 添加新牌阵功能

# 更新 TODO.md
- [x] 新牌阵功能
```

### 4.2 Bug 修复流程

**步骤 1：定位问题**
```bash
# 运行测试
python -m pytest -v

# 查看错误信息
# 定位到具体文件和行号
```

**步骤 2：复现问题**
```python
# 编写失败的测试
def test_bug_fix():
    """测试 bug 修复"""
    # 复现 bug
    result = buggy_function(input)
    assert result == expected  # 这里会失败
```

**步骤 3：修复代码**
```python
# 修复 bug
def buggy_function(input):
    # 修复后的代码
    return correct_result
```

**步骤 4：验证修复**
```bash
# 运行测试
python -m pytest tests/test_bug.py -v

# 运行所有测试
python -m pytest
```

**步骤 5：提交代码**
```bash
git add -A
git commit -m "fix: 修复 [问题描述]"
```

---

## 五、测试指南

### 5.1 测试类型

| 类型 | 文件 | 数量 | 覆盖范围 |
|------|------|------|---------|
| 单元测试 | test_*.py | 22 | 数据层、工具层、配置层 |
| 集成测试 | - | 0 | 待补充 |
| UI 测试 | - | 0 | 待补充 |
| 边界测试 | - | 0 | 待补充 |

### 5.2 编写测试

```python
# tests/test_example.py
import pytest
from tarot.style import display_width

class TestDisplayWidth:
    """测试 display_width 函数"""
    
    def test_ascii(self):
        """测试 ASCII 字符"""
        assert display_width("hello") == 5
    
    def test_cjk(self):
        """测试 CJK 字符"""
        assert display_width("你好") == 4
    
    def test_mixed(self):
        """测试混合字符"""
        assert display_width("hi你好") == 6
    
    def test_empty(self):
        """测试空字符串"""
        assert display_width("") == 0
```

### 5.3 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试文件
python -m pytest tests/test_style.py

# 运行特定测试类
python -m pytest tests/test_style.py::TestDisplayWidth

# 运行特定测试方法
python -m pytest tests/test_style.py::TestDisplayWidth::test_ascii

# 运行并显示详细输出
python -m pytest -v

# 运行并显示覆盖率
python -m pytest --cov=tarot --cov-report=html
```

---

## 六、Git 工作流

### 6.1 分支策略

```
master (主分支)
├── feature/xxx (功能分支)
├── fix/xxx (修复分支)
└── refactor/xxx (重构分支)
```

### 6.2 提交规范

```
feat: 新功能
fix: Bug 修复
refactor: 重构
docs: 文档更新
test: 测试相关
chore: 构建/工具相关
```

**示例**：
```bash
git commit -m "feat: 添加新牌阵功能"
git commit -m "fix: 修复居中输入问题"
git commit -m "refactor: 拆分 app.py"
git commit -m "docs: 更新 CHANGELOG"
git commit -m "test: 添加集成测试"
```

### 6.3 常用命令

```bash
# 查看状态
git status

# 查看提交历史
git log --oneline -10

# 创建分支
git checkout -b feature/new-spread

# 切换分支
git checkout master

# 合并分支
git merge feature/new-spread

# 创建标签
git tag v0.8.0

# 推送到远程
git push origin master
```

---

## 七、环境配置

### 7.1 依赖安装

```bash
# 安装项目依赖
pip install -e .

# 或者手动安装
pip install rich prompt_toolkit httpx

# 开发依赖
pip install pytest pytest-cov
```

### 7.2 环境变量

创建 `.env` 文件：
```env
# AI 配置
TAROT_AI_API_KEY=your_api_key
TAROT_AI_BASE_URL=https://api.deepseek.com
TAROT_AI_MODEL=deepseek-chat
```

### 7.3 IDE 配置

**VS Code**：
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"]
}
```

**PyCharm**：
1. 设置 Python 解释器
2. 配置 pytest 作为测试运行器
3. 配置代码风格（PEP 8）

---

## 八、常见问题

### 8.1 导入错误

**问题**：`ModuleNotFoundError: No module named 'tarot'`

**解决**：
```bash
# 确保在项目根目录
cd D:/agent_workspace/tarot-cli

# 安装项目
pip install -e .
```

### 8.2 测试失败

**问题**：测试失败但代码看起来正确

**解决**：
```bash
# 清理缓存
rm -rf __pycache__ .pytest_cache

# 重新运行测试
python -m pytest -v
```

### 8.3 编码问题

**问题**：Windows 终端显示乱码

**解决**：
```python
# 在代码开头添加
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
```

---

## 九、性能优化

### 9.1 启动优化

```python
# 延迟导入
def heavy_function():
    import heavy_module  # 只在需要时导入
    ...
```

### 9.2 渲染优化

```python
# 缓存计算结果
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(x):
    ...
```

### 9.3 内存优化

```python
# 使用生成器
def process_large_data():
    for item in large_dataset:
        yield process(item)
```

---

## 十、下一步计划

### 10.1 短期目标（1-2周）

- [ ] **Phase 4: 补充测试**
  - 集成测试（牌阵流程）
  - 边界条件测试（输入验证）
  - 测试覆盖率 30% → 80%

- [ ] **版本发布**
  - 创建 v0.7.2 标签
  - 推送到远程仓库

### 10.2 中期目标（1个月）

- [ ] **新功能开发**
  - 新牌阵类型
  - 历史数据导出
  - 终端标题管理

- [ ] **性能优化**
  - 启动时间优化
  - 渲染性能优化

### 10.3 长期目标（3个月）

- [ ] **架构升级**
  - 插件系统
  - 主题系统
  - 多语言支持

- [ ] **生态建设**
  - 文档完善
  - 社区建设
  - 版本发布

---

## 十一、资源链接

### 11.1 官方文档

- **Python**: https://docs.python.org/3/
- **Rich**: https://rich.readthedocs.io/
- **prompt_toolkit**: https://python-prompt-toolkit.readthedocs.io/
- **pytest**: https://docs.pytest.org/

### 11.2 工具

- **Git**: https://git-scm.com/
- **VS Code**: https://code.visualstudio.com/
- **PyCharm**: https://www.jetbrains.com/pycharm/

### 11.3 学习资源

- **Python 教程**: https://docs.python.org/3/tutorial/
- **测试教程**: https://docs.pytest.org/en/stable/getting-started.html
- **Git 教程**: https://git-scm.com/docs/gittutorial

---

## 十二、总结

### 12.1 项目状态

- ✅ **Phase 1 完成** — app.py 拆分
- ✅ **Phase 2 完成** — 统一常量
- ✅ **Phase 3 完成** — 接口隔离
- ⏳ **Phase 4 待做** — 补充测试

### 12.2 代码质量

- **可维护性**: ✅ 良好（模块职责清晰）
- **可测试性**: ✅ 良好（接口隔离）
- **可扩展性**: ✅ 良好（依赖注入）
- **测试覆盖**: ⚠️ 30%（待提升）

### 12.3 下一步行动

1. **立即行动**
   - 运行 `python -m tarot` 测试功能
   - 运行 `python -m pytest` 验证测试

2. **短期计划**
   - 补充测试（Phase 4）
   - 版本发布（v0.7.2）

3. **长期规划**
   - 新功能开发
   - 架构升级
   - 生态建设

---

> **文档版本**: v1.0
> **最后更新**: 2026-06-22
> **作者**: Claude Code
> **用途**: 下一次启动开发时的完整参考指南
