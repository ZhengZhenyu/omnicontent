# openGecko 文件权责划分表

> 本文档定义了项目中每个文件/目录的主要负责人和协作者。
>
> **原则**：修改他人负责的文件前，请先沟通或提交PR让负责人审查。

## 角色定义

| 角色ID | 角色名称 | 英文名 | 核心职责 |
|-------|---------|--------|---------|
| 👤 角色1 | 认证与权限架构师 | Auth & Security Lead | 用户认证、权限控制、多租户隔离、安全审计 |
| 📝 角色2 | 社区与内容管理专家 | Content Management Lead | 社区管理、内容CRUD、文件处理、格式转换 |
| 🚀 角色3 | 多渠道发布工程师 | Publishing Integration Lead | 多渠道发布、第三方API集成、渠道配置管理 |
| 🔧 角色4 | 数据分析与基础设施专家 | Analytics & Infrastructure Lead | 数据分析、数据库设计、CI/CD、测试基础设施 |

---

## 后端文件权责划分

### API 路由层 (`backend/app/api/`)

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `auth.py` | 👤 角色1 | - | 认证接口：登录、注册、密码重置、初始化设置 |
| `communities.py` | 📝 角色2 | 👤 角色1 | 社区CRUD、成员管理（需权限验证） |
| `contents.py` | 📝 角色2 | 👤 角色1 | 内容CRUD、状态管理（需权限验证） |
| `upload.py` | 📝 角色2 | - | 文件上传：DOCX、图片、封面 |
| `publish.py` | 🚀 角色3 | 📝 角色2 | 发布接口：多渠道发布、预览（依赖内容数据） |
| `analytics.py` | 🔧 角色4 | - | 数据分析接口：概览、统计、渠道配置 |

### 核心功能 (`backend/app/core/`)

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `security.py` | 👤 角色1 | - | 安全核心：JWT、密码哈希、Fernet加密 |
| `dependencies.py` | 👤 角色1 | 🔧 角色4 | FastAPI依赖注入：权限验证、社区隔离 |

### 数据模型 (`backend/app/models/`)

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `user.py` | 👤 角色1 | - | 用户模型、社区成员关联表 |
| `password_reset.py` | 👤 角色1 | - | 密码重置Token模型 |
| `audit.py` | 👤 角色1 | - | 审计日志模型 |
| `community.py` | 📝 角色2 | - | 社区模型 |
| `content.py` | 📝 角色2 | - | 内容模型、协作者关联表 |
| `publish_record.py` | 🚀 角色3 | - | 发布记录、内容分析模型 |
| `channel.py` | 🚀 角色3 | 👤 角色1 | 渠道配置模型（使用加密存储） |
| `__init__.py` | 🔧 角色4 | 模型负责人 | 模型聚合、关系维护 |

### 数据验证模式 (`backend/app/schemas/`)

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `auth.py` | 👤 角色1 | - | 认证相关Schema |
| `user.py` | 👤 角色1 | - | 用户相关Schema |
| `community.py` | 📝 角色2 | - | 社区相关Schema |
| `content.py` | 📝 角色2 | - | 内容相关Schema |
| `publish.py` | 🚀 角色3 | - | 发布相关Schema |
| `__init__.py` | 🔧 角色4 | - | Schema聚合 |

### 业务逻辑服务 (`backend/app/services/`)

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `converter.py` | 📝 角色2 | - | 格式转换：Markdown/HTML/DOCX |
| `wechat.py` | 🚀 角色3 | 👤 角色1 | 微信公众号API集成（使用加密） |
| `hugo.py` | 🚀 角色3 | - | Hugo博客生成 |
| `csdn.py` | 🚀 角色3 | - | CSDN格式适配 |
| `zhihu.py` | 🚀 角色3 | - | 知乎格式适配 |
| `exceptions.py` | 🚀 角色3 | 所有人 | 统一服务层异常（待创建） |

### 应用配置与数据库 (`backend/app/`)

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `config.py` | 🔧 角色4 | 所有人 | 全局配置（变更需Code Review） |
| `database.py` | 🔧 角色4 | - | 数据库连接与初始化 |
| `main.py` | 🔧 角色4 | - | FastAPI应用入口 |

### 数据库迁移 (`backend/alembic/`)

| 目录/文件 | 主要负责人 | 协作者 | 说明 |
|---------|-----------|-------|------|
| `versions/` | 🔧 角色4 | 模型负责人 | 迁移脚本（模型变更者提供SQL） |
| `env.py` | 🔧 角色4 | - | Alembic环境配置 |

### 测试 (`backend/tests/`)

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `conftest.py` | 🔧 角色4 | - | 测试fixtures和配置 |
| `test_auth_api.py` | 👤 角色1 | - | 认证API测试 |
| `test_auth_integration.py` | 👤 角色1 | - | 认证集成测试 |
| `test_communities_api.py` | 📝 角色2 | - | 社区API测试 |
| `test_contents_api.py` | 📝 角色2 | - | 内容API测试 |
| `test_rbac_collaboration.py` | 📝 角色2 | 👤 角色1 | 权限和协作测试 |
| `test_publish_api.py` | 🚀 角色3 | - | 发布API测试 |
| `test_analytics_api.py` | 🔧 角色4 | - | 分析API测试 |

---

## 前端文件权责划分

### 页面组件 (`frontend/src/views/`)

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `Login.vue` | 👤 角色1 | - | 登录页 |
| `InitialSetup.vue` | 👤 角色1 | - | 初始化设置页 |
| `ForgotPassword.vue` | 👤 角色1 | - | 忘记密码页 |
| `ResetPassword.vue` | 👤 角色1 | - | 重置密码页 |
| `UserManage.vue` | 👤 角色1 | - | 用户管理页 |
| `CommunityManage.vue` | 📝 角色2 | 👤 角色1 | 社区管理页 |
| `ContentList.vue` | 📝 角色2 | - | 内容列表页 |
| `ContentEdit.vue` | 📝 角色2 | - | 内容编辑页（最复杂） |
| `PublishView.vue` | 🚀 角色3 | 📝 角色2 | 发布管理页（多渠道预览） |
| `Settings.vue` | 🚀 角色3 | - | 设置页（渠道凭证配置） |
| `Dashboard.vue` | 🔧 角色4 | - | 数据仪表板页 |

### 可复用组件 (`frontend/src/components/`)

| 文件/目录 | 主要负责人 | 协作者 | 说明 |
|---------|-----------|-------|------|
| `CommunitySwitcher.vue` | 📝 角色2 | - | 社区切换器 |
| `common/` | 📝 角色2 | 所有人 | 通用组件目录（待创建） |
| `business/` | 📝 角色2 | 所有人 | 业务组件目录（待创建） |

### 状态管理 (`frontend/src/stores/`)

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `auth.ts` | 👤 角色1 | - | 认证状态：token、user、communities |
| `community.ts` | 📝 角色2 | - | 社区状态：currentCommunityId |

### API客户端 (`frontend/src/api/`)

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `index.ts` | 🔧 角色4 | - | Axios配置、拦截器 |
| `auth.ts` | 👤 角色1 | - | 认证API调用 |
| `community.ts` | 📝 角色2 | - | 社区API调用 |
| `content.ts` | 📝 角色2 | - | 内容API调用 |
| `publish.ts` | 🚀 角色3 | - | 发布API调用 |

### 路由配置 (`frontend/src/router/`)

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `index.ts` | 🔧 角色4 | 👤 角色1 | 路由配置（角色1负责路由守卫部分） |

### TypeScript类型定义 (`frontend/src/types/`)

| 目录 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `types/` | 🔧 角色4 | 所有人 | TypeScript类型定义目录（待创建） |

### 工具函数 (`frontend/src/utils/`)

| 目录 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `utils/` | 🔧 角色4 | 所有人 | 工具函数目录（待扩展） |

### 组合式函数 (`frontend/src/composables/`)

| 目录 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `composables/` | 📝 角色2 | 所有人 | 可复用逻辑目录（待扩展） |

---

## 基础设施与配置文件

### Docker与部署

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `docker-compose.yml` | 🔧 角色4 | - | Docker编排配置 |
| `backend/Dockerfile` | 🔧 角色4 | - | 后端容器配置 |
| `frontend/Dockerfile` | 🔧 角色4 | - | 前端容器配置 |
| `Makefile` | 🔧 角色4 | - | 构建脚本 |

### CI/CD

| 目录/文件 | 主要负责人 | 协作者 | 说明 |
|---------|-----------|-------|------|
| `.github/workflows/` | 🔧 角色4 | - | GitHub Actions工作流（待创建） |
| `.pre-commit-config.yaml` | 🔧 角色4 | - | Pre-commit hooks配置（待创建） |

### 依赖管理

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `backend/requirements.txt` | 🔧 角色4 | - | 后端Python依赖 |
| `backend/requirements-dev.txt` | 🔧 角色4 | - | 后端开发依赖 |
| `frontend/package.json` | 🔧 角色4 | - | 前端npm依赖 |

### 测试配置

| 文件 | 主要负责人 | 协作者 | 说明 |
|-----|-----------|-------|------|
| `backend/pytest.ini` | 🔧 角色4 | - | Pytest配置 |
| `backend/TESTING.md` | 🔧 角色4 | - | 测试文档 |

---

## 文档

### 项目文档 (`docs/`)

| 文件/目录 | 主要负责人 | 协作者 | 说明 |
|---------|-----------|-------|------|
| `README.md` | 🔧 角色4 | - | 项目说明 |
| `CHANGELOG.md` | 所有人 | - | 变更日志（所有人更新） |
| `OWNERSHIP.md` | 🔧 角色4 | - | 本文档 |
| `GIT_WORKFLOW.md` | 🔧 角色4 | - | Git工作流文档（待创建） |
| `design/` | 🔧 角色4 | 架构变更者 | 设计文档 |
| `requirements/` | 🔧 角色4 | - | 需求文档 |
| `api/` | API开发者 | - | API文档目录（待创建） |

### API文档 (`docs/api/`) - 待创建

| 文件 | 主要负责人 | 说明 |
|-----|-----------|------|
| `auth-api.md` | 👤 角色1 | 认证API文档 |
| `community-api.md` | 📝 角色2 | 社区API文档 |
| `content-api.md` | 📝 角色2 | 内容API文档 |
| `publish-api.md` | 🚀 角色3 | 发布API文档 |
| `analytics-api.md` | 🔧 角色4 | 分析API文档 |

---

## 协作规范

### 📌 修改他人负责的文件

如果你需要修改他人负责的文件，请遵循以下流程：

1. **提前沟通**：在团队群或私聊中说明修改原因和范围
2. **创建Issue**：在GitHub上创建Issue并@相关负责人
3. **提交PR**：提交Pull Request并指定负责人为Reviewer
4. **等待审查**：等待负责人审查并批准

### 📌 跨模块变更

如果你的变更涉及多个模块，请：

1. **至少2人审查**：指定至少2位相关负责人作为Reviewer
2. **API契约先行**：如涉及API变更，先更新API文档并获得团队同意
3. **分步提交**：优先提交基础设施部分（如Schema），再提交业务逻辑

### 📌 紧急修复

如果遇到紧急Bug需要快速修复：

1. **创建hotfix分支**：`hotfix/<issue-id>-<description>`
2. **通知负责人**：在群里@文件负责人说明情况
3. **快速审查**：负责人应在1小时内审查
4. **事后复盘**：修复后在团队会议上分享根本原因

---

## 版本历史

| 版本 | 日期 | 修改人 | 说明 |
|-----|------|-------|------|
| v1.0 | 2026-02-09 | 🔧 角色4 | 初始版本 |

---

## 联系方式

如有文件权责划分相关问题，请联系：

- **文档维护者**：🔧 角色4（基础设施专家）
- **协作流程问题**：在团队会议上讨论
- **权责调整**：需要团队一致同意后更新本文档
