# 文件上传 API

**负责人**：角色2 - 内容与发布域专家
**模块**：File Upload
**基础路径**：`/api/upload`

---

## 概述

文件上传模块提供图片、文档的上传和格式转换功能。

---

## 端点列表

### 文件上传

- `POST /api/upload/image` - 上传图片
- `POST /api/upload/document` - 上传文档（DOCX、Markdown）
- `POST /api/upload/cover` - 上传封面图

---

## 待完善

此文档模板由角色2（内容与发布域专家）负责完善。

---

## 相关文件

**后端**：
- [backend/app/api/upload.py](../../backend/app/api/upload.py)
- [backend/app/services/converter.py](../../backend/app/services/converter.py)

---

**最后更新**：2026-02-09
