> [!IMPORTANT]
> 这是个小型公开项目。
> 我要求所有的文档、过程日志与说明均保持极度精简、克制、平和、去形容词，无需冗长描述。
> 仅提供未来 Agent 检索和理解信息所需的最小说明，记录人类决策即可。
> 用 doc-todo-log-loop skill 在 backlog 记录开发日志。文件名无需额外标题段。
> 用 impeccable skill 微调页面视觉。
> 在所有文档与说明中避免使用 AI/AIGC 相关术语，太无聊了。

## 目录

- [backlog/](./backlog)：存放开发日志 (格式 `YYYY-MM-DD-HH-mm-{简述}.md`) 与待办事项。
- [src/](./src)：前端源码与构建脚本 (`build.py`, `app.js`, `styles.css`)。
- [source/](./source)：原始文章 Markdown 数据源 (需包含 YAML Frontmatter)。
- [gallery/](./gallery)：原始图片与视频。
- [templates/](./templates)：网页 HTML 模板片段。
- [docs/](./docs)：静态构建输出目录 (GitHub Pages 部署根目录)，脚本生成，禁止手动修改。

## 命令

- 构建：`python3 src/build.py`
- 本地预览：`python3 -m http.server 8000 -d docs`
