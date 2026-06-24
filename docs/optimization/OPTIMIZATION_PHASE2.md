# Phase 2 优化计划

基于代码审查，继续优化项目质量。

---

## 任务清单

### P0 - 核心质量

- [ ] **T1: 添加 pytest-cov 覆盖率配置**
  - 配置 pyproject.toml 支持覆盖率
  - 运行 baseline 覆盖率报告

- [ ] **T2: 为 SpreadUI 补充核心测试**
  - 测试 do_single_reading 流程
  - 测试 do_three_card_reading 流程
  - 测试 do_celtic_cross_reading 流程

### P1 - 代码质量

- [ ] **T3: 添加 ruff linting 配置**
  - 配置 pyproject.toml
  - 修复 linting 警告

- [ ] **T4: 添加 mypy 类型检查**
  - 配置 pyproject.toml
  - 修复类型错误

### P2 - 架构改进

- [ ] **T5: style.py 拆分**
  - 颜色定义保留在 style.py
  - 工具函数提取到 utils.py

- [ ] **T6: 统一输出方式**
  - app.py 中统一使用 Rich

---

## 当前状态

- **项目版本**: v0.7.6
- **测试数量**: 122 个（1 个跳过）
- **Phase 1 完成**: Mock 重复、常量统一、正则统一、线程处理
