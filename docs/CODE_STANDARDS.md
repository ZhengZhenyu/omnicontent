# 代码规范与安全指南

本文档为 openGecko 项目提供代码规范和安全最佳实践指南。

## SQL 查询规范

### 优先使用 ORM

尽量使用 SQLAlchemy ORM 进行数据库查询，而不是原始 SQL：

```python
# ✅ 推荐：使用 ORM
task = db.query(DesignTask).filter(
    DesignTask.id == task_id,
    DesignTask.community_id == community_id
).first()

# 获取关联数据
user_role = db.query(community_users.c.role).filter(
    community_users.c.user_id == user_id,
    community_users.c.community_id == community_id
).scalar()
```

### 何时可以使用原始 SQL

在以下情况下可以使用 `db.execute()` + `text()`：

1. 复杂的聚合查询需要优化性能时
2. 需要使用原生 SQL 特定功能时

使用原始 SQL 时必须：

- ✅ 使用参数化查询（`:param` 语法）
- ❌ 禁止字符串拼接构建 SQL
- ✅ 使用 `text()` 包装 SQL 字符串
- ✅ 对结果进行验证

```python
# ✅ 正确：参数化查询
from sqlalchemy import text

row = db.execute(
    text("SELECT role FROM community_users WHERE user_id = :uid AND community_id = :cid"),
    {"uid": user_id, "cid": community_id}
).fetchone()

# ❌ 错误：字符串拼接（SQL 注入风险！）
sql = f"SELECT role FROM community_users WHERE user_id = {user_id}"
```

### 统一导入风格

在文件顶部统一导入所需的模块：

```python
from sqlalchemy import select, text
from sqlalchemy.orm import Session
```

---

## 敏感信息处理

### 配置密钥管理

1. **禁止使用默认密钥**：生产环境必须修改所有默认密码和密钥

   ```env
   # ❌ 禁止使用
   JWT_SECRET_KEY=change-me-in-production-please-use-a-strong-secret-key
   DEFAULT_ADMIN_PASSWORD=admin123
   
   # ✅ 必须修改为随机字符串
   JWT_SECRET_KEY=<openssl rand -hex 32生成的值>
   ```

2. **密钥派生**：如果需要从主密钥派生其他加密密钥，确保使用独立的盐值：

   ```python
   # 不要直接从 JWT_SECRET_KEY 派生加密密钥
   # 建议在环境变量中单独配置
   ENCRYPTION_KEY=<独立的加密密钥>
   ```

### 凭证存储

- 所有敏感凭证（API Key、Token、密码）必须加密存储
- API 响应中必须脱敏（如显示末 4 位）
- 日志中禁止记录敏感信息

---

## API 安全

### 速率限制

项目已集成 slowapi 速率限制，确保：

1. 登录接口使用 `RATE_LIMIT_LOGIN` 限制
2. 其他接口使用 `RATE_LIMIT_DEFAULT` 限制
3. 在 `main.py` 中正确挂载中间件

```python
from app.core.rate_limit import limiter

@router.post("/login")
@limiter.limit(settings.RATE_LIMIT_LOGIN)
async def login(request: Request):
    ...
```

### 输入验证

- 所有用户输入必须通过 Pydantic Schema 验证
- 使用 `Field` 定义验证规则
- 禁止直接信任用户输入

---

## 错误处理

### 生产环境

- 确保 `DEBUG=False`
- 错误响应不泄露敏感信息（堆栈、路径、内部配置）
- 统一错误响应格式

```python
# 统一错误响应
{
    "detail": "请求参数无效",
    "error_code": "VALIDATION_ERROR"
}
```

---

## 依赖安全

定期检查依赖漏洞：

```bash
pip-audit
# 或
safety check
```

更新依赖时注意：

- 检查 changelog
- 小版本升级相对安全
- 大版本升级需完整测试

---

## 前端安全

### 认证令牌

- Token 存储在 localStorage（注意 XSS 风险）
- 敏感操作需要二次验证
- 登出时清除所有认证信息

### 社区隔离

前端传入的 `X-Community-Id` 不能完全信任，后端必须验证：

```python
async def get_current_community(
    x_community_id: int = Header(...),
    db: Session = Depends(get_db),
) -> int:
    # 后端必须验证用户是否属于该社区
    # 不能直接信任前端传入的值
```

---

## 附录：常用安全检查命令

```bash
# 代码格式化
black app/

# 代码检查
ruff check app/

# 类型检查
mypy app/ --ignore-missing-imports

# 依赖漏洞检查
pip-audit

# 安全依赖检查
safety check
```