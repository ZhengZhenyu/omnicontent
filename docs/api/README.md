# openGecko API 文档

本目录包含 openGecko 平台所有 API 端点的详细文档。

---

## 文档结构

```
docs/api/
├── README.md                    # 本文件：API 文档总览
├── auth-api.md                  # 认证与授权 API（角色1负责）
├── content-api.md               # 内容管理 API（角色2负责）
├── community-api.md             # 社区管理 API（角色3负责）
├── governance-api.md            # 治理模块 API（角色3负责）
├── publish-api.md               # 多渠道发布 API（角色2负责）
├── analytics-api.md             # 数据分析 API（角色4负责）
├── upload-api.md                # 文件上传 API（角色2负责）
└── schemas/                     # 共享数据模型定义
    ├── common-schemas.md
    ├── error-responses.md
    └── pagination.md
```

---

## API 模块概览

### 1. 认证与授权 API ([auth-api.md](./auth-api.md))
**负责人**：角色1 - 安全域专家

- 用户注册与初始化
- 用户登录（用户名/密码、OAuth）
- JWT Token 管理
- 密码重置
- 用户管理（CRUD）
- 权限验证

**基础路径**：`/api/auth`

### 2. 社区管理 API ([community-api.md](./community-api.md))
**负责人**：角色3 - 治理域专家

- 社区 CRUD
- 社区成员管理
- 社区切换
- 社区配置

**基础路径**：`/api/communities`

### 3. 内容管理 API ([content-api.md](./content-api.md))
**负责人**：角色2 - 内容与发布域专家

- 内容 CRUD
- 内容列表与搜索
- 内容版本管理
- 标签管理

**基础路径**：`/api/contents`

### 4. 治理模块 API ([governance-api.md](./governance-api.md))
**负责人**：角色3 - 治理域专家

- 委员会管理
- 委员会成员管理
- 会议管理
- 会议提醒
- CSV 批量导入/导出

**基础路径**：`/api/committees`, `/api/meetings`

### 5. 多渠道发布 API ([publish-api.md](./publish-api.md))
**负责人**：角色2 - 内容与发布域专家

- 渠道配置管理
- 内容发布（微信、Hugo、CSDN、知乎）
- 发布记录查询
- 发布预览

**基础路径**：`/api/publish`

### 6. 数据分析 API ([analytics-api.md](./analytics-api.md))
**负责人**：角色4 - 平台与基础设施专家

- 内容统计
- 发布统计
- 用户活跃度分析
- 趋势分析

**基础路径**：`/api/analytics`

### 7. 文件上传 API ([upload-api.md](./upload-api.md))
**负责人**：角色2 - 内容与发布域专家

- 图片上传（封面、内容图片）
- 文档上传（DOCX、Markdown）
- 文件格式转换

**基础路径**：`/api/upload`

---

## API 通用规范

### 基础 URL

```
开发环境：http://localhost:8000
生产环境：https://api.opengecko.com
```

### 认证方式

所有需要认证的 API 使用 **JWT Bearer Token**：

```http
Authorization: Bearer <access_token>
```

获取 Token：

```bash
POST /api/auth/login
{
  "username": "admin",
  "password": "password123"
}

# 响应
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 请求头

| Header | 值 | 说明 |
|--------|---|------|
| `Content-Type` | `application/json` | 请求体格式（除文件上传外） |
| `Authorization` | `Bearer <token>` | JWT Token |
| `Accept` | `application/json` | 期望的响应格式 |
| `X-Community-ID` | `<community_id>` | 可选：指定社区上下文 |

### 响应格式

#### 成功响应

```json
{
  "id": 1,
  "title": "Example Content",
  "created_at": "2026-02-09T10:00:00Z"
}
```

列表响应（带分页）：

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```

#### 错误响应

```json
{
  "detail": "错误描述"
}
```

或（验证错误）：

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### HTTP 状态码

| 状态码 | 说明 | 使用场景 |
|-------|------|---------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 删除成功（无响应体） |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证或 Token 无效 |
| 403 | Forbidden | 无权限访问 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突（如重复创建） |
| 422 | Unprocessable Entity | 数据验证失败 |
| 500 | Internal Server Error | 服务器内部错误 |

### 分页参数

所有列表接口支持分页：

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| `page` | integer | 1 | 页码（从 1 开始） |
| `page_size` | integer | 20 | 每页数量 |
| `keyword` | string | - | 搜索关键词（可选） |

示例：

```http
GET /api/contents?page=2&page_size=50&keyword=技术
```

### 排序参数

| 参数 | 类型 | 说明 |
|-----|------|------|
| `sort_by` | string | 排序字段（如 `created_at`, `title`） |
| `order` | string | 排序方向：`asc` 或 `desc` |

示例：

```http
GET /api/contents?sort_by=created_at&order=desc
```

### 过滤参数

根据具体 API 端点，支持字段过滤：

```http
GET /api/contents?status=published&community_id=1
```

---

## 数据模型约定

### 时间戳格式

所有时间戳使用 **ISO 8601** 格式（UTC 时区）：

```json
{
  "created_at": "2026-02-09T10:00:00Z",
  "updated_at": "2026-02-09T15:30:00Z"
}
```

### ID 类型

所有 ID 使用 **整数**：

```json
{
  "id": 123,
  "user_id": 456,
  "community_id": 789
}
```

### 布尔值

```json
{
  "is_active": true,
  "is_published": false
}
```

### 枚举值

使用字符串枚举：

```json
{
  "status": "draft",  // "draft" | "published" | "archived"
  "role": "admin"     // "admin" | "editor" | "viewer"
}
```

---

## 多租户隔离

openGecko 是多租户 SaaS 平台，所有数据按 `community_id` 隔离。

### 自动隔离

多数 API 会自动根据当前用户的社区上下文进行数据隔离：

```python
# 后端示例
@router.get("/contents")
def get_contents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 自动过滤当前用户社区的内容
    return db.query(Content).filter(
        Content.community_id == current_user.current_community_id
    ).all()
```

### 手动指定社区

管理员可以通过 `X-Community-ID` 请求头切换上下文：

```http
GET /api/contents
X-Community-ID: 5
```

---

## 权限控制

API 端点有不同的权限要求：

| 权限级别 | 说明 | 示例 |
|---------|------|------|
| **Public** | 无需认证 | `/api/health` |
| **Authenticated** | 需要登录 | `/api/contents` |
| **Community Admin** | 社区管理员 | `/api/communities/{id}` PUT |
| **Platform Admin** | 平台管理员 | `/api/users` |

权限在每个 API 文档中明确标注。

---

## 错误处理

### 通用错误码

| 错误代码 | HTTP 状态 | 说明 |
|---------|----------|------|
| `INVALID_CREDENTIALS` | 401 | 用户名或密码错误 |
| `TOKEN_EXPIRED` | 401 | JWT Token 已过期 |
| `PERMISSION_DENIED` | 403 | 无权限执行操作 |
| `RESOURCE_NOT_FOUND` | 404 | 资源不存在 |
| `DUPLICATE_ENTRY` | 409 | 重复的资源 |
| `VALIDATION_ERROR` | 422 | 数据验证失败 |

### 错误响应示例

```json
{
  "detail": "Invalid credentials",
  "error_code": "INVALID_CREDENTIALS"
}
```

---

## 速率限制

为防止滥用，API 有速率限制：

| 用户类型 | 限制 |
|---------|------|
| 未认证用户 | 100 请求/小时 |
| 认证用户 | 1000 请求/小时 |
| 管理员 | 5000 请求/小时 |

超出限制时返回 **429 Too Many Requests**：

```json
{
  "detail": "Rate limit exceeded. Try again in 3600 seconds."
}
```

---

## API 版本控制

当前版本：**v1**

未来如有不兼容变更，将通过路径版本化：

```
/api/v1/contents
/api/v2/contents  # 未来版本
```

---

## 测试与调试

### Swagger UI

访问自动生成的交互式 API 文档：

```
http://localhost:8000/docs
```

### ReDoc

访问另一种风格的 API 文档：

```
http://localhost:8000/redoc
```

### cURL 示例

```bash
# 登录获取 Token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 使用 Token 访问受保护资源
curl -X GET http://localhost:8000/api/contents \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### Python 示例

```python
import requests

# 登录
response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"username": "admin", "password": "admin123"}
)
token = response.json()["access_token"]

# 获取内容列表
response = requests.get(
    "http://localhost:8000/api/contents",
    headers={"Authorization": f"Bearer {token}"}
)
contents = response.json()
```

---

## 贡献指南

### 更新 API 文档

当你添加或修改 API 端点时：

1. **更新对应的 API 文档文件**（如 `auth-api.md`）
2. **遵循统一的文档格式**（见下方模板）
3. **在代码中添加详细的 docstring**
4. **提交 PR 时在描述中说明 API 变更**

### API 文档模板

```markdown
## POST /api/endpoint

**描述**：简要说明此端点的功能

**权限**：Authenticated / Community Admin / Platform Admin

**请求**：

\`\`\`json
{
  "field1": "string",
  "field2": 123
}
\`\`\`

**响应 200**：

\`\`\`json
{
  "id": 1,
  "field1": "string",
  "created_at": "2026-02-09T10:00:00Z"
}
\`\`\`

**错误响应**：

- **400 Bad Request**：参数错误
- **401 Unauthorized**：未认证
- **403 Forbidden**：无权限

**示例**：

\`\`\`bash
curl -X POST http://localhost:8000/api/endpoint \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"field1": "value", "field2": 123}'
\`\`\`
```

---

## 相关资源

- [项目需求文档](../requirements/01-需求分析文档.md)
- [系统设计文档](../design/)
- [团队分工方案](../TEAM_DIVISION_CLAUDE_CODE.md)
- [Git 工作流](../GIT_WORKFLOW.md)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)

---

**文档维护**：各模块 API 文档由对应负责人维护（见各文件开头）

**最后更新**：2026-02-09
