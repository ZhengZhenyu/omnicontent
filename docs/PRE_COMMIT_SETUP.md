# Pre-commit Hooks 设置指南

本文档说明如何为 openGecko 项目配置 pre-commit hooks，确保代码质量和规范。

---

## 什么是 Pre-commit Hooks？

Pre-commit hooks 是在你提交代码（`git commit`）之前自动运行的脚本，用于：
- 自动格式化代码
- 检测代码质量问题
- 发现安全漏洞
- 验证 commit message 格式
- 防止提交敏感信息

---

## 安装步骤

### 1. 安装 pre-commit 工具

```bash
# 使用 pip 安装（推荐）
pip install pre-commit

# 或使用 brew（macOS）
brew install pre-commit

# 验证安装
pre-commit --version
```

### 2. 安装项目 hooks

在项目根目录执行：

```bash
# 克隆仓库后首次设置
cd /path/to/openGecko
pre-commit install

# 安装 commit-msg hook（检查提交信息格式）
pre-commit install --hook-type commit-msg

# 验证安装
ls -la .git/hooks/
# 应该看到 pre-commit 和 commit-msg 文件
```

### 3. 初始化 secrets baseline（可选）

如果你的仓库已经有一些"假阳性"的密钥检测（如示例配置），可以创建 baseline：

```bash
# 生成 secrets baseline
detect-secrets scan > .secrets.baseline

# 查看检测到的"secrets"
detect-secrets audit .secrets.baseline
```

---

## 使用方法

### 自动运行（推荐）

安装后，每次 `git commit` 时会自动运行 hooks：

```bash
git add backend/app/api/auth.py
git commit -m "feat(auth): add OAuth login"

# Pre-commit hooks 自动运行：
# ✅ Check for added large files...Passed
# ✅ Check for merge conflicts...Passed
# ✅ Format Python code with Black...Passed
# ✅ Sort Python imports with isort...Passed
# ✅ Lint Python code with Flake8...Passed
# ✅ Type check Python with mypy...Passed
# ✅ Security check with Bandit...Passed
# ✅ Check commit message format...Passed

# 如果所有检查通过，提交成功
# 如果有检查失败，提交被拒绝
```

### 手动运行

```bash
# 对所有文件运行所有 hooks
pre-commit run --all-files

# 只运行特定 hook
pre-commit run black --all-files
pre-commit run flake8 --all-files
pre-commit run eslint --all-files

# 对特定文件运行
pre-commit run --files backend/app/api/auth.py
```

### 跳过 hooks（不推荐）

在紧急情况下，可以跳过 pre-commit 检查：

```bash
# ⚠️ 不推荐：跳过所有 hooks
git commit --no-verify -m "emergency fix"

# 注意：CI 仍然会运行检查
```

---

## Hooks 详细说明

### 通用文件检查

| Hook | 作用 | 触发条件 |
|------|------|---------|
| check-added-large-files | 防止提交大文件（>500KB） | 所有文件 |
| check-merge-conflict | 检测未解决的合并冲突标记 | 所有文件 |
| check-yaml/json/toml | 验证配置文件语法 | .yml, .json, .toml 文件 |
| end-of-file-fixer | 确保文件以换行符结尾 | 所有文本文件 |
| trailing-whitespace | 删除行尾空白 | 所有文本文件 |
| detect-private-key | 检测私钥 | 所有文件 |
| no-commit-to-branch | 防止直接提交到 main/develop | 保护分支 |

### Python 后端检查（`backend/` 目录）

| Hook | 作用 | 自动修复 | 配置 |
|------|------|---------|------|
| **black** | 代码格式化 | ✅ 是 | 行长度: 100 |
| **isort** | 导入语句排序 | ✅ 是 | 兼容 black |
| **flake8** | 代码风格检查 | ❌ 否 | 忽略 E203, W503 |
| **mypy** | 类型检查 | ❌ 否 | 忽略缺失类型 |
| **bandit** | 安全漏洞扫描 | ❌ 否 | 低/中等级 |

**示例输出**：
```bash
# black 自动格式化
Reformatted backend/app/api/auth.py
All done! ✨ 🍰 ✨
1 file reformatted.

# flake8 检测到问题
backend/app/api/auth.py:45:80: E501 line too long (105 > 100 characters)
backend/app/api/auth.py:67:1: F401 'typing.Optional' imported but unused
```

### 前端检查（`frontend/` 目录）

| Hook | 作用 | 自动修复 | 文件类型 |
|------|------|---------|---------|
| **eslint** | JavaScript/TypeScript/Vue 代码检查 | ✅ 部分 | .js, .ts, .vue |
| **prettier** | 代码格式化 | ✅ 是 | .js, .ts, .vue, .css, .json |

**示例输出**：
```bash
# prettier 自动格式化
frontend/src/views/Login.vue 50ms
frontend/src/api/auth.ts 32ms

# eslint 检测到问题
frontend/src/views/Login.vue
  12:7  error  'username' is assigned a value but never used  @typescript-eslint/no-unused-vars
  45:3  warning  Unexpected console statement  no-console
```

### Commit Message 检查

验证提交信息是否符合 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```bash
# ✅ 正确格式
feat(auth): add OAuth login
fix(content): resolve duplicate save issue
docs(readme): update installation steps

# ❌ 错误格式
Added OAuth login          # 缺少 type 和 scope
fix: bug                   # 描述过于简单
feat(auth) add login       # 缺少冒号
```

**格式要求**：
```
<type>(<scope>): <subject>

type: feat, fix, docs, style, refactor, perf, test, chore, ci
scope: auth, content, publish, governance, analytics, infra
subject: 小写字母开头，不超过 50 字符，不以句号结尾
```

### 安全检查

| Hook | 作用 | 检测内容 |
|------|------|---------|
| **detect-secrets** | 检测硬编码的密钥 | API keys, passwords, tokens |
| **bandit** | 扫描 Python 安全漏洞 | SQL 注入, 不安全的函数调用 |

**示例检测**：
```python
# ❌ 会被 detect-secrets 检测到
API_KEY = "sk-1234567890abcdef"
password = "admin123"

# ✅ 正确做法
API_KEY = os.getenv("API_KEY")
password = os.getenv("ADMIN_PASSWORD")
```

---

## 常见问题

### Q1: Hook 运行失败怎么办？

```bash
# 查看详细错误信息
pre-commit run --all-files --verbose

# 如果是依赖问题，清理并重新安装
pre-commit clean
pre-commit install-hooks
```

### Q2: 如何更新 hooks 到最新版本？

```bash
# 自动更新所有 hooks
pre-commit autoupdate

# 手动更新 .pre-commit-config.yaml 中的 rev 版本
```

### Q3: Black 和 Flake8 冲突怎么办？

我们的配置已经处理了这个问题：
- Flake8 忽略 E203（与 Black 冲突）
- Flake8 忽略 W503（与 Black 冲突）
- isort 使用 `--profile black` 兼容 Black

### Q4: ESLint 在 pre-commit 中无法运行？

确保前端依赖已安装：

```bash
cd frontend
npm install

# 或让 pre-commit 安装依赖
pre-commit run eslint --all-files
```

### Q5: 如何禁用特定 hook？

临时禁用（单次提交）：
```bash
SKIP=flake8 git commit -m "feat: work in progress"
SKIP=eslint,prettier git commit -m "feat: draft changes"
```

永久禁用（修改 `.pre-commit-config.yaml`）：
```yaml
- repo: https://github.com/pycqa/flake8
  rev: 7.0.0
  hooks:
    - id: flake8
      stages: [manual]  # 只在手动运行时执行
```

### Q6: Commit message 检查失败？

确保提交信息符合规范：

```bash
# ❌ 错误
git commit -m "fixed bug"

# ✅ 正确
git commit -m "fix(auth): resolve JWT token refresh issue"

# 或使用编辑器编写详细提交信息
git commit  # 会打开编辑器
```

---

## 团队协作建议

### 1. 统一开发环境

所有团队成员应：
- 安装相同版本的 pre-commit
- 使用相同的 Python/Node.js 版本
- 定期执行 `pre-commit autoupdate`

### 2. 处理遗留代码

如果项目中已有大量不符合规范的代码：

```bash
# 逐步修复（推荐）
# 1. 先提交 .pre-commit-config.yaml
git add .pre-commit-config.yaml
git commit -m "chore: add pre-commit hooks configuration"

# 2. 运行 hooks 修复所有代码
pre-commit run --all-files

# 3. 提交格式化后的代码
git add -u
git commit -m "style: auto-format codebase with pre-commit hooks"

# 一次性修复（如果改动太大）
# 可以分模块逐步进行
pre-commit run black --files backend/app/api/*.py
git add backend/app/api/
git commit -m "style: format auth API with black"
```

### 3. CI/CD 集成

Pre-commit hooks 也在 CI 中运行：

```yaml
# .github/workflows/pre-commit.yml
name: Pre-commit Checks

on: [push, pull_request]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - uses: pre-commit/action@v3.0.0
```

### 4. 使用 Claude Code 修复问题

当 pre-commit 检测到问题时，可以让 Claude Code 帮忙修复：

```bash
# 运行 pre-commit 并保存输出
pre-commit run --all-files > pre-commit-errors.txt

# 在 Claude Code 中：
"请根据以下 pre-commit 错误报告修复代码：
<粘贴 pre-commit-errors.txt 内容>

要求：
1. 修复所有 flake8 错误
2. 解决 mypy 类型检查问题
3. 修复 bandit 安全警告
4. 确保不破坏现有功能"
```

---

## 自定义配置

### 修改 Black 行长度

编辑 `.pre-commit-config.yaml`：

```yaml
- repo: https://github.com/psf/black
  rev: 23.12.1
  hooks:
    - id: black
      args: ['--line-length=120']  # 修改为 120
```

同时更新 `backend/pyproject.toml` 或 `backend/setup.cfg`：

```toml
# pyproject.toml
[tool.black]
line-length = 120
```

### 添加自定义 hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-migration-message
        name: Check Alembic migration message
        entry: bash -c 'grep -q "message" alembic.ini || exit 0'
        language: system
        files: ^backend/alembic/versions/.*\.py$
```

---

## 卸载 Pre-commit Hooks

如果需要临时禁用：

```bash
# 卸载 hooks
pre-commit uninstall
pre-commit uninstall --hook-type commit-msg

# 恢复
pre-commit install
pre-commit install --hook-type commit-msg
```

---

## 相关资源

- [Pre-commit 官方文档](https://pre-commit.com/)
- [Conventional Commits 规范](https://www.conventionalcommits.org/zh-hans/)
- [Black 代码风格指南](https://black.readthedocs.io/)
- [Flake8 错误代码](https://flake8.pycqa.org/en/latest/user/error-codes.html)
- [项目 Git 工作流文档](./GIT_WORKFLOW.md)

---

**文档维护**：本文档由角色4（平台与基础设施专家）负责维护。

**最后更新**：2026-02-09
