# FinTax 架构学习指南

## 目录
1. [核心概念](#核心概念)
2. [三大仓库详解](#三大仓库详解)
3. [Multi-Agent 工作流](#multi-agent-工作流)
4. [角色系统](#角色系统)
5. [实现要点](#实现要点)
6. [如何复刻](#如何复刻)

---

## 核心概念

### 什么是 FinTax 架构？

FinTax 是一个**用 AI 团队协作开发软件**的创新架构。它将传统软件开发团队的角色（架构师、项目经理、开发者、测试员等）映射为 AI 角色，通过协议文件定义每个角色的行为边界和工作流程。

### 核心设计理念

1. **角色分离** - 每个 AI 只负责特定职责，避免混乱
2. **协议驱动** - 用 Markdown 文件定义规则，而不是硬编码
3. **状态同步** - 用 Git 和 JSON 文件作为"共享内存"
4. **流水线执行** - 功能按固定顺序流转：设计 → 开发 → UI → 测试

---

## 三大仓库详解

### 1. fintax-ai-protocols（协议仓库）

**作用**：AI 系统的"宪法"

**核心文件**：
- `AI.md` - 角色激活入口，用户输入 `#architect` 时读取此文件
- `core_protocol.md` - 基础规则（Git 规范、学习协议等）
- `roles/*.md` - 7 个角色的定义文件
- `skills/expert/*.md` - 16 个可加载的技能模块

**关键点**：
- 只有 Architect 角色可以修改此仓库
- 其他角色只能读取，确保规则不被破坏
- 使用路径别名 `{protocols_repo}` 在所有文档中引用

### 2. fintax-suite-governance（治理仓库）

**作用**：项目状态的单一事实来源

**核心文件**：
- `genesis.md` - 产品需求文档（用户手写，只有 Solutionist 和 Observer 可读）
- `progress.json` - 全局生命周期状态（Principal 主维护）
- `featurelist.json` - Feature 注册表
- `proposals/` - 技术规格文档（Solutionist 输出）
- `decisions/` - 架构决策记录（不可修改，只能追加）
- `tests/` - 业务验收测试用例
- `db/` - 数据库 SQL 脚本

**关键点**：
- 所有角色都可以直接提交到 `dev` 分支
- 不使用 feature branch，简化协作
- `progress.json` 是核心，记录每个功能的每个角色的状态

**progress.json 结构示例**：
```json
{
  "modules": {
    "system": {
      "stage": "development",
      "features": {
        "SYS-001": {
          "phase": 1,
          "Solutionist": {"status": "completed"},
          "Coder": {"status": "completed"},
          "Stylist": {"status": "active"},
          "Tester": {"status": "pending"}
        }
      }
    }
  }
}
```

### 3. fintax-suite-codespace（代码仓库）

**作用**：实际业务代码

**技术栈**：
- 后端：Spring Boot 3 + MyBatis + PostgreSQL + Spring Modulith
- 前端：Vue 3 + Vite + TailwindCSS + shadcn-vue + Pinia

**关键点**：
- Coder 和 Stylist 使用 `git worktree` 在隔离分支开发
- 完成后提 PR 合并到 `dev` 分支
- 使用 Spring Modulith 实现模块化（package-level）

---

## Multi-Agent 工作流

### 角色激活流程

```
用户输入：#architect
  ↓
AI 读取 AI.md（角色选择协议）
  ↓
读取 roles/architect.md（加载角色定义）
  ↓
读取 core_protocol.md（加载基础规则）
  ↓
宣告：[ROLE ACTIVATED]: Architect
```

### Sub-agent 启动流程

这是 FinTax 最核心的创新点：

**1. Principal 轮询调度**
```bash
用户输入：#pri -poll
Principal 检查 progress.json
发现 SYS-003 的 Coder 状态是 pending
生成 session_id：claude-20260315-sys-003-coder
```

**2. 启动新终端 Tab**
```bash
scripts/new_subagent.sh 调用 osascript
在新的 Terminal Tab 中启动 Cline/Claude
传入完整任务描述（包含角色、仓库路径、功能 ID）
```

**3. Sub-agent 工作流**
```
Step 0: 创建 git worktree（如果是 Coder/Stylist）
Step 0a: Session Registration
        更新 progress.json（status=active, session_id）
        提交推送到 governance dev
Step 0b: 每 10 分钟写 checkpoint 到 dispatch_log.jsonl
...执行任务...
最后一步: 更新 progress.json（status=completed）
         写 completed 事件到 dispatch_log.jsonl
         关闭 Terminal Tab
```

### Feature 生命周期

```
Phase 0 (Ideation)  → 只是想法，不生成任何文件
Phase 1 (Active)    → 完整流水线启用

流程：
Solutionist（设计）
    ↓ 输出 proposals/、db/、tests/
Coder（后端实现）
    ↓ 在 cod/{feature_id} 分支开发，提 PR
Stylist（前端实现）
    ↓ 在 sty/{feature_id} 分支开发，提 PR
Tester（测试验证）
    ↓ 执行 tests/ 中的用例，通过/失败
    ↓ 失���则回溯到 Coder/Stylist
```

---

## 角色系统

### 7 个核心角色

| 角色 | 职责 | 权限 |
|------|------|------|
| **Architect** | 维护协议文件，设计系统架构 | 只能修改 protocols 仓库 |
| **Principal** | 全局编排，轮询调度，维护 progress.json | 可读所有仓库，可写 governance |
| **Solutionist** | 需求分解、DB 设计、API 规格、测试用例 | 可读 genesis.md，可写 governance |
| **Coder** | 后端业务逻辑实现（Java + Spring Boot） | 可读写 codespace |
| **Stylist** | 前端 UI 实现（Vue3 + TailwindCSS） | 可读写 codespace |
| **Tester** | 自动化测试执行与验证 | 可读 codespace，可写 governance |
| **Observer** | 只读审计，可访问所有资产 | 只读所有仓库 |

### 权限矩阵

```
                genesis.md  progress.json  proposals/  code_repo  protocols_repo
Architect           ✗            ✗            ✗          READ      READ+WRITE
Principal           ✗        READ+WRITE       READ       READ         READ
Solutionist       READ       READ+WRITE   READ+WRITE      ✗          READ
Coder               ✗        READ+WRITE       READ    READ+WRITE     READ
Stylist             ✗        READ+WRITE       READ    READ+WRITE     READ
Tester              ✗        READ+WRITE       READ       READ         READ
Observer          READ          READ          READ       READ         READ
```

---

## 实现要点

### 1. 协议文件设计

**AI.md 示例结构**：
```markdown
# AI 协议入口

当用户输入 #<role> 时：
1. 读取 roles/{role}.md
2. 读取 core_protocol.md
3. 加载对应的 skills
4. 宣告角色激活

支持的角色：
- #architect - 架构师
- #pri - Principal（项目经理）
- #sol - Solutionist（方案设计师）
- #cod - Coder（后端开发）
- #sty - Stylist（前端开发）
- #test - Tester（测试）
- #obs - Observer（审计）
```

**角色文件示例（roles/coder.md）**：
```markdown
# Coder 角色定义

## 使命
实现后端业务逻辑（Java + Spring Boot）

## 权限
- READ: protocols_repo, governance_repo
- READ+WRITE: code_repo

## 工作流
1. 读取 proposals/{feature_id}.md
2. 创建 git worktree: cod/{feature_id}
3. 实现业务逻辑
4. 提交 PR 到 dev
5. 更新 progress.json

## 禁止事项
- 不能读取 genesis.md
- 不能修改 protocols_repo
- 不能直接提交到 dev（必须通过 PR）
```

### 2. Shell 脚本实现

**new_subagent.sh 核心逻辑**：
```bash
#!/bin/bash
WORKSPACE=$1
PROVIDER=$2  # -claude, -codex, -gemini
TASK=$3

# 使用 osascript 在新 Terminal Tab 启动
osascript <<EOF
tell application "Terminal"
    activate
    tell application "System Events"
        keystroke "t" using command down
    end tell
    do script "cd $WORKSPACE && cline $PROVIDER '$TASK'" in front window
end tell
EOF

# 记录到 dispatch_log.jsonl
echo "{\"event\":\"dispatch\",\"timestamp\":\"$(date)\",\"task\":\"$TASK\"}" >> .runtime/dispatch_log.jsonl
```

### 3. 状态同步机制

**progress.json 更新流程**：
```
Sub-agent 启动
  ↓
读取 progress.json
  ↓
更新自己的状态为 "active"
  ↓
git add progress.json
git commit -m "Session start: {session_id}"
git push origin dev
  ↓
...执行任务...
  ↓
更新状态为 "completed"
  ↓
git add progress.json
git commit -m "Session complete: {session_id}"
git push origin dev
```

### 4. Git 分支策略

```
protocols 仓库:
  dev ← Architect 直接提交

governance 仓库:
  dev ← 所有角色直接提交

codespace 仓库:
  dev ← 主分支
  cod/{feature_id} ← Coder worktree
  sty/{feature_id} ← Stylist worktree
  
  工作流:
  worktree → feature branch → PR → dev → (模块完成后) → master
```

---

## 如何复刻

### 最小可行���本（MVP）

**Step 1: 创建三个仓库**
```bash
mkdir my-ai-team
cd my-ai-team

# 创建三个独立的 Git 仓库
mkdir protocols governance codespace
cd protocols && git init && cd ..
cd governance && git init && cd ..
cd codespace && git init && cd ..
```

**Step 2: 创建协议文件**
```bash
cd protocols

# 创建 AI.md
cat > AI.md << 'EOF'
# AI 协议入口

当用户输入 #<role> 时，读取对应的角色文件。

支持的角色：
- #dev - 开发者
- #test - 测试员
- #pm - 项目经理
EOF

# 创建角色文件
mkdir roles
cat > roles/dev.md << 'EOF'
# 开发者角色

## 使命
实现功能代码

## 工作流
1. 读取需求
2. 编写代码
3. 提交 PR
4. 更新状态
EOF
```

**Step 3: 创建治理文件**
```bash
cd ../governance

# 创建 progress.json
cat > progress.json << 'EOF'
{
  "features": {
    "FEAT-001": {
      "dev": {"status": "pending"},
      "test": {"status": "pending"}
    }
  }
}
EOF

# 创建需求文档
cat > requirements.md << 'EOF'
# 项目需求

## FEAT-001: 用户登录
实现用户登录功能
EOF
```

**Step 4: 创建启动脚本**
```bash
cd ../protocols

mkdir scripts
cat > scripts/new_agent.sh << 'EOF'
#!/bin/bash
ROLE=$1
TASK=$2

# 简化版：直接在当前终端启动
echo "=== 启动 $ROLE 角色 ==="
echo "任务: $TASK"
echo "请在新的 Cline 会话中输入: #$ROLE"
EOF

chmod +x scripts/new_agent.sh
```

**Step 5: 测试运行**
```bash
# 在 VS Code 中打开工作区
code my-ai-team

# 启动 Cline，输入：
#dev

# Cline 会读取 protocols/AI.md 和 roles/dev.md
# 然后按照协议工作
```

### 进阶功能

**1. 添加 Sub-agent 自动启动**
- 使用 osascript（macOS）或 PowerShell（Windows）
- 在新终端 Tab 中启动 AI 会话

**2. 添加状态监控**
- 创建 dashboard 脚本读取 progress.json
- 实时显示各角色工作状态

**3. 添加学习系统**
- 创建 `.inception/` 目录
- 每次会话结束后，AI 总结经验写入对应文件
- 下次启动时自动加载历史经验

**4. 添加技能模块**
- 创建 `skills/` 目录
- 每个技能一个 .md 文件
- 角色按需加载技能

### 关键成功因素

1. **协议要清晰** - 每个角色的职责和边界必须明确
2. **状态要同步** - 使用 Git 和 JSON 确保所有 AI 看到相同的状态
3. **流程要简单** - 从最小可行版本开始，逐步增加复杂度
4. **测试要充分** - 先用简单任务测试流程，再处理复杂项目

---

## 学习资源

### 推荐阅读顺序

1. **理解核心概念** - 阅读本文档的"核心概念"部分
2. **研究角色系统** - 理解 7 个角色的职责和权限
3. **分析工作流** - 理解 Sub-agent 启动和 Feature 生命周期
4. **动手实践** - 按照"如何复刻"部分创建 MVP
5. **逐步优化** - 添加进阶功能

### 实践建议

1. **从简单开始** - 先用 2-3 个角色（开发、测试、项目经理）
2. **手动模拟** - 先手动切换角色，理解流程后再自动化
3. **记录经验** - 每次实践后记录遇到的问题和解决方案
4. **迭代改进** - 根据实际��用情况调整协议和流程

---

## 常见问题

**Q: 为什么要分三个仓库？**
A: 分离关注点。协议是规则，治理是状态，代码是产出。独立仓库便于权限控制和版本管理。

**Q: 为什么用 Markdown 而不是代码？**
A: Markdown 更易读易写，AI 理解起来更自然。协议本质是"给 AI 的说明书"。

**Q: 如何确保 AI 遵守协议？**
A: 在每次会话开始时加载协议文件，在 prompt 中明确角色边界。AI 会自我约束。

**Q: 可以用其他 AI 模型吗？**
A: 可以。FinTax 支持 Claude、Codex、Gemini。关键是 AI 要能理解协议文件。

**Q: 适合什么类型的项目？**
A: 适合结构化、模块化的项目（如 Web 应用、API 服务）。不太适合探索性、创意性项目。

---

## 总结

FinTax 架构的核心价值：

1. **可复制** - 通过协议文件，任何人都可以复刻这个系统
2. **可扩展** - 可以添加新角色、新技能、新模块
3. **可审计** - 所有操作都有 Git 记录和 JSON 状态
4. **可学习** - AI 可以从历史经验中学习改进

这是一个将"AI 作为团队成员"的理念落地的实践案例，值得深入研究和借鉴。
