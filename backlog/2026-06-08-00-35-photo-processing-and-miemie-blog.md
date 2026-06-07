## 变更概述

- 新增图片处理机制与协作规范：
  1. 新增 `src/process_images.py` 脚本，基于 ImageMagick 和 ExifTool 对图片进行最大长边 2048px 缩放与 JPEG 95% 格式转换，并在清除 EXIF 时保留 ICC 配置文件、注入版权信息。
  2. 新建 `inbox/` 目录（配置 `.gitignore` 过滤其临时内容），并在 `agents.md` 中补充 “Blog 协作工作流”。
- 实现首篇咩咩介绍博客 (`source/2026-06-08-00-00_miemie-at-2018.md`)：
  1. 导入并处理了 8 张正面横版照片，重命名为 `2026-06-08-00-00_miemie-at-2018_miemie-{1-8}.jpg` 移入 `gallery/`。
  2. 在 YAML Frontmatter 中以 `pageMeta` 格式配置了作者 `sameAs` 与宠物 `owns` 关联。
- 重命名测试文稿（在文件名加 `_` 前缀，包括 `_cute-cats.md`, `_wallpaper-engine.md`, `_line-stickers.md`）以使其在编译结果中不再展示。
- 重构构建脚本 `src/build.py` 与前端 `src/app.js`：
  1. 增强 YAML 解析器以支持字典嵌套和纯字符串列表。
  2. 隔离界面标题 `title` 与 SEO 描述 `alt`（若 `title` 为空则不生成 `.asset-caption` 节点）。
  3. 支持从 `pageMeta` 动态渲染 JSON-LD 结构化数据，并在每次编译前自动清空 `docs/` 目录以防残留。
- 修正首页、导航与外部链接页的 GitHub 链接：
  1. 在 `templates/base.html` 的 `site-nav` 中增加了 `GITHUB` 菜单项，复用原有的极简导航样式，避免了添加突兀的 Footer，保持项目的 Stark Editorial 审美风格。
  2. 修复了 `source/_links.md` 中指向 `.io` 的 broken 链接，将其修正为正确的 GitHub 个人 Profile URL。
- 微调页面视觉排版与可读性：
  1. 将 `src/styles.css` 中全局 Header 的 `h1` 与 `p` 的 `font-weight` 从过细的 `300` 统一调整至适中的 `400`，大幅提升了可读性，同时保留了单色调的静谧感。

## 影响文件

- 新增：`src/process_images.py`、`inbox/.gitkeep`、`source/2026-06-08-00-00_miemie-at-2018.md`、`gallery/2026-06-08-00-00_miemie-at-2018_miemie-*.jpg`
- 修改：`src/build.py`、`src/app.js`、`agents.md`、`.gitignore`、`source/_cute-cats.md`、`source/_wallpaper-engine.md`、`source/_line-stickers.md`、`templates/base.html`、`src/styles.css`、`source/_links.md`
