> [!IMPORTANT]
> 这是个小型公开项目。
> 我要求所有的文档、过程日志与说明均保持极度精简、克制、平和、去形容词，无需冗长描述。
> 仅提供未来 Agent 检索和理解信息所需的最小说明，记录人类决策即可。
> 用 doc-todo-log-loop skill 在 backlog 记录开发日志。文件名无需额外标题段。
> 用 impeccable skill 微调页面视觉。
> 在所有文档与说明中避免使用 AI/AIGC 相关术语，太无聊了。

## 目录

- [backlog/](./backlog)：存放开发日志 (格式 `YYYY-MM-DD-HH-mm-{简述}.md`) 与待办事项。
- [src/](./src)：前端源码与构建脚本 (`build.py`, `app.js`, `styles.css`, `process_images.py`)。
- [source/](./source)：原始文章 Markdown 数据源 (需包含 YAML Frontmatter)。
- [gallery/](./gallery)：原始图片与视频。
- [templates/](./templates)：网页 HTML 模板片段。
- [docs/](./docs)：静态构建输出目录 (GitHub Pages 部署根目录)，脚本生成，禁止手动修改。

## 命令

- 构建：`python3 src/build.py`
- 处理图片：`python3 src/process_images.py`
- 本地预览：`python3 -m http.server 8000 -d docs`

## Blog 协作工作流

1. 用户提供博客内容构想，并将原始图片放入项目根目录下的 `inbox/` 目录中。
2. Agent 负责执行以下自动化处理：
   - 运行图片处理脚本对 `inbox/` 内的图片进行缩放、转码与版权注入。
   - 将处理后的图片移动到 `gallery/` 目录。
   - 遵循命名规范：
     - 文章文稿：`source/YYYY-MM-DD-HH-mm-{title}.md`
     - 图片资源：`gallery/YYYY-MM-DD-HH-mm-{title}-{identity_id}.jpg`（`identity_id` 为猫咪身份如 `jiujiu`, `miemie` 或序号）。
   - 结合用户的内容构想，在 `source/` 下生成包含 YAML Frontmatter 的文章 Markdown 模板。
3. Agent 在终端中运行 `zed source/YYYY-MM-DD-HH-mm-{title}.md` 打开生成好的文章，供用户最终编辑。
