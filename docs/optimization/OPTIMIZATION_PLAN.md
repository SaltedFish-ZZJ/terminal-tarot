# 代码优化计划

基于专业代码审查，制定以下优化任务。

---

## 优先级说明

- **P0**: 必须修复 - 影响核心功能可靠性
- **P1**: 应该修复 - 代码质量提升
- **P2**: 可以改进 - 技术债务清理

---

## 任务清单

### P0 - 核心可靠性

- [x] **T1: 提取 conftest.py 消除 Mock 重复** ✅ (v0.7.6)
  - 将 `test_business.py` 和 `test_integration.py` 中的 MockAI/MockTUI 提取到 `conftest.py`
  - 减少维护成本，修改接口时只需改一处

- [x] **T2: 统一 REVERSED_PROBABILITY** ✅ (v0.7.6)
  - 将 `app.py` 和 `spreads_ui.py` 中的重复定义提取到 `style.py`

### P1 - 代码质量

- [x] **T3: 统一正则表达式定义** ✅ (v0.7.6)
  - `style.py` 和 `renderer.py` 中的 ANSI 正则重复，统一到 `style.py`

- [x] **T4: 改进 _show_reading 线程处理** ✅ (v0.7.6)
  - 使用更清晰的超时处理逻辑，避免潜在竞态

### P2 - 技术债务

- [~] **T5: 删除 sys.path.insert 临时方案** — 保留（支持直接运行 `python main.py`）
  - 依赖 `pip install -e .` 安装

- [~] **T6: 清理 cards/ 目录结构** — 低优先级（愚者牌有独立颜色映射，合并需修改）
  - 合并 fool.py 到合适的文件，统一命名

---

## 当前状态

- **项目版本**: v0.7.6
- **测试数量**: 123 个，全部通过（1 个 Windows 环境问题跳过）
- **代码行数**: ~6250 行
- **综合评分**: 7.5/10

## 已完成

- [x] T1: 提取 conftest.py 消除 Mock 重复 ✅
- [x] T2: 统一 REVERSED_PROBABILITY ✅
- [x] T3: 统一正则表达式定义 ✅
- [x] T4: 改进线程超时处理 ✅
- [~] T5: sys.path.insert — 保留
- [~] T6: cards/ 目录结构 — 低优先级
