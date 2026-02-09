# 治理模块 API

**负责人**：角色3 - 治理域专家
**模块**：Governance Module
**基础路径**：`/api/committees`, `/api/meetings`

---

## 概述

治理模块提供委员会、委员会成员和会议管理功能，支持社区组织的运营管理。

---

## 端点列表

### 委员会管理

- `GET /api/committees` - 获取委员会列表
- `POST /api/committees` - 创建委员会
- `GET /api/committees/{committee_id}` - 获取委员会详情
- `PUT /api/committees/{committee_id}` - 更新委员会
- `DELETE /api/committees/{committee_id}` - 删除委员会
- `GET /api/committees/{committee_id}/members` - 获取委员会成员列表

### 委员会成员管理

- `POST /api/committees/{committee_id}/members` - 添加委员会成员
- `GET /api/committees/{committee_id}/members/{member_id}` - 获取成员详情
- `PUT /api/committees/{committee_id}/members/{member_id}` - 更新成员信息
- `DELETE /api/committees/{committee_id}/members/{member_id}` - 删除成员
- `POST /api/committees/{committee_id}/members/import` - 批量导入成员（CSV）
- `GET /api/committees/{committee_id}/members/export` - 导出成员列表（CSV）

### 会议管理

- `GET /api/meetings` - 获取会议列表
- `POST /api/meetings` - 创建会议
- `GET /api/meetings/{meeting_id}` - 获取会议详情
- `PUT /api/meetings/{meeting_id}` - 更新会议
- `DELETE /api/meetings/{meeting_id}` - 删除会议
- `POST /api/meetings/{meeting_id}/reminders` - 发送会议提醒

---

## 详细 API 文档

### POST /api/committees

创建新的委员会。

**权限**：Community Admin

**请求**：

```json
{
  "name": "技术委员会",
  "slug": "tech-committee",
  "description": "负责技术方向和架构决策",
  "meeting_frequency": "monthly",
  "notification_email": "tech@example.com",
  "notification_wechat": "tech-group-id",
  "established_at": "2026-01-01T00:00:00Z"
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| `name` | string | ✅ | 委员会名称 |
| `slug` | string | ✅ | URL 友好的标识符 |
| `description` | string | ❌ | 委员会描述 |
| `meeting_frequency` | string | ❌ | 会议频率：`weekly`, `monthly`, `quarterly` |
| `notification_email` | string | ❌ | 通知邮箱 |
| `notification_wechat` | string | ❌ | 微信群 ID |
| `established_at` | string | ❌ | 成立日期 |

**响应 201**：

```json
{
  "id": 1,
  "community_id": 1,
  "name": "技术委员会",
  "slug": "tech-committee",
  "description": "负责技术方向和架构决策",
  "meeting_frequency": "monthly",
  "is_active": true,
  "established_at": "2026-01-01T00:00:00Z",
  "created_at": "2026-02-09T10:00:00Z",
  "updated_at": "2026-02-09T10:00:00Z"
}
```

**错误响应**：

- **400 Bad Request**：参数验证失败
- **401 Unauthorized**：未认证
- **403 Forbidden**：非社区管理员
- **409 Conflict**：slug 重复

**示例**：

```bash
curl -X POST http://localhost:8000/api/committees \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "技术委员会",
    "slug": "tech-committee",
    "description": "负责技术方向和架构决策",
    "meeting_frequency": "monthly"
  }'
```

---

### POST /api/committees/{committee_id}/members

添加委员会成员。

**权限**：Community Admin

**请求**：

```json
{
  "name": "张三",
  "email": "zhangsan@example.com",
  "phone": "+86 138 0000 0000",
  "wechat": "zhangsan_wx",
  "organization": "某科技公司",
  "roles": ["主席", "常务委员"],
  "term_start": "2026-01-01",
  "term_end": "2027-12-31",
  "bio": "资深技术专家，拥有20年软件开发经验"
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| `name` | string | ✅ | 成员姓名 |
| `email` | string | ✅ | 邮箱 |
| `phone` | string | ❌ | 电话 |
| `wechat` | string | ❌ | 微信号 |
| `organization` | string | ❌ | 所属组织 |
| `roles` | string[] | ❌ | 角色标签：`["主席", "副主席", "委员", "常务委员"]` |
| `term_start` | string | ❌ | 任期开始日期 |
| `term_end` | string | ❌ | 任期结束日期 |
| `bio` | string | ❌ | 个人简介 |

**响应 201**：

```json
{
  "id": 1,
  "committee_id": 1,
  "name": "张三",
  "email": "zhangsan@example.com",
  "phone": "+86 138 0000 0000",
  "wechat": "zhangsan_wx",
  "organization": "某科技公司",
  "roles": ["主席", "常务委员"],
  "term_start": "2026-01-01",
  "term_end": "2027-12-31",
  "is_active": true,
  "bio": "资深技术专家，拥有20年软件开发经验",
  "created_at": "2026-02-09T10:00:00Z"
}
```

**示例**：

```bash
curl -X POST http://localhost:8000/api/committees/1/members \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "email": "zhangsan@example.com",
    "roles": ["主席"]
  }'
```

---

### POST /api/committees/{committee_id}/members/import

批量导入委员会成员（CSV 文件）。

**权限**：Community Admin

**请求**：

```http
POST /api/committees/1/members/import
Content-Type: multipart/form-data

file: [CSV 文件]
```

**CSV 格式**：

```csv
name,email,phone,wechat,organization,roles,term_start,term_end,bio
张三,zhangsan@example.com,13800000000,zhangsan_wx,某科技公司,"主席,常务委员",2026-01-01,2027-12-31,资深技术专家
李四,lisi@example.com,13900000000,lisi_wx,某咨询公司,副主席,2026-01-01,2027-12-31,行业专家
```

**响应 200**：

```json
{
  "success": 2,
  "failed": 0,
  "errors": [],
  "imported_members": [
    {
      "id": 1,
      "name": "张三",
      "email": "zhangsan@example.com"
    },
    {
      "id": 2,
      "name": "李四",
      "email": "lisi@example.com"
    }
  ]
}
```

**错误响应**：

- **400 Bad Request**：CSV 格式错误
- **413 Payload Too Large**：文件过大（>2MB）

**示例**：

```bash
curl -X POST http://localhost:8000/api/committees/1/members/import \
  -H "Authorization: Bearer <token>" \
  -F "file=@members.csv"
```

---

### POST /api/meetings

创建会议。

**权限**：Community Admin

**请求**：

```json
{
  "committee_id": 1,
  "title": "2026年第一季度技术评审会议",
  "scheduled_at": "2026-03-15T14:00:00Z",
  "location_type": "online",
  "location": "https://zoom.us/j/123456789",
  "agenda": "1. 技术路线图评审\n2. Q1项目总结\n3. Q2规划",
  "reminder_before_hours": [168, 72, 24]
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| `committee_id` | integer | ✅ | 所属委员会 ID |
| `title` | string | ✅ | 会议标题 |
| `scheduled_at` | string | ✅ | 会议时间（ISO 8601） |
| `location_type` | string | ❌ | 会议类型：`online`, `offline`, `hybrid` |
| `location` | string | ❌ | 会议地点或链接 |
| `agenda` | string | ❌ | 会议议程 |
| `reminder_before_hours` | integer[] | ❌ | 提前提醒时间（小时）：`[168, 72, 24]` 表示提前7天、3天、1天 |

**响应 201**：

```json
{
  "id": 1,
  "committee_id": 1,
  "title": "2026年第一季度技术评审会议",
  "scheduled_at": "2026-03-15T14:00:00Z",
  "location_type": "online",
  "location": "https://zoom.us/j/123456789",
  "status": "scheduled",
  "agenda": "1. 技术路线图评审\n2. Q1项目总结\n3. Q2规划",
  "reminder_sent": false,
  "created_at": "2026-02-09T10:00:00Z"
}
```

**会议状态**：

| 状态 | 说明 |
|------|------|
| `scheduled` | 已安排 |
| `in_progress` | 进行中 |
| `completed` | 已完成 |
| `cancelled` | 已取消 |

**示例**：

```bash
curl -X POST http://localhost:8000/api/meetings \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "committee_id": 1,
    "title": "2026年第一季度技术评审会议",
    "scheduled_at": "2026-03-15T14:00:00Z",
    "location_type": "online",
    "location": "https://zoom.us/j/123456789"
  }'
```

---

## 数据模型

### Committee

```typescript
interface Committee {
  id: number
  community_id: number
  name: string
  slug: string
  description: string | null
  is_active: boolean
  meeting_frequency: 'weekly' | 'monthly' | 'quarterly' | null
  notification_email: string | null
  notification_wechat: string | null
  established_at: string | null  // ISO 8601
  created_at: string  // ISO 8601
  updated_at: string  // ISO 8601
}
```

### CommitteeMember

```typescript
interface CommitteeMember {
  id: number
  committee_id: number
  name: string
  email: string
  phone: string | null
  wechat: string | null
  organization: string | null
  roles: string[]  // ["主席", "副主席", "委员", "常务委员"]
  term_start: string | null  // YYYY-MM-DD
  term_end: string | null  // YYYY-MM-DD
  is_active: boolean
  bio: string | null
  avatar_url: string | null
  created_at: string  // ISO 8601
  updated_at: string  // ISO 8601
}
```

### Meeting

```typescript
interface Meeting {
  id: number
  committee_id: number
  title: string
  scheduled_at: string  // ISO 8601
  location_type: 'online' | 'offline' | 'hybrid' | null
  location: string | null
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled'
  agenda: string | null
  minutes: string | null
  attachments: string[] | null
  reminder_sent: boolean
  reminder_before_hours: number[] | null
  created_at: string  // ISO 8601
  updated_at: string  // ISO 8601
}
```

---

## 业务规则

1. **角色管理**：
   - 成员可以有多个角色标签
   - 标准角色：主席、副主席、委员、常务委员
   - 可以自定义其他角色标签

2. **会议提醒**：
   - 默认提醒时间点：7天前、3天前、1天前、2小时前
   - 通过邮件和微信发送提醒
   - 自动记录提醒发送状态

3. **CSV 导入**：
   - 支持批量导入成员信息
   - 重复邮箱自动跳过
   - 返回导入结果和失败详情

---

## 相关文件

**后端**：
- Backend models: [backend/app/models/committee.py](../../backend/app/models/)
- Backend API: [backend/app/api/governance.py](../../backend/app/api/)
- Backend schemas: [backend/app/schemas/governance.py](../../backend/app/schemas/)

**前端**：
- Frontend API: [frontend/src/api/governance.ts](../../frontend/src/api/)
- Committee management: [frontend/src/views/CommitteeManage.vue](../../frontend/src/views/)
- Meeting calendar: [frontend/src/views/Dashboard.vue](../../frontend/src/views/)

**测试**：
- [backend/tests/test_governance_api.py](../../backend/tests/)

**设计文档**：
- [理事会治理模块设计](../design/03-理事会治理模块设计.md)

---

**最后更新**：2026-02-09
