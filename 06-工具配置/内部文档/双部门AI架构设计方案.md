# 双部门 AI 协作架构设计方案

## 架构概览

基于 FinTax 架构理念，设计一个简化的双部门协作系统：

```
用户想法 → 研究部门 → 需求文档 → 实现部门 → 最终产品
```

---

## 一、核心设计理念

### 1. 职责分离
- **研究部门**：专注需求理解、资料研究、方案设计
- **实现部门**：专注代码实现、技术落地

### 2. 协议驱动
- 用 Markdown 文件定义每个角色的行为规则
- 用 JSON 文件记录项目状态和交接信息

### 3. 状态同步
- 使用 Git 仓库作为共享存储
- 使用标准化的文档格式进行部门间交接

---

## 二、仓库结构

### 方案 A：三仓库模式（推荐）

```
my-ai-project/
├── protocols/          # 协议仓库（规则定义）
│   ├── AI.md          # 角色激活入口
│   ├── core_protocol.md
│   └── roles/
│       ├── researcher.md    # 研究员角色
│       ├── analyst.md       # 分析师角色
│       ├── developer.md     # 开发者角色
│       └── coordinator.md   # 协调员角色
│
├── workspace/         # 工作区仓库（需求与状态）
│   ├── ideas/         # 用户原始想法
│   ├── research/      # 研究资料和笔记
│   ├── requirements/  # 最终需求文档
│   ├── status.json    # 项目状态追踪
│   └── handoff.json   # 部门交接记录
│
└── codebase/          # 代码仓库（实现产出）
    ├── src/
    ├── tests/
    └── docs/
```

### 方案 B：单仓库模式（简化版）

```
my-ai-project/
├── .ai/               # AI 协议目录
│   ├── AI.md
│   └── roles/
├── workspace/         # 工作区
│   ├── ideas/
│   ├── research/
│   ├── requirements/
│   └── status.json
└── src/               # 代码目录
```

---

## 三、角色设计

### 研究部门（2 个角色）

#### 1. Researcher（研究员）
**使命**：查找资料、研究技术方案、收集信息

**职责**：
- 根据用户想法搜索相关资料
- 研究现有解决方案和最佳实践
- 整理技术调研报告
- 提出可行性分析

**工作流**：
```
1. 读取 ideas/{idea_id}.md（用户想法）
2. 搜索相关技术资料（使用搜索工具）
3. 撰写 research/{idea_id}_research.md
4. 更新 status.json（research: completed）
5. 通知 Analyst 开始工作
```

**权限**：
- READ: ideas/, requirements/
- WRITE: research/
- UPDATE: status.json

#### 2. Analyst（分析师）
**使命**：与用户对话、完善需求、撰写需求文档

**职责**：
- 基于研究资料与用户深度对话
- 提出问题、澄清需求
- 完善功能设计
- 撰写标准化需求文档

**工作流**：
```
1. 读取 ideas/{idea_id}.md 和 research/{idea_id}_research.md
2. 与用户对话，提出问题和建议
3. 撰写 requirements/{idea_id}_spec.md
4. 更新 status.json（analysis: completed）
5. 触发 handoff 到实现部门
```

**权限**：
- READ: ideas/, research/
- WRITE: requirements/
- UPDATE: status.json, handoff.json

### 实现部门（5 个角色）

#### 3. Principal（项目经理）
**使命**：全局编排、轮询调度、维护项目状态

**职责**：
- 监控项目状态（轮询 status.json）
- 触发角色切换和任务分配
- 管理部门交接
- 维护 status.json 和 handoff.json
- 处理异常情况和冲突

**工作流**：
```
1. 轮询 status.json，检查各阶段状态
2. 根据状态触发下一个角色
3. 记录交接信息到 handoff.json
4. 使用脚本在新终端启动 Sub-agent
5. 监控 Sub-agent 执行状态
6. 处理异常和回溯
```

**权限**：
- READ: 所有目录
- WRITE: status.json, handoff.json

#### 4. Coder（后端开发）
**使命**：实现后端业务逻辑

**职责**：
- 读取需求文档和技术规格
- 实现后端 API 和业务逻辑
- 编写单元测试和集成测试
- 提交 PR 到代码仓库

**工作流**：
```
1. 读取 requirements/{idea_id}_spec.md
2. 创建 git worktree: cod/{idea_id}
3. 实现后端业务逻辑（API、Service、Repository）
4. 编写单元测试（覆盖率 > 80%）
5. 提交 PR 到 dev 分支
6. 更新 status.json（coder: completed）
```

**权限**：
- READ: requirements/, research/
- WRITE: codebase/（通过 worktree 和 PR）
- UPDATE: status.json

#### 5. Stylist（前端开发）
**使命**：实现前端 UI 和交互

**职责**：
- 读取需求文档和 UI 设计
- 实现前端页面和组件
- 对接后端 API
- 编写前端测试

**工作流**：
```
1. 读取 requirements/{idea_id}_spec.md
2. 创建 git worktree: sty/{idea_id}
3. 实现前端页面和组件
4. 对接后端 API
5. 编写前端测试
6. 提交 PR 到 dev 分支
7. 更新 status.json（stylist: completed）
```

**权限**：
- READ: requirements/, research/
- WRITE: codebase/（通过 worktree 和 PR）
- UPDATE: status.json

#### 6. Reviewer（审核员）
**使命**：代码审查、质量把关、架构审核

**职责**：
- 审查 Coder 和 Stylist 提交的 PR
- 检查代码质量、规范性、安全性
- 验证是否符合需求文档
- 提出改进建议或批准合并

**工作流**：
```
1. 读取 PR 和相关需求文档
2. 审查代码质量和规范
3. 检查是否符合需求
4. 运行测试确保通过
5. 提出修改意见或批准 PR
6. 更新 status.json（reviewer: completed）
```

**权限**：
- READ: requirements/, codebase/, research/
- WRITE: review_comments/
- UPDATE: status.json
- APPROVE: PR merge

#### 7. Tester（测试员）
**使命**：自��化测试执行与验证

**职责**：
- 读取需求文档和验收标准
- 执行自动化测试用例
- 验证功能是否符合需求
- 记录测试结果和缺陷

**工作流**：
```
1. 读取 requirements/{idea_id}_spec.md
2. ���行自动化测试用例
3. 验证验收标准
4. 记录测试结果
5. 如果失败，回溯到 Coder/Stylist
6. 如果通过，更新 status.json（tester: completed）
```

**权限**：
- READ: requirements/, codebase/
- WRITE: test_reports/
- UPDATE: status.json

---

## 四、核心文件设计

### 1. status.json（项目状态）

```json
{
  "projects": {
    "IDEA-001": {
      "title": "用户登录功能",
      "stage": "research",
      "created_at": "2026-03-15T15:00:00Z",
      "updated_at": "2026-03-15T15:30:00Z",
      "phases": {
        "research": {
          "status": "active",
          "assigned_to": "researcher",
          "started_at": "2026-03-15T15:00:00Z"
        },
        "analysis": {
          "status": "pending"
        },
        "development": {
          "status": "pending"
        },
        "testing": {
          "status": "pending"
        }
      }
    }
  }
}
```

### 2. handoff.json（交接记录）

```json
{
  "handoffs": [
    {
      "id": "HO-001",
      "project_id": "IDEA-001",
      "from_role": "analyst",
      "to_role": "developer",
      "timestamp": "2026-03-15T16:00:00Z",
      "artifacts": [
        "requirements/IDEA-001_spec.md",
        "research/IDEA-001_research.md"
      ],
      "notes": "需求已确认，可以开始开发"
    }
  ]
}
```

### 3. ideas/{idea_id}.md（用户想法）

```markdown
# IDEA-001: 用户登录功能

## 背景
我需要为我的网站添加用户登录功能

## 初步想法
- 用户可以用邮箱和密码登录
- 支持记住登录状态
- 需要安全性

## 期望
- 简单易用
- 安全可靠
- 响应快速

## 约束
- 预算有限
- 需要在 2 周内完成
```

### 4. requirements/{idea_id}_spec.md（需求文档）

```markdown
# IDEA-001 需求规格说明书

## 1. 功能概述
实现基于邮箱密码的用户登录系统

## 2. 功能需求

### 2.1 用户注册
- 输入：邮箱、密码、确认密码
- 验证：邮箱格式、密码强度（至少 8 位）
- 输出：注册成功/失败消息

### 2.2 用户登录
- 输入：邮箱、密码、记住我（可选）
- 验证：凭证正确性
- 输出：登录成功跳转 / 错误提示

### 2.3 会话管理
- 登录后生成 JWT token
- "记住我"功能：token 有效期 30 天，否则 24 小时

## 3. 技术方案

### 3.1 技术栈
- 后端：Node.js + Express + JWT
- 数据库：PostgreSQL
- 加密：bcrypt

### 3.2 API 设计
```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET /api/auth/me
```

## 4. 数据模型

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 5. 安全要求
- 密码使用 bcrypt 加密（salt rounds: 10）
- JWT secret 存储在环境变量
- 实施速率限制（登录：5 次/分钟）

## 6. 验收标准
- [ ] 用户可以成功注册
- [ ] 用户可以用正确凭证登录
- [ ] 错误凭证会被拒绝
- [ ] "记住我"功能���常工作
- [ ] 所有 API 有单元测试
```

---

## 五、工作流程

### 完整流程图

```
用户输入想法
    ↓
创建 ideas/{id}.md
    ↓
更新 status.json (stage: research)
    ↓
[研究部门]
    ↓
Researcher 启动
    ↓
查找资料、技术调研
    ↓
撰写 research/{id}_research.md
    ↓
更新 status.json (research: completed)
    ↓
Analyst 启动
    ↓
读取研究资料
    ↓
与用户对话、完善需求
    ↓
撰写 requirements/{id}_spec.md
    ↓
更新 status.json (analysis: completed)
    ↓
记录 handoff.json
    ↓
[实现部门]
    ↓
Developer 启动
    ↓
读取需求文档
    ↓
实现功能代码
    ↓
提交 PR
    ↓
更新 status.json (development: completed)
    ↓
完成 ✓
```

### 角色切换机制

#### 方式 1：手动切换（简单）
```bash
# 用户手动输入命令切换角色
#researcher    # 启动研究员
#analyst       # 启动分析师
#developer     # 启动开发者
```

#### 方式 2：自动调度（进阶）
```bash
# Coordinator 轮询 status.json
#coord -poll

# 检测到 research completed，自动启动 Analyst
# 使用脚本在新终端启动
./scripts/start_agent.sh analyst IDEA-001
```

---

## 六、协议文件示例

### AI.md（角色激活入口）

```markdown
# AI 协议入口

## 角色激活

当用户输入 `#<role>` 时：
1. 读取 `roles/{role}.md`
2. 读取 `core_protocol.md`
3. 加载角色定义
4. 宣告角色激活

## 支持的角色

### 研究部门
- `#researcher` - 研究员（技术调研）
- `#analyst` - 分析师（需求分析）

### 实现部门
- `#pri` - Principal（项目经理/全局调度）
- `#cod` - Coder（后端开发）
- `#sty` - Stylist（前端开发）
- `#rev` - Reviewer（代码审核员）
- `#test` - Tester（测试员）

## 使用示例

```bash
# 启动研究员角色
#researcher

# 启动分析师角色，处理特定项目
#analyst IDEA-001

# 启动开发者角色
#developer IDEA-001
```
```

### roles/researcher.md（研究员角���）

```markdown
# Researcher 角色定义

## 使命
查找资料、研究技术方案、收集信息

## 权限
- READ: ideas/, requirements/
- WRITE: research/
- UPDATE: status.json

## 工作流

### Step 1: 读取用户想法
```bash
读取 ideas/{idea_id}.md
理解用户的初步想法和需求
```

### Step 2: 技术调研
- 搜索相关技术方案
- 研究最佳实践
- 查找类似案例
- 评估可行性

### Step 3: 撰写研究报告
创建 `research/{idea_id}_research.md`，包含：
- 技术方案对比
- 推荐方案及理由
- 潜在风险和挑战
- 参考资料链接

### Step 4: 更新状态
```json
{
  "phases": {
    "research": {
      "status": "completed",
      "completed_at": "2026-03-15T16:00:00Z"
    }
  }
}
```

### Step 5: 通知下一角色
在终端输出：
```
[RESEARCH COMPLETED]
Project: IDEA-001
Next: #analyst IDEA-001
```

## 输出规范

### research/{idea_id}_research.md 模板
```markdown
# {项目标题} - 技术调研报告

## 1. 需求理解
（简述用户需求）

## 2. 技术方案

### 方案 A: {方案名称}
- 优点：
- 缺点：
- 适用场景：

### 方案 B: {方案名称}
- 优点：
- 缺点：
- 适用场景：

## 3. 推荐方案
（说明推荐理由）

## 4. 技术栈建议
- 后端：
- 前端：
- 数据库：
- 其他：

## 5. 潜在风险
- 风险 1：
- 风险 2：

## 6. 参考资料
- [链接 1](url)
- [链接 2](url)
```

## 禁止事项
- ❌ 不能直接编写代码
- ❌ 不能修改 requirements/ 目录
- ❌ 不能跳过调研直接给结论
- ❌ 不能修改用户的原始想法文件
```

### roles/analyst.md（分析师角色）

```markdown
# Analyst 角色定义

## 使命
与用户对话、完善需求、撰写需求文档

## 权限
- READ: ideas/, research/
- WRITE: requirements/
- UPDATE: status.json, handoff.json

## 工作流

### Step 1: 准备工作
```bash
读取 ideas/{idea_id}.md
读取 research/{idea_id}_research.md
理解用户想法和技术调研结果
```

### Step 2: 与用户对话
提出关键问题，例如：
- "根据调研，我们有 A 和 B 两种方案，您更倾向哪种？"
- "关于 {功能点}，您期望的具体行为是？"
- "是否有性能/安全/预算方面的特殊要求？"

### Step 3: 完善需求
基于对话结果，明确：
- 功能范围
- 技术选型
- 验收标准
- 时间预算

### Step 4: 撰写需求文档
创建 `requirements/{idea_id}_spec.md`，包含：
- 功能概述
- 详细需求
- 技术方案
- 数据模型
- API 设计
- 验收标准

### Step 5: 确认需求
向用户展示需求文档，询问：
"我已经整理了完整的需求文档，请确认是否符合您的期望？"

### Step 6: 交接到实现部门
```bash
更新 status.json (analysis: completed)
记录 handoff.json
通知：#developer {idea_id}
```

## 输出规范

### requirements/{idea_id}_spec.md 模板
（见前文"核心文件设计"部分）

## 对话技巧
- ✅ 提出具体的选择题，而非开放式问题
- ✅ 基于调研结果给出专业建议
- ✅ 用简单语言解释技术概念
- ✅ 确认关键决策点
- ✅ 记录所有重要对话内容

## 禁止事项
- ❌ 不能编写代码
- ❌ 不能修改研究报告
- ❌ 不能在需求不明确时强行推进
- ❌ 不能忽略用户的反馈
```

### roles/developer.md（开发者角色）

```markdown
# Developer 角色定义

## 使命
根据需求文档实现功能代码

## 权限
- READ: requirements/, research/
- WRITE: codebase/
- UPDATE: status.json

## 工作流

### Step 1: 读取需求
```bash
读取 requirements/{idea_id}_spec.md
理解功能需求和技术方案
如有疑问，向 Analyst 提问
```

### Step 2: 创建分支
```bash
cd codebase
git checkout -b feature/{idea_id}
```

### Step 3: 实现功能
按照需求文档：
- 设计代码结构
- 实现业务逻辑
- 编写单元测试
- 添加必要注释

### Step 4: 自测
- 运行所有测试
- 手动测试关键功能
- 检查代码质量

### Step 5: 提交代码
```bash
git add .
git commit -m "feat: implement {feature_name} (IDEA-001)"
git push origin feature/{idea_id}
```

### Step 6: 创建 PR
- 描述实现内容
- 关联需求文档
- 请求 code review

### Step 7: 更新状态
```json
{
  "phases": {
    "development": {
      "status": "completed",
      "pr_url": "https://github.com/.../pull/123",
      "completed_at": "2026-03-15T18:00:00Z"
    }
  }
}
```

## 代码规范
- 遵循项目现有代码风格
- 函数/类命名清晰
- 关键逻辑添加注释
- 测试覆盖率 > 80%

## 禁止事项
- ❌ 不能修改需求文档
- ❌ 不能跳过测试
- ❌ 不能直接提交到主分支
- ❌ 不能实现需求外的功能
```

---

## 七、实施步骤

### MVP 版本（最小可行）

#### 第 1 步：创建仓库结构
```bash
mkdir my-ai-project
cd my-ai-project

# 创建目录
mkdir -p .ai/roles
mkdir -p workspace/{ideas,research,requirements}
mkdir -p src

# 初始化 Git
git init
```

#### 第 2 步：创建协议文件
```bash
# 创建 AI.md
cat > .ai/AI.md << 'EOF'
# AI 协议入口
（复制前文的 AI.md 内容）
EOF

# 创建角色文件
cat > .ai/roles/researcher.md << 'EOF'
（复制前文的 researcher.md 内容）
EOF

cat > .ai/roles/analyst.md << 'EOF'
（复制前文的 analyst.md 内容）
EOF

cat > .ai/roles/developer.md << 'EOF'
（复制前文的 developer.md 内容）
EOF
```

#### 第 3 步：创建状态文件
```bash
cat > workspace/status.json << 'EOF'
{
  "projects": {},
  "last_updated": "2026-03-15T15:00:00Z"
}
EOF

cat > workspace/handoff.json << 'EOF'
{
  "handoffs": []
}
EOF
```

#### 第 4 步：创建第一个想法
```bash
cat > workspace/ideas/IDEA-001.md << 'EOF'
# IDEA-001: 待办事项应用

## 背景
我需要一个简单的待办事项管理应用

## 初步想法
- 可以添加、删除、完成待办事项
- 数据持久化存储
- 简洁的界面

## 期望
- 快速开发
- 易于使用
EOF
```

#### 第 5 步：测试运行
```bash
# 在 VS Code 中打开项目
code .

# 启动 Cline，输入：
#researcher IDEA-001

# Researcher 会：
# 1. 读取 IDEA-001.md
# 2. 进行技术调研
# 3. 撰写 research/IDEA-001_research.md
# 4. 更新 status.json
```

### 进阶功能

#### 1. 自动角色切换
创建 `scripts/start_agent.sh`：
```bash
#!/bin/bash
ROLE=$1
PROJECT_ID=$2

# 在新终端启动 AI 会话
osascript <<EOF
tell application "Terminal"
    activate
    tell application "System Events"
        keystroke "t" using command down
    end tell
    do script "cd $(pwd) && cline '#$ROLE $PROJECT_ID'" in front window
end tell
EOF
```

#### 2. 状态监控面板
创建 `scripts/status.sh`：
```bash
#!/bin/bash
echo "=== 项目状态 ==="
cat workspace/status.json | jq '.projects'
```

#### 3. 交接通知
在 Analyst 完成时自动通知：
```bash
echo "[HANDOFF] IDEA-001: analysis → development"
echo "Run: #developer IDEA-001"
```

---

## 八、使用示例

### 场景：开发一个用户登录功能

#### 1. 用户创建想法
```bash
# 创建 workspace/ideas/IDEA-002.md
# IDEA-002: 用户登录功能
我需要为网站添加用户登录...
```

#### 2. 启动研究员
```bash
用户输入：#researcher IDEA-002

Researcher 输出：
[ROLE ACTIVATED]: Researcher
[PROJECT]: IDEA-002
[TASK]: 技术调研

正在读取用户想法...
开始技术调研...

（搜索相关���料）
（分析技术方案）

已完成调研报告：workspace/research/IDEA-002_research.md

[RESEARCH COMPLETED]
Next: #analyst IDEA-002
```

#### 3. 启动分析师
```bash
用户输入：#analyst IDEA-002

Analyst 输出：
[ROLE ACTIVATED]: Analyst
[PROJECT]: IDEA-002
[TASK]: 需求分析

已读取：
- ideas/IDEA-002.md
- research/IDEA-002_research.md

根据调研，我有几个问题：

1. 您希望支持哪些登录方式？
   A. 仅邮箱密码
   B. 邮箱密码 + 第三方登录（Google/GitHub）
   C. 手机号验证码

2. 关于会话管理，您的偏好是？
   A. 短期会话（24小时）
   B. 长期会话（30天）
   C. 可选"记住我"

（用户回答问题）

好的，我已经理解您的需求。正在撰写需求文档...

已完成需求文档：workspace/requirements/IDEA-002_spec.md

请确认需求文档是否符合您的期望？

（用户确认）

[ANALYSIS COMPLETED]
[HANDOFF] research + analysis → development
Next: #developer IDEA-002
```

#### 4. 启动开发者
```bash
用户输入：#developer IDEA-002

Developer 输出：
[ROLE ACTIVATED]: Developer
[PROJECT]: IDEA-002
[TASK]: 功能实现

已读取需求文档：requirements/IDEA-002_spec.md

开始实现...

1. 创建分支：feature/IDEA-002
2. 实现用户模型
3. 实现认证逻辑
4. 编写单元测试
5. 提交代码

[DEVELOPMENT COMPLETED]
PR: https://github.com/.../pull/123
```

---

## 九、关键成功因素

### 1. 清晰的职责边界
- 研究员只做调研，不写需求
- 分析师只写需求，不写代码
- 开发者只写代码，不改需求

### 2. 标准化的文档格式
- 每个阶���的输出都有固定模板
- 便于下一角色理解和使用

### 3. 完善的状态管理
- status.json 记录每个阶段的状态
- handoff.json 记录交接信息
- 所有角色都能看到全局进度

### 4. 灵活的扩展性
- 可以添加新角色（如 Reviewer、Tester）
- 可以添加新阶段（如 Design、Deployment）
- 可以自定义工作流

---

## 十、与 FinTax 的对比

| 维度 | FinTax | 双部门架构 |
|------|--------|-----------|
| 角色数量 | 7 个 | 7 个 |
| 仓库数量 | 3 个 | 1-3 个（可选） |
| 复杂度 | 高 | 中 |
| 适用场景 | 大型项目 | 中小型项目 |
| 学习曲线 | 陡峭 | 平缓 |
| 自动化程度 | 高 | 中（可扩展） |

---

## 十一、下一步行动

### 立即可做
1. ✅ 创建基础目录结构
2. ✅ 编写 3-4 个核心角色文件
3. ✅ 创建第一个测试项目
4. ✅ 手动运行完整流程

### 短期优化
1. 添加自动角色切换脚本
2. 完善文档模板
3. 添加状态监控工具
4. 优化交接流程

### 长期扩展
1. 添加更多角色（Reviewer、Tester、Deployer）
2. 实现完全自动化调度
3. 添加学习系统（.inception/）
4. 集成 CI/CD 流程

---

## 总结

这个双部门架构是 FinTax 的简化版本，保留了核心理念：
- **职责分离**：研究和实现分开
- **协议驱动**：用 Markdown 定义规则
- **状态同步**：用 JSON 和 Git 管理状态

相比 FinTax，它更简单、更易上手，适合个人或小团队使用。

**核心价值**：
1. 让 AI 专注于特定任务，提高质量
2. 标准化流程，减少混乱
3. 可追溯、可审计、可复现
4. 易于扩展和定制
