# 多渠道发布 API

**负责人**：角色2 - 内容与发布域专家
**模块**：Multi-channel Publishing
**基础路径**：`/api/publish`

---

## 概述

多渠道发布模块提供将内容发布到微信公众号、Hugo、CSDN、知乎等平台的功能。

---

## 端点列表

### 渠道配置

- `GET /api/publish/channels` - 获取渠道配置列表
- `POST /api/publish/channels` - 创建渠道配置
- `GET /api/publish/channels/{channel_id}` - 获取渠道详情
- `PUT /api/publish/channels/{channel_id}` - 更新渠道配置
- `DELETE /api/publish/channels/{channel_id}` - 删除渠道

### 内容发布

- `POST /api/publish/wechat` - 发布到微信公众号
- `POST /api/publish/hugo` - 发布到 Hugo 博客
- `POST /api/publish/csdn` - 生成 CSDN 格式
- `POST /api/publish/zhihu` - 生成知乎格式

### 发布记录

- `GET /api/publish/records` - 获取发布记录
- `GET /api/publish/records/{record_id}` - 获取发布记录详情

---

## 待完善

此文档模板由角色2（内容与发布域专家）负责完善。

---

## 相关文件

**后端**：
- [backend/app/api/publish.py](../../backend/app/api/publish.py)
- [backend/app/services/wechat.py](../../backend/app/services/wechat.py)
- [backend/app/services/hugo.py](../../backend/app/services/hugo.py)

**前端**：
- [frontend/src/api/publish.ts](../../frontend/src/api/publish.ts)
- [frontend/src/views/PublishView.vue](../../frontend/src/views/PublishView.vue)

---

**最后更新**：2026-02-09
