# 错误响应格式

本文档定义 openGecko API 的错误响应格式。

---

## 标准错误响应

```typescript
interface ErrorResponse {
  detail: string | ValidationError[]
  error_code?: string
}
```

---

## 简单错误

```json
{
  "detail": "Resource not found"
}
```

---

## 验证错误

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "password"],
      "msg": "ensure this value has at least 8 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

---

## 带错误代码

```json
{
  "detail": "Invalid credentials",
  "error_code": "INVALID_CREDENTIALS"
}
```

---

## HTTP 状态码对照表

| 状态码 | 说明 | 常见场景 |
|-------|------|---------|
| 400 | Bad Request | 请求参数格式错误 |
| 401 | Unauthorized | 未认证或 Token 无效 |
| 403 | Forbidden | 无权限访问资源 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突（如重复创建） |
| 422 | Unprocessable Entity | 数据验证失败 |
| 429 | Too Many Requests | 超过速率限制 |
| 500 | Internal Server Error | 服务器内部错误 |

---

**最后更新**：2026-02-09
