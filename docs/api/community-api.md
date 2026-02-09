# 社区管理 API

**负责人**：角色3 - 治理域专家
**模块**：Community Management
**基础路径**：`/api/communities`

---

## 概述

社区管理模块提供社区的创建、配置和成员管理功能。

---

## 端点列表

### 社区管理

- `GET /api/communities` - 获取社区列表
- `POST /api/communities` - 创建社区
- `GET /api/communities/{community_id}` - 获取社区详情
- `PUT /api/communities/{community_id}` - 更新社区
- `DELETE /api/communities/{community_id}` - 删除社区

### 社区成员

- `GET /api/communities/{community_id}/members` - 获取社区成员
- `POST /api/communities/{community_id}/members` - 添加成员
- `DELETE /api/communities/{community_id}/members/{user_id}` - 移除成员

---

## 待完善

此文档模板由角色3（治理域专家）负责完善。

---

## 相关文件

**后端**：
- [backend/app/api/communities.py](../../backend/app/api/communities.py)
- [backend/app/models/community.py](../../backend/app/models/community.py)

**前端**：
- [frontend/src/api/community.ts](../../frontend/src/api/community.ts)
- [frontend/src/views/CommunityManage.vue](../../frontend/src/views/CommunityManage.vue)

---

**最后更新**：2026-02-09
