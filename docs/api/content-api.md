# 内容管理 API

**负责人**：角色2 - 内容与发布域专家
**模块**：Content Management
**基础路径**：`/api/contents`

---

## 概述

内容管理模块提供内容的创建、编辑、查询和管理功能。

---

## 端点列表

### 内容管理

- `GET /api/contents` - 获取内容列表
- `POST /api/contents` - 创建内容
- `GET /api/contents/{content_id}` - 获取内容详情
- `PUT /api/contents/{content_id}` - 更新内容
- `DELETE /api/contents/{content_id}` - 删除内容
- `POST /api/contents/batch` - 批量上传内容

### 内容搜索

- `GET /api/contents/search` - 搜索内容

---

## 待完善

此文档模板由角色2（内容与发布域专家）负责完善。

请参考 [auth-api.md](./auth-api.md) 和 [governance-api.md](./governance-api.md) 的格式编写详细 API 文档。

---

## 相关文件

**后端**：
- [backend/app/api/contents.py](../../backend/app/api/contents.py)
- [backend/app/models/content.py](../../backend/app/models/content.py)

**前端**：
- [frontend/src/api/content.ts](../../frontend/src/api/content.ts)
- [frontend/src/views/ContentList.vue](../../frontend/src/views/ContentList.vue)
- [frontend/src/views/ContentEdit.vue](../../frontend/src/views/ContentEdit.vue)

---

**最后更新**：2026-02-09
