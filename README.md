# OmniContent

<div align="center">

**全域内容管理平台 - Manage All, Publish Everywhere**

企业级多社区全渠道内容编排与发布系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.3+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal.svg)](https://fastapi.tiangolo.com/)

</div>

## ✨ 项目简介

OmniContent 是为管理 10+ 开源社区打造的企业级多租户内容管理平台，支持统一管理多个社区的内容策划、创作、编排和多渠道发布。

### 核心特性

🏢 **多租户架构** - 共享数据库，社区级数据隔离，独立配置管理
📅 **日历视图** - 可拖拽的内容排期沙盘，可视化策划发布计划
📋 **看板管理** - Kanban 流程可视化 (草稿 → 审核 → 通过 → 发布)
📊 **数据分析** - 按社区/渠道/作者多维度透视，ECharts 可视化仪表板
🚀 **多渠道发布** - 一键分发至微信公众号、Hugo、CSDN、知乎
✏️ **智能编辑** - 支持 DOCX/Markdown 上传，自动格式转换和图片提取
🔐 **用户认证** - JWT 认证，多用户协作，完整审计日志

## 🎯 应用场景

- **多社区运营**: 统一管理多个开源社区的内容发布
- **内容编排**: 日历视图规划发布计划，看板管理内容流转
- **团队协作**: 多用户权限管理，操作审计追溯
- **数据驱动**: 多维度数据分析，发布效果可视化

## 🏗️ 技术架构

### 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| **前端** | Vue 3 + Pinia + Element Plus | 企业级组件库，TypeScript 支持 |
| **日历** | FullCalendar | 拖拽式内容排期 |
| **看板** | vue-draggable-plus | 流程可视化 |
| **图表** | ECharts | 数据分析仪表板 |
| **后端** | FastAPI + SQLAlchemy | 高性能异步框架，自动生成 API 文档 |
| **数据库** | SQLite / PostgreSQL | 开发/生产环境 |
| **认证** | JWT + bcrypt | 安全认证机制 |
| **部署** | Docker Compose | 容器化部署 |

### 架构特点

- 🎨 **前后端分离**: RESTful API 设计
- 🏢 **多租户隔离**: Community ID 级别数据隔离
- 🔒 **依赖注入**: FastAPI Depends 实现权限控制
- 📦 **ORM 模式**: SQLAlchemy + Alembic 数据库迁移
- 📝 **审计日志**: 完整的操作追踪记录

## 📦 功能模块

### 已实现 ✅

- ✅ **基础认证与权限**: JWT 用户认证、多用户协作、审计日志
- ✅ **多租户架构**: Community ID 级别数据隔离、社区独立配置
- ✅ **内容管理**: DOCX/Markdown 上传、在线编辑、封面图管理
- ✅ **多渠道发布**:
  - 微信公众号 (API 创建草稿)
  - Hugo 博客 (自动生成 front matter)
  - CSDN/知乎 (一键复制适配格式)
- ✅ **效果追踪**: 发布记录、数据概览
- ✅ **内容工作流**: 状态流转管理

### 规划中 📋

- 📅 **日历视图**: FullCalendar 可拖拽排期 (Phase 2)
- 📋 **看板管理**: Kanban 流程可视化 (Phase 3)
- 📊 **数据分析**: ECharts 多维度仪表板 (Phase 4)

详见 [实施计划](docs/plannings/01-实施计划.md)

## 🚀 快速开始

### 前置条件

- **Python 3.11+**
- **Node.js 18+** / npm
- **Make**（macOS / Linux 自带）

### 1. 安装依赖

```bash
make setup
```

> 该命令会：创建 Python 虚拟环境 `.venv` 并安装后端依赖 → 安装前端 npm 依赖 → 从 `.env.example` 生成 `backend/.env`。

### 2. 配置环境变量

编辑 `backend/.env`，按需修改以下关键项：

```env
# 数据库（默认 SQLite，生产可改为 PostgreSQL）
DATABASE_URL=sqlite:///./omnicontent.db

# JWT 密钥（⚠️ 生产环境务必修改为强随机字符串）
JWT_SECRET_KEY=your-secret-key-change-in-production

# 默认管理员账号（仅首次启动时用于初始化，见下方说明）
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=admin123
DEFAULT_ADMIN_EMAIL=admin@example.com

# SMTP（可选，用于密码重置邮件）
# SMTP_HOST=smtp.example.com
# SMTP_PORT=587
# SMTP_USER=your-email@example.com
# SMTP_PASSWORD=your-email-password
# SMTP_FROM_EMAIL=noreply@example.com
```

### 3. 启动开发服务器

```bash
make dev
```

访问：
- 🖥️ **前端界面**: http://localhost:3000
- 📖 **API 文档**: http://localhost:8000/docs

### 4. 初始设置流程

1. **首次登录** — 使用 `.env` 中配置的默认管理员账号登录（默认 `admin` / `admin123`）
2. **强制创建新管理员** — 首次登录后系统会要求你创建一个正式管理员账号（设置用户名、密码、邮箱）
3. **默认账号自动删除** — 新管理员创建成功后，默认 `admin` 账号将被自动删除，以确保安全
4. **配置渠道凭证** — 登录后进入「设置」页面，为各社区配置发布渠道（微信 AppID/Secret、CSDN Cookie 等），所有凭证均使用 Fernet 加密存储

### Docker 部署（生产环境）

```bash
# 1. 配置环境变量
cp backend/.env.example backend/.env
# ⚠️ 编辑 backend/.env，务必修改 JWT_SECRET_KEY

# 2. 启动服务
docker compose up -d
```

- 前端: http://localhost（Nginx 代理，端口 80）
- 后端 API: http://localhost:8000

## 📚 文档

### 快速导航

- [开发指南](docs/DEVELOPMENT.md) - 开发环境设置、工作流程、代码规范
- [配置指南](docs/CONFIGURATION.md) - 环境变量、渠道配置、部署配置

### 设计文档

- [需求分析文档](docs/requirements/01-需求分析文档.md)
- [系统架构设计](docs/design/01-系统架构设计.md)
- [数据库详细设计](docs/design/02-数据库详细设计.md)
- [UML 设计视图](docs/uml/01-类图与时序图.md)
- [实施计划](docs/plannings/01-实施计划.md)

完整文档索引请查看 [docs/README.md](docs/README.md)

## 🗺️ 开发路线图

### Phase 1: 基础认证与社区隔离 ✅
- ✅ JWT 用户认证系统
- ✅ 多租户数据隔离
- ✅ 社区管理 CRUD
- ✅ 审计日志系统

### Phase 2: 日历视图与计划发布 🚧
- [ ] FullCalendar 日历视图集成
- [ ] 拖拽式内容排期
- [ ] 定时发布服务
- [ ] 日历视图与内容库联动

### Phase 3: 看板视图与流程管理
- [ ] Kanban 看板视图
- [ ] 拖拽改变状态
- [ ] 批量操作
- [ ] 自定义工作流

### Phase 4: 可视化分析仪表板
- [ ] ECharts 多维度图表
- [ ] 渠道/作者/分类统计
- [ ] 发布趋势分析
- [ ] 自定义报表

详见 [实施计划](docs/plannings/01-实施计划.md)

## 📄 License

[MIT License](LICENSE)

---

<div align="center">

**OmniContent** - Manage All, Publish Everywhere 🚀

Made with ❤️ for Open Source Communities

</div>
