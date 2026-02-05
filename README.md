# Community Content Hub

开源社区内容管理与多渠道发布平台。

## 功能

- **内容管理**: 上传 WORD(.docx)/Markdown 文件，自动转换为 Markdown，在线编辑
- **多渠道发布**:
  - 微信公众号 — API 创建草稿，微信后台确认发布
  - Hugo 博客 — 自动生成带 front matter 的 Markdown 文件
  - CSDN — 生成适配格式，一键复制
  - 知乎 — 生成富文本 HTML，一键复制
- **效果追踪**: 发布记录管理，各渠道数据概览
- **内容工作流**: 草稿 → 审核 → 通过 → 发布

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | Python 3.11+ / FastAPI / SQLAlchemy / SQLite |
| 前端 | Vue 3 / TypeScript / Vite / Element Plus |
| WORD 处理 | mammoth / python-docx |
| 部署 | Docker Compose |

## 快速开始

### 开发模式

**后端**:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 编辑配置
uvicorn app.main:app --reload
```

**前端**:

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000（前端开发服务器会代理 API 到后端 8000 端口）。

### Docker 部署

```bash
cp backend/.env.example backend/.env  # 编辑配置
docker compose up -d
```

访问 http://localhost（前端）和 http://localhost:8000/docs（API 文档）。

## 配置说明

在 `backend/.env` 中配置：

| 变量 | 说明 |
|------|------|
| `WECHAT_APP_ID` | 微信公众号 AppID |
| `WECHAT_APP_SECRET` | 微信公众号 AppSecret |
| `HUGO_REPO_PATH` | Hugo 博客仓库本地路径 |
| `HUGO_CONTENT_DIR` | Hugo 内容目录（默认 `content/posts`）|

## API 文档

启动后端后访问 http://localhost:8000/docs 查看 Swagger UI 交互式文档。

## License

MIT
