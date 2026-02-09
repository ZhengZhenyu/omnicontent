# 认证与授权 API

**负责人**：角色1 - 安全域专家
**模块**：Authentication & Security
**基础路径**：`/api/auth`

---

## 概述

认证与授权模块提供用户身份验证、权限管理和安全相关的 API 端点。

---

## 端点列表

### 系统状态

- `GET /api/health` - 系统健康检查

### 用户认证

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `POST /api/auth/refresh` - 刷新 Token
- `POST /api/auth/oauth/{provider}` - OAuth 登录（Google、GitHub）

### 用户管理

- `GET /api/auth/me` - 获取当前用户信息
- `PUT /api/auth/me` - 更新当前用户信息
- `GET /api/users` - 获取用户列表（管理员）
- `POST /api/users` - 创建用户（管理员）
- `GET /api/users/{user_id}` - 获取用户详情（管理员）
- `PUT /api/users/{user_id}` - 更新用户（管理员）
- `DELETE /api/users/{user_id}` - 删除用户（管理员）

### 密码管理

- `POST /api/auth/forgot-password` - 请求密码重置
- `POST /api/auth/reset-password` - 重置密码
- `PUT /api/auth/change-password` - 修改密码

### 初始化

- `POST /api/auth/initial-setup` - 系统初始化（首次创建管理员）
- `GET /api/system/status` - 获取系统状态

---

## 详细 API 文档

### POST /api/auth/login

用户登录，获取 JWT Token。

**权限**：Public（无需认证）

**请求**：

```json
{
  "username": "admin",
  "password": "password123"
}
```

**响应 200**：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**错误响应**：

- **401 Unauthorized**：用户名或密码错误

```json
{
  "detail": "Incorrect username or password"
}
```

**示例**：

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }'
```

---

### GET /api/auth/me

获取当前登录用户的信息。

**权限**：Authenticated

**请求头**：

```
Authorization: Bearer <access_token>
```

**响应 200**：

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "Admin User",
  "is_superuser": true,
  "current_community_id": 1,
  "created_at": "2026-01-01T00:00:00Z"
}
```

**错误响应**：

- **401 Unauthorized**：Token 无效或已过期

**示例**：

```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

---

### POST /api/auth/initial-setup

首次系统初始化，创建管理员账户。只能在系统无用户时调用。

**权限**：Public（仅首次）

**请求**：

```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "secure_password_123",
  "full_name": "System Administrator"
}
```

**响应 201**：

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "System Administrator",
  "is_superuser": true,
  "created_at": "2026-02-09T10:00:00Z"
}
```

**错误响应**：

- **409 Conflict**：系统已初始化

```json
{
  "detail": "System already initialized"
}
```

**示例**：

```bash
curl -X POST http://localhost:8000/api/auth/initial-setup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "secure_password_123",
    "full_name": "System Administrator"
  }'
```

---

### POST /api/auth/forgot-password

请求密码重置，系统会发送重置链接到用户邮箱。

**权限**：Public

**请求**：

```json
{
  "email": "user@example.com"
}
```

**响应 200**：

```json
{
  "message": "Password reset email sent"
}
```

**注意**：即使邮箱不存在，也返回成功（防止用户枚举）

**示例**：

```bash
curl -X POST http://localhost:8000/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

---

### POST /api/auth/reset-password

使用重置 Token 重置密码。

**权限**：Public

**请求**：

```json
{
  "token": "reset_token_from_email",
  "new_password": "new_secure_password"
}
```

**响应 200**：

```json
{
  "message": "Password reset successful"
}
```

**错误响应**：

- **400 Bad Request**：Token 无效或已过期

**示例**：

```bash
curl -X POST http://localhost:8000/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "token": "abc123xyz",
    "new_password": "new_secure_password"
  }'
```

---

### GET /api/users

获取用户列表（管理员功能）。

**权限**：Platform Admin

**查询参数**：

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| `page` | integer | 1 | 页码 |
| `page_size` | integer | 20 | 每页数量 |
| `keyword` | string | - | 搜索关键词（用户名、邮箱） |
| `is_active` | boolean | - | 筛选活跃用户 |

**响应 200**：

```json
{
  "items": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "Admin User",
      "is_superuser": true,
      "is_active": true,
      "created_at": "2026-01-01T00:00:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "page_size": 20,
  "pages": 3
}
```

**错误响应**：

- **403 Forbidden**：非管理员用户

**示例**：

```bash
curl -X GET "http://localhost:8000/api/users?page=1&page_size=20" \
  -H "Authorization: Bearer <admin_token>"
```

---

## 数据模型

### User

```typescript
interface User {
  id: number
  username: string
  email: string
  full_name: string | null
  is_superuser: boolean
  is_active: boolean
  current_community_id: number | null
  created_at: string  // ISO 8601
  updated_at: string  // ISO 8601
}
```

### LoginRequest

```typescript
interface LoginRequest {
  username: string
  password: string
}
```

### LoginResponse

```typescript
interface LoginResponse {
  access_token: string
  token_type: 'bearer'
  expires_in: number  // seconds
}
```

---

## 安全注意事项

1. **密码策略**：
   - 最小长度：8 字符
   - 必须包含：大小写字母、数字
   - 使用 bcrypt 哈希（cost factor 12）

2. **Token 过期**：
   - Access Token：30 分钟
   - Refresh Token：7 天

3. **速率限制**：
   - 登录接口：5 次/分钟（单 IP）
   - 密码重置：3 次/小时（单邮箱）

4. **审计日志**：
   - 所有认证相关操作记录到 `audit` 表

---

## 相关文件

**后端**：
- [backend/app/api/auth.py](../../backend/app/api/auth.py)
- [backend/app/core/security.py](../../backend/app/core/security.py)
- [backend/app/models/user.py](../../backend/app/models/user.py)
- [backend/app/schemas/auth.py](../../backend/app/schemas/auth.py)

**前端**：
- [frontend/src/api/auth.ts](../../frontend/src/api/auth.ts)
- [frontend/src/stores/auth.ts](../../frontend/src/stores/auth.ts)
- [frontend/src/views/Login.vue](../../frontend/src/views/Login.vue)

**测试**：
- [backend/tests/test_auth_api.py](../../backend/tests/test_auth_api.py)

---

**最后更新**：2026-02-09
