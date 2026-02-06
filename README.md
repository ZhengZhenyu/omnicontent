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
- 🔐 **用户认证**: JWT 登录、多用户协作 (Phase 1)
- 🏢 **社区管理**: 多租户架构、社区隔离 (Phase 1)

详见 [实施计划](docs/plannings/01-实施计划.md)

## 🚀 快速开始

### 前置条件

- Python 3.11+
- Node.js 18+
- (可选) Docker & Docker Compose

macOS 用户可通过 Homebrew 安装:

```bash
brew install python@3.11 node
```

### 开发环境启动

#### 方式 1: Make 命令 (推荐)

```bash
# 首次运行: 安装依赖、创建数据库
make setup

# 启动前后端开发服务器
make dev
```

访问:
- 前端: http://localhost:3000
- API 文档: http://localhost:8000/docs

#### 方式 2: 手动启动

**后端**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 编辑配置
uvicorn app.main:app --reload
```

**前端**:
```bash
cd frontend
npm install
npm run dev
```

### 生产环境部署

```bash
cp backend/.env.example backend/.env  # 编辑配置
docker compose up -d
```

访问 http://localhost

## ⚙️ 配置说明

在 `backend/.env` 中配置渠道账号:

```env
# 微信公众号
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret

# Hugo 博客
HUGO_REPO_PATH=/path/to/hugo/repo
HUGO_CONTENT_DIR=content/posts

# 数据库 (生产环境)
DATABASE_URL=postgresql://user:pass@localhost/omnicontent

# JWT 密钥 (生产必须修改!)
JWT_SECRET_KEY=your-super-secret-key-change-me
```

## 📚 文档

- [需求分析文档](docs/requirements/01-需求分析文档.md)
- [系统架构设计](docs/design/01-系统架构设计.md)
- [数据库详细设计](docs/design/02-数据库详细设计.md)
- [UML 设计视图](docs/uml/01-类图与时序图.md)
- [实施计划](docs/plannings/01-实施计划.md)

完整设计文档请查看 [docs/README.md](docs/README.md)

## 🛠️ Make 命令参考

| 命令 | 说明 |
|------|------|
| `make setup` | 一键安装所有依赖，初始化数据库 |
| `make dev` | 同时启动前后端开发服务器 |
| `make dev-backend` | 只启动后端 (FastAPI) |
| `make dev-frontend` | 只启动前端 (Vue) |
| `make stop` | 停止后台服务 |
| `make clean` | 清理构建产物 |
| `make test` | 运行测试套件 |

## 🗺️ 开发路线图

### Phase 1: 基础认证与社区隔离 (P0) - 进行中
- [ ] JWT 用户认证系统
- [ ] 多租户数据隔离
- [ ] 社区管理 CRUD
- [ ] 审计日志系统

### Phase 2: 日历视图与计划发布
- [ ] FullCalendar 日历视图
- [ ] 拖拽式内容排期
- [ ] 定时发布服务

### Phase 3: 看板视图与流程管理
- [ ] Kanban 看板视图
- [ ] 拖拽改变状态
- [ ] 批量操作

### Phase 4: 可视化分析仪表板
- [ ] ECharts 多维度图表
- [ ] 渠道/作者/分类统计
- [ ] 发布趋势分析

详见 [实施计划](docs/plannings/01-实施计划.md)

## 📄 License

[MIT License](LICENSE)

---

<div align="center">

**OmniContent** - Manage All, Publish Everywhere 🚀

Made with ❤️ for Open Source Communities

</div>
