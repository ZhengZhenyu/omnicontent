# 通用数据模型

本文档定义 OmniContent API 中使用的通用数据模型和 Schema。

---

## 分页响应

所有列表 API 返回的分页响应格式：

```typescript
interface PaginatedResponse<T> {
  items: T[]           // 当前页数据
  total: number        // 总记录数
  page: number         // 当前页码（从 1 开始）
  page_size: number    // 每页数量
  pages: number        // 总页数
}
```

**示例**：

```json
{
  "items": [
    { "id": 1, "title": "Content 1" },
    { "id": 2, "title": "Content 2" }
  ],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```

---

## 时间戳

所有时间戳使用 ISO 8601 格式（UTC）：

```typescript
type Timestamp = string  // "2026-02-09T10:00:00Z"
```

**示例**：

```json
{
  "created_at": "2026-02-09T10:00:00Z",
  "updated_at": "2026-02-09T15:30:00Z"
}
```

---

## ID 字段

所有 ID 使用整数类型：

```typescript
type ID = number
```

---

## 成功响应

简单操作成功响应：

```typescript
interface SuccessResponse {
  message: string
}
```

**示例**：

```json
{
  "message": "Operation completed successfully"
}
```

---

## 最后更新

**最后更新**：2026-02-09
