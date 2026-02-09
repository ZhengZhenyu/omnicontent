# OmniContent Git 工作流规范

本文档定义了 OmniContent 项目的 Git 分支管理策略、提交规范和协作流程，适用于 4 人并行开发的场景。

---

## 一、分支管理策略

### 1.1 分支结构（简化版 Git Flow）

```
main（生产分支，受保护）
  ↑ 定期合并
develop（开发主分支，受保护）
  ↑ PR 合并
  ├── feature/security-oauth-integration          # 角色1: 安全域专家
  ├── feature/content-batch-upload                 # 角色2: 内容与发布域专家
  ├── feature/governance-committee-management      # 角色3: 治理域专家
  └── feature/infra-analytics-dashboard            # 角色4: 平台与基础设施专家
```

### 1.2 分支类型说明

| 分支类型 | 用途 | 命名规范 | 生命周期 | 可以合并到 |
|---------|------|---------|---------|-----------|
| **main** | 生产环境代码 | `main` | 永久 | - |
| **develop** | 开发主分支 | `develop` | 永久 | main |
| **feature** | 功能开发 | `feature/<domain>-<description>` | 临时 | develop |
| **bugfix** | Bug 修复 | `bugfix/<issue-id>-<description>` | 临时 | develop |
| **hotfix** | 紧急修复 | `hotfix/<issue-id>-<description>` | 临时 | main, develop |
| **release** | 发布准备 | `release/v<version>` | 临时 | main, develop |

### 1.3 分支命名约定

#### Feature 分支命名（功能开发）
```bash
# 格式：feature/<domain>-<description>
# <domain>: security | content | governance | infra

# 角色1（安全域）示例
feature/security-oauth-integration
feature/security-password-policy
feature/security-audit-log

# 角色2（内容与发布域）示例
feature/content-batch-upload
feature/content-markdown-editor
feature/publish-wechat-image

# 角色3（治理域）示例
feature/governance-committee-crud
feature/governance-meeting-calendar
feature/governance-member-import

# 角色4（基础设施域）示例
feature/infra-analytics-dashboard
feature/infra-notification-service
feature/infra-database-migration
```

#### Bugfix 分支命名（Bug 修复）
```bash
# 格式：bugfix/<issue-id>-<description>

bugfix/123-login-token-expiry
bugfix/456-content-duplicate-save
bugfix/789-meeting-reminder-timezone
```

#### Hotfix 分支命名（紧急修复）
```bash
# 格式：hotfix/<issue-id>-<description>

hotfix/999-security-xss-vulnerability
hotfix/888-database-connection-leak
```

#### Release 分支命名（版本发布）
```bash
# 格式：release/v<major>.<minor>.<patch>

release/v1.0.0
release/v1.1.0
release/v1.2.1
```

---

## 二、分支工作流

### 2.1 Feature 分支开发流程

#### 步骤 1：从 develop 创建功能分支
```bash
# 1. 切换到 develop 分支并拉取最新代码
git checkout develop
git pull origin develop

# 2. 创建新的功能分支
git checkout -b feature/security-oauth-integration

# 3. 推送到远程（可选，建议首次创建时推送）
git push -u origin feature/security-oauth-integration
```

#### 步骤 2：开发过程中定期同步 develop
```bash
# 方法 1：使用 rebase（推荐，保持线性历史）
git checkout develop
git pull origin develop
git checkout feature/security-oauth-integration
git rebase develop

# 如果遇到冲突，解决后继续
git add <解决冲突的文件>
git rebase --continue

# 方法 2：使用 merge（适合复杂冲突场景）
git checkout feature/security-oauth-integration
git merge develop
```

**建议同步频率**：
- 每天开始工作前同步一次
- 提交 PR 前必须同步
- develop 有重大变更时立即同步

#### 步骤 3：提交代码（遵循 Commit Message 规范）
```bash
# 查看变更
git status
git diff

# 添加文件到暂存区（推荐逐文件添加，避免误提交）
git add backend/app/api/auth.py
git add backend/app/schemas/auth.py
git add backend/tests/test_auth_api.py

# 提交（使用规范的 commit message）
git commit -m "feat(auth): add OAuth login endpoints

- Add Google OAuth integration
- Add GitHub OAuth integration
- Add tests for OAuth flow
- Update API documentation

Refs: #123"

# 推送到远程
git push origin feature/security-oauth-integration
```

#### 步骤 4：创建 Pull Request
```bash
# 使用 GitHub CLI（推荐）
gh pr create \
  --base develop \
  --head feature/security-oauth-integration \
  --title "feat(auth): add OAuth login endpoints" \
  --body "$(cat <<'EOF'
## 概述
实现 OAuth 第三方登录功能，支持 Google 和 GitHub。

## 变更内容
- ✅ 添加 OAuth 认证端点（`/api/auth/oauth/{provider}`）
- ✅ 集成 Google OAuth 2.0
- ✅ 集成 GitHub OAuth 2.0
- ✅ 更新用户模型添加 `oauth_provider` 字段
- ✅ 添加单元测试（覆盖率 85%）
- ✅ 更新 API 文档

## 测试
```bash
pytest backend/tests/test_auth_api.py::test_oauth_login -v
```

## 截图
![OAuth Login Flow](docs/images/oauth-flow.png)

## 依赖
需要设置环境变量：
- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- `GITHUB_OAUTH_CLIENT_ID`
- `GITHUB_OAUTH_CLIENT_SECRET`

## 检查清单
- [x] 代码通过 linter 检查
- [x] 测试覆盖率 ≥ 80%
- [x] API 文档已更新
- [x] 没有硬编码的敏感信息
- [x] 遵循项目代码规范

## 相关 Issue
Closes #123

EOF
)" \
  --reviewer security-reviewer,infra-lead
```

#### 步骤 5：代码审查与合并
```bash
# 审查通过后，由维护者或自己合并（需要权限）
# 推荐使用 Squash and Merge 保持 develop 分支整洁

# 合并后删除功能分支
git checkout develop
git pull origin develop
git branch -d feature/security-oauth-integration
git push origin --delete feature/security-oauth-integration
```

### 2.2 Bugfix 分支流程

```bash
# 1. 从 develop 创建 bugfix 分支
git checkout develop
git pull origin develop
git checkout -b bugfix/123-login-token-expiry

# 2. 修复 bug 并提交
git add <修复的文件>
git commit -m "fix(auth): resolve token expiry issue

Token expiration was not properly validated in JWT middleware.
Now correctly checks exp claim and returns 401 for expired tokens.

Fixes: #123"

# 3. 推送并创建 PR
git push origin bugfix/123-login-token-expiry
gh pr create --base develop --head bugfix/123-login-token-expiry \
  --title "fix(auth): resolve token expiry issue" \
  --label bug --label priority:high
```

### 2.3 Hotfix 分支流程（紧急修复）

```bash
# 1. 从 main 创建 hotfix 分支
git checkout main
git pull origin main
git checkout -b hotfix/999-security-xss-vulnerability

# 2. 修复并提交
git add <修复的文件>
git commit -m "fix(security): patch XSS vulnerability in content preview

Sanitize user input before rendering in preview component.
Add CSP headers to prevent inline script execution.

SECURITY: CVE-2024-XXXX
Fixes: #999"

# 3. 推送并创建 PR 到 main
git push origin hotfix/999-security-xss-vulnerability
gh pr create --base main --head hotfix/999-security-xss-vulnerability \
  --title "fix(security): patch XSS vulnerability" \
  --label security --label priority:critical

# 4. 合并到 main 后，也要合并到 develop
gh pr create --base develop --head hotfix/999-security-xss-vulnerability \
  --title "fix(security): patch XSS vulnerability (backport to develop)"
```

### 2.4 Release 分支流程（版本发布）

```bash
# 1. 从 develop 创建 release 分支
git checkout develop
git pull origin develop
git checkout -b release/v1.1.0

# 2. 更新版本号和 CHANGELOG
# 编辑 backend/app/__init__.py 更新 __version__
# 编辑 frontend/package.json 更新 version
# 编辑 CHANGELOG.md 添加发布说明

git add backend/app/__init__.py frontend/package.json CHANGELOG.md
git commit -m "chore(release): bump version to v1.1.0"

# 3. 推送并创建 PR 到 main
git push origin release/v1.1.0
gh pr create --base main --head release/v1.1.0 \
  --title "Release v1.1.0" \
  --label release

# 4. 合并到 main 后打 tag
git checkout main
git pull origin main
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0

# 5. 将 release 分支也合并回 develop
gh pr create --base develop --head release/v1.1.0 \
  --title "Merge release v1.1.0 back to develop"
```

---

## 三、Commit Message 规范

### 3.1 格式要求

```
<type>(<scope>): <subject>

<body>

<footer>
```

**示例**：
```
feat(governance): add committee member CSV import

- Implement CSV file parser with validation
- Add batch import API endpoint
- Handle duplicate entries gracefully
- Update frontend with upload component

Refs: #234
```

### 3.2 Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| **feat** | 新功能 | `feat(content): add markdown editor` |
| **fix** | Bug 修复 | `fix(auth): resolve JWT token refresh issue` |
| **docs** | 文档变更 | `docs(api): update authentication endpoints` |
| **style** | 代码格式（不影响逻辑） | `style(frontend): format with prettier` |
| **refactor** | 重构（既不是新功能也不是 bug 修复） | `refactor(services): extract common upload logic` |
| **perf** | 性能优化 | `perf(database): add index on content.created_at` |
| **test** | 测试相关 | `test(auth): add unit tests for password reset` |
| **chore** | 构建/工具/依赖更新 | `chore(deps): upgrade FastAPI to 0.110.0` |
| **ci** | CI/CD 配置变更 | `ci(github): add codecov integration` |
| **revert** | 回滚 commit | `revert: feat(governance): remove meeting export` |

### 3.3 Scope 范围

根据 4 人分工的业务域定义：

| Scope | 说明 | 负责人 |
|-------|------|--------|
| **auth** | 认证与授权 | 角色1 |
| **security** | 安全相关 | 角色1 |
| **content** | 内容管理 | 角色2 |
| **publish** | 多渠道发布 | 角色2 |
| **community** | 社区管理 | 角色3 |
| **governance** | 治理模块（委员会/会议） | 角色3 |
| **analytics** | 数据分析 | 角色4 |
| **infra** | 基础设施 | 角色4 |
| **notification** | 通知服务 | 角色4 |
| **database** | 数据库 | 角色4 |
| **ci** | CI/CD | 角色4 |
| **docs** | 文档 | 所有人 |
| **deps** | 依赖管理 | 所有人 |

### 3.4 Subject 和 Body 编写规则

**Subject（主题行）**：
- 使用英文，首字母小写
- 使用祈使句（动词原形开头）：`add`, `fix`, `update`, `remove`
- 不超过 50 个字符
- 不以句号结尾

**Body（正文）**：
- 详细说明 **做了什么** 和 **为什么**
- 使用项目符号列表
- 每行不超过 72 个字符
- 可以包含代码片段或示例

**Footer（脚注）**：
- 关联 Issue：`Refs: #123` 或 `Closes: #123`
- Breaking Changes：`BREAKING CHANGE: <description>`
- 安全问题：`SECURITY: CVE-2024-XXXX`

### 3.5 使用 Claude Code 生成 Commit Message

```bash
# 在 Claude Code 中使用以下提示词：
"请根据以下 git diff 生成一个符合规范的 commit message：
<粘贴 git diff 输出>

要求：
1. 使用 conventional commits 格式
2. type 和 scope 根据变更内容选择
3. subject 简洁明了（<50字符）
4. body 列出主要变更点
5. 如果修复了 bug，添加 Fixes: #issue-id"
```

---

## 四、Pull Request 规范

### 4.1 PR 标题规范

PR 标题应与主要 commit message 保持一致：
```
<type>(<scope>): <description>
```

示例：
- `feat(governance): add committee member CSV import`
- `fix(auth): resolve JWT token refresh race condition`
- `refactor(content): extract markdown conversion service`

### 4.2 PR 描述模板

GitHub PR 描述应包含以下部分：

```markdown
## 概述
简要说明这个 PR 的目的和背景。

## 变更内容
- ✅ 变更点 1
- ✅ 变更点 2
- ✅ 变更点 3

## 测试
描述如何测试这些变更：
\`\`\`bash
pytest backend/tests/test_xxx.py -v
\`\`\`

## 截图（如适用）
![Feature Screenshot](url)

## 依赖 / Breaking Changes
列出新的依赖项或不兼容变更。

## 检查清单
- [ ] 代码通过 linter 检查
- [ ] 测试覆盖率 ≥ 80%
- [ ] API 文档已更新
- [ ] 没有硬编码的敏感信息
- [ ] 遵循项目代码规范
- [ ] 已同步 develop 分支最新代码

## 相关 Issue
Closes #123
Refs #456
```

### 4.3 PR 审查要求

#### 必须审查人分配规则

| 变更范围 | 必须审查人 | 可选审查人 |
|---------|-----------|-----------|
| 认证/权限相关 | 角色1（安全域专家） | 角色4（安全审计） |
| 内容/发布相关 | 角色2（内容与发布域专家） | 角色1（权限部分） |
| 治理模块相关 | 角色3（治理域专家） | 角色1（权限部分） |
| 数据库/基础设施 | 角色4（平台与基础设施专家） | 所有人 |
| 跨域变更 | 至少 2 人 | - |
| 安全漏洞修复 | 角色1 + 角色4 | - |

#### PR 审查检查清单

**功能性审查**：
- [ ] 代码逻辑正确，实现了需求
- [ ] 边界条件和错误处理完善
- [ ] 没有明显的性能问题
- [ ] 数据库查询优化（避免 N+1 查询）

**安全性审查**：
- [ ] 没有 SQL 注入风险
- [ ] 没有 XSS 漏洞
- [ ] 敏感数据已加密
- [ ] 权限验证正确
- [ ] 输入验证充分

**可维护性审查**：
- [ ] 代码结构清晰，易于理解
- [ ] 变量和函数命名有意义
- [ ] 复杂逻辑有注释
- [ ] 没有重复代码（DRY 原则）
- [ ] 遵循项目代码规范

**测试审查**：
- [ ] 测试覆盖率 ≥ 80%
- [ ] 测试用例覆盖主要场景
- [ ] 测试用例可读性好
- [ ] 集成测试通过

**文档审查**：
- [ ] API 文档已更新
- [ ] README 已更新（如适用）
- [ ] CHANGELOG.md 已更新
- [ ] 代码注释充分

### 4.4 PR 合并策略

**推荐使用 Squash and Merge**：
- 保持 develop 和 main 分支历史整洁
- 将多个 commit 合并为一个有意义的 commit
- 合并时的 commit message 应遵循规范

**何时使用 Rebase and Merge**：
- Feature 分支只有少量高质量 commit
- 想保留详细的开发历史

**禁止使用 Merge Commit**：
- 会产生大量无意义的 merge commit
- 使分支历史混乱

---

## 五、代码审查（Code Review）流程

### 5.1 使用 Claude Code 辅助 Code Review

```bash
# 1. 拉取 PR 分支
gh pr checkout 123

# 2. 让 Claude Code 分析变更
"请审查这次 PR (#123) 的代码变更，重点检查：
1. 是否有安全漏洞（SQL 注入、XSS、权限绕过）
2. 是否符合项目代码规范
3. 测试覆盖是否充分（应 ≥ 80%）
4. 是否有潜在的性能问题
5. 数据库查询是否优化
6. 错误处理是否完善

请逐文件分析并给出具体建议。"

# 3. 运行测试和 linter
cd backend
pytest --cov=app --cov-report=term-missing
black --check app/
flake8 app/

cd ../frontend
npm run lint
npm run type-check

# 4. 在 GitHub 上提交 Review 意见
gh pr review 123 --comment -b "整体代码质量不错，有几点建议：
1. backend/app/api/auth.py:45 - 建议添加速率限制
2. frontend/src/views/Login.vue:120 - 密码输入框应禁用自动完成
3. tests/test_auth_api.py - 建议添加 OAuth 失败场景的测试

其他部分 LGTM！"

# 或者批准 PR
gh pr review 123 --approve -b "LGTM! 代码质量高，测试覆盖充分。"

# 或者请求变更
gh pr review 123 --request-changes -b "需要修复安全问题后再合并。"
```

### 5.2 Code Review 响应时间

| PR 优先级 | 响应时间 | 审查完成时间 |
|----------|---------|-------------|
| Critical（hotfix） | 30 分钟 | 2 小时 |
| High（bug、阻塞性功能） | 2 小时 | 4 小时 |
| Medium（常规功能） | 4 小时 | 1 工作日 |
| Low（文档、重构） | 1 工作日 | 2 工作日 |

### 5.3 处理 Review 意见

```bash
# 1. 根据审查意见修改代码
git add <修改的文件>
git commit -m "refactor(auth): address code review feedback

- Add rate limiting to login endpoint
- Disable autocomplete on password input
- Add OAuth failure test cases

Co-authored-by: Reviewer Name <reviewer@example.com>"

# 2. 推送更新
git push origin feature/security-oauth-integration

# 3. 回复 Review 评论
gh pr comment 123 --body "已根据建议进行修改：
✅ 添加了登录接口的速率限制（5次/分钟）
✅ 密码输入框已禁用自动完成
✅ 补充了 OAuth 失败场景测试（覆盖率提升至 88%）

请再次审查，谢谢！"
```

---

## 六、冲突解决策略

### 6.1 预防冲突的最佳实践

1. **频繁同步 develop 分支**
```bash
# 每天开始工作前
git checkout develop && git pull origin develop
git checkout feature/your-branch && git rebase develop
```

2. **小步提交，频繁推送**
```bash
# 每完成一个小功能就提交，避免大量变更积累
git add <files>
git commit -m "feat(scope): small incremental change"
git push origin feature/your-branch
```

3. **遵循文件所有权原则**
- 参考 `docs/OWNERSHIP.md` 明确的文件责任划分
- 不要随意修改他人负责的文件
- 跨域变更需要提前沟通

4. **使用 Feature Toggle 隔离未完成功能**
```python
# backend/app/config.py
class Settings(BaseSettings):
    ENABLE_OAUTH_LOGIN: bool = False
    ENABLE_COMMITTEE_CSV_IMPORT: bool = False
```

### 6.2 解决 Merge 冲突

#### 场景 1：rebase 时出现冲突
```bash
# 1. rebase 时遇到冲突
git rebase develop
# Auto-merging backend/app/api/auth.py
# CONFLICT (content): Merge conflict in backend/app/api/auth.py

# 2. 查看冲突文件
git status

# 3. 手动解决冲突（编辑文件，删除冲突标记）
# <<<<< HEAD
# 你的代码
# =====
# develop 分支的代码
# >>>>> develop

# 4. 标记冲突已解决
git add backend/app/api/auth.py

# 5. 继续 rebase
git rebase --continue

# 6. 如果冲突太复杂，可以中止 rebase
git rebase --abort
```

#### 场景 2：使用 Claude Code 辅助解决冲突
```bash
# 1. 让 Claude Code 分析冲突
"我在 rebase 时遇到冲突，文件是 backend/app/api/auth.py。
以下是冲突内容：
<<<<< HEAD
def login(username: str, password: str):
    user = get_user_by_username(username)
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401)
=====
def login(credentials: LoginCredentials):
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise AuthenticationError()
>>>>> develop

请帮我合并这两个版本的代码，保留两边的改进。"

# 2. Claude Code 会给出合并建议
# 3. 应用建议并继续 rebase
git add backend/app/api/auth.py
git rebase --continue
```

### 6.3 复杂冲突的处理流程

```bash
# 1. 如果 rebase 冲突过多，考虑使用 merge
git rebase --abort
git merge develop

# 2. 或者重新创建分支（适用于冲突太复杂的情况）
git checkout develop
git pull origin develop
git checkout -b feature/security-oauth-integration-v2
git cherry-pick <commit-hash-1>
git cherry-pick <commit-hash-2>
# 逐个应用原分支的 commit

# 3. 提前沟通避免冲突
# 在团队群里发消息：
"我正在修改 backend/app/core/security.py 添加 OAuth 功能，
预计今天下午完成，如果有人也要修改这个文件，请协调一下时间。"
```

---

## 七、分支保护规则

### 7.1 protected 分支（main 和 develop）

在 GitHub 仓库设置中配置以下保护规则：

**main 分支保护**：
- ✅ Require pull request before merging
  - Require approvals: 2
  - Dismiss stale pull request approvals when new commits are pushed
- ✅ Require status checks to pass before merging
  - backend-ci
  - frontend-ci
  - codecov/patch (if configured)
- ✅ Require branches to be up to date before merging
- ✅ Require conversation resolution before merging
- ✅ Do not allow bypassing the above settings
- ✅ Restrict who can push to matching branches
  - 只允许 Maintainers

**develop 分支保护**：
- ✅ Require pull request before merging
  - Require approvals: 1
- ✅ Require status checks to pass before merging
  - backend-ci
  - frontend-ci
- ✅ Require conversation resolution before merging
- ✅ Allow force pushes: Everyone (仅限 develop，便于 rebase)

### 7.2 禁止的 Git 操作

**永远不要在 main 或 develop 上执行**：
```bash
# ❌ 直接提交到受保护分支
git checkout main
git commit -m "quick fix"  # 禁止！

# ❌ Force push 到 main（会破坏历史）
git push --force origin main  # 禁止！

# ❌ 在 main 上执行 reset
git reset --hard HEAD~1  # 禁止！

# ❌ 在 main 上删除他人的 commit
git rebase -i HEAD~5  # 禁止！
```

**允许的操作**：
```bash
# ✅ 在自己的 feature 分支上 force push（rebase 后）
git push --force-with-lease origin feature/your-branch

# ✅ 在 develop 上执行 rebase（需要权限）
git checkout develop
git rebase main
git push --force-with-lease origin develop
```

---

## 八、常见场景和最佳实践

### 8.1 场景：需要修改他人负责的文件

```bash
# 1. 先在团队群或 Issue 中沟通
"@content-lead 我在开发发布功能时需要修改 backend/app/models/content.py
添加一个 last_published_at 字段，可以吗？"

# 2. 等待确认后再修改
# 3. 创建 PR 时 @相关负责人作为审查者
gh pr create --reviewer content-lead

# 4. 或者让负责人来修改，你等待他们完成
```

### 8.2 场景：功能开发被阻塞

```bash
# 情况：你需要另一个模块的 API，但它还没开发完

# 方案 1：使用 Mock（推荐）
# 在你的代码中先写 Mock 函数
def get_user_by_id(user_id: int):
    # TODO: 等待认证模块实现
    return {"id": user_id, "username": "mock_user"}

# 方案 2：定义接口契约，并行开发
# 1. 先和负责人确定 API 设计（在 docs/api/ 中）
# 2. 你基于契约开发前端
# 3. 后端负责人实现 API
# 4. 最后集成测试

# 方案 3：创建 Issue 并标记为阻塞
gh issue create --title "需要用户认证 API" \
  --label blocked \
  --assignee auth-lead \
  --body "我的发布功能需要 /api/users/me 接口，优先级高。"
```

### 8.3 场景：紧急修复生产问题

```bash
# 1. 立即从 main 创建 hotfix 分支
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-fix

# 2. 快速修复并测试
# <修复代码>
pytest backend/tests/  # 确保测试通过

# 3. 提交并推送
git add <files>
git commit -m "fix(security): patch critical XSS vulnerability

SECURITY: Immediate fix required for production.
Details: <CVE link or internal ticket>"

git push origin hotfix/critical-security-fix

# 4. 创建 PR 到 main（标记为 critical）
gh pr create --base main \
  --head hotfix/critical-security-fix \
  --title "fix(security): patch critical XSS vulnerability" \
  --label security --label priority:critical \
  --reviewer security-lead,infra-lead

# 5. 审查通过后立即合并
# 6. 将 hotfix 也合并到 develop
gh pr create --base develop \
  --head hotfix/critical-security-fix \
  --title "fix(security): patch critical XSS vulnerability (backport)"
```

### 8.4 场景：长期功能分支管理

```bash
# 情况：某个功能需要开发 2 周以上

# 1. 创建长期 feature 分支
git checkout -b feature/governance-module

# 2. 将大功能拆分为小任务，创建子分支
git checkout -b feature/governance-module-committee-model
# 完成后合并到 feature/governance-module

git checkout -b feature/governance-module-meeting-api
# 完成后合并到 feature/governance-module

# 3. 定期同步 develop（每 2-3 天）
git checkout feature/governance-module
git rebase develop

# 4. 子功能完成后先合并到主 feature 分支
git checkout feature/governance-module
git merge --no-ff feature/governance-module-committee-model

# 5. 整个功能完成后一次性合并到 develop
gh pr create --base develop \
  --head feature/governance-module \
  --title "feat(governance): add complete committee management"
```

---

## 九、Git Hooks 和自动化

### 9.1 Pre-commit Hook（由角色4配置）

```bash
# 安装 pre-commit
pip install pre-commit

# 配置 .pre-commit-config.yaml（见相关文档）

# 安装 hooks
pre-commit install

# 手动运行检查
pre-commit run --all-files
```

### 9.2 Commit Message 验证

```bash
# .git/hooks/commit-msg（自动生成）
# 验证 commit message 格式是否符合 conventional commits

# 如果格式错误，commit 会被拒绝
git commit -m "bad commit message"
# Error: Commit message does not follow conventional commits format
```

### 9.3 Pre-push Hook

```bash
# .git/hooks/pre-push
# 推送前自动运行测试

#!/bin/bash
echo "Running tests before push..."
cd backend && pytest --cov=app --cov-fail-under=80
if [ $? -ne 0 ]; then
  echo "Tests failed, push aborted."
  exit 1
fi
echo "Tests passed, proceeding with push."
```

---

## 十、团队协作日常检查清单

### 每天开始工作时
- [ ] 切换到 develop 并拉取最新代码：`git checkout develop && git pull`
- [ ] 将最新的 develop 合并到你的 feature 分支：`git checkout feature/xxx && git rebase develop`
- [ ] 查看是否有新的 PR 需要审查：`gh pr list --author=@me`
- [ ] 查看是否有被分配的 Issue：`gh issue list --assignee=@me`

### 提交 PR 前
- [ ] 确保所有测试通过：`pytest` 和 `npm run test`
- [ ] 运行 linter：`black`, `flake8`, `eslint`
- [ ] 同步最新的 develop 分支
- [ ] 检查是否有敏感信息（密码、API key）
- [ ] 更新相关文档（API 文档、README）
- [ ] 填写完整的 PR 描述

### 审查 PR 时
- [ ] 阅读 PR 描述理解变更目的
- [ ] 检查代码逻辑和安全性
- [ ] 运行代码并手动测试
- [ ] 查看测试覆盖率报告
- [ ] 在 4 小时内给出反馈

### 每周五（发布前）
- [ ] 运行完整的集成测试
- [ ] 检查所有 PR 是否已合并
- [ ] 更新 CHANGELOG.md
- [ ] 准备 release 分支

---

## 十一、常见问题（FAQ）

### Q1: 我不小心在 main 分支上提交了代码怎么办？
```bash
# 如果还没推送到远程
git reset HEAD~1  # 撤销最后一次 commit
git stash         # 保存变更
git checkout -b feature/my-fix  # 创建新分支
git stash pop     # 恢复变更

# 如果已经推送，联系管理员回滚
```

### Q2: 我的 feature 分支和 develop 差距太大了怎么办？
```bash
# 方案 1：rebase（推荐，但可能有多次冲突）
git checkout feature/my-branch
git rebase develop

# 方案 2：merge（简单但会产生 merge commit）
git checkout feature/my-branch
git merge develop

# 方案 3：重新创建分支（适合冲突太多）
git checkout develop
git checkout -b feature/my-branch-v2
git cherry-pick <需要的 commit>
```

### Q3: 如何快速查看某个文件的历史变更？
```bash
# 查看文件的 commit 历史
git log --follow -- backend/app/api/auth.py

# 查看每次变更的具体内容
git log -p -- backend/app/api/auth.py

# 使用 Claude Code 分析
"请分析 backend/app/api/auth.py 最近 10 次提交的变更历史，
总结主要的功能演进。"
```

### Q4: 如何撤销已经推送的 commit？
```bash
# 方案 1：使用 revert（推荐，不改变历史）
git revert <commit-hash>
git push origin feature/my-branch

# 方案 2：使用 reset + force push（仅限自己的分支）
git reset --hard HEAD~1
git push --force-with-lease origin feature/my-branch

# ⚠️ 永远不要在 main 或 develop 上 force push！
```

### Q5: 如何处理二进制文件冲突（如图片）？
```bash
# 冲突时选择使用某一方的版本
git checkout --ours path/to/image.png    # 使用你的版本
git checkout --theirs path/to/image.png  # 使用他们的版本

git add path/to/image.png
git rebase --continue
```

---

## 十二、相关资源

- **项目文档**：
  - [团队分工方案](./TEAM_DIVISION_CLAUDE_CODE.md)
  - [文件所有权](./OWNERSHIP.md)
  - [API 设计文档](./api/)
  - [实施计划](./plannings/01-实施计划.md)

- **Git 学习资源**：
  - [Pro Git Book](https://git-scm.com/book/zh/v2)
  - [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)
  - [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)

- **工具文档**：
  - [GitHub CLI (gh)](https://cli.github.com/manual/)
  - [Pre-commit](https://pre-commit.com/)

---

## 附录：快速命令参考

```bash
# === 分支管理 ===
git checkout -b feature/xxx    # 创建并切换到新分支
git branch -d feature/xxx      # 删除本地分支
git push origin --delete xxx   # 删除远程分支

# === 同步代码 ===
git fetch origin              # 获取远程更新
git pull origin develop       # 拉取并合并 develop
git rebase develop            # 将当前分支 rebase 到 develop

# === 提交代码 ===
git add <file>                # 添加文件到暂存区
git commit -m "message"       # 提交
git push origin <branch>      # 推送到远程

# === PR 管理 ===
gh pr create                  # 创建 PR
gh pr list                    # 查看 PR 列表
gh pr checkout 123            # 检出 PR #123
gh pr review 123 --approve    # 批准 PR

# === 冲突解决 ===
git status                    # 查看冲突文件
git add <resolved-file>       # 标记冲突已解决
git rebase --continue         # 继续 rebase
git rebase --abort            # 中止 rebase

# === 撤销操作 ===
git reset HEAD~1              # 撤销最后一次 commit（保留变更）
git reset --hard HEAD~1       # 撤销最后一次 commit（丢弃变更）
git revert <commit-hash>      # 创建一个新 commit 来撤销指定 commit

# === 查看历史 ===
git log --oneline --graph     # 查看提交历史（图形化）
git log --follow -- <file>    # 查看文件历史
git diff develop              # 对比与 develop 的差异
```

---

**文档维护**：本文档由角色4（平台与基础设施专家）负责维护，所有团队成员都可以提出改进建议。

**最后更新**：2026-02-09
