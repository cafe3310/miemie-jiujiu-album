# 记录：Open Graph 元标签集成与站点全局更名 chocho-miemie-gallery

- **背景**：用户发现项目生成的 HTML 中缺少 Open Graph（`og:` 属性）元标签，不利于在社交平台分享时的富媒体卡片展示；同时用户决定将网站名称、展示文案及硬编码的规范 URL 路径全局彻底更名为 `chocho-miemie-gallery`。
- **问题**：原 HTML 模板与构建脚本仅支持基本元数据；首页的分享标题不够清晰；详情页缺少多图抓取及文章专有元数据（发布时间、作者等）；此外，所有历史代码、配置和静态说明中均残留硬编码的旧域名 `jiujiu-miemie-gallery`。
- **为什么需要这份文档**：本记录整合了 2026-06-10 期间关于 Open Graph 功能开发以及全站重命名重构的两次演进，删除中间过渡状态的冗余记录，清晰记录最终集成逻辑与受影响文件。

## 集成设计与规范

我们为站点定义并生成了以下 Open Graph 属性及配套的 Twitter Card 标签：

| 属性 | 作用 | 详情 |
| :--- | :--- | :--- |
| `og:title` | 页面标题 | 详情页为文章标题，列表页为 `"chocho-miemie gallery, cats of cafe3310"`，链接页为 `"Links"` |
| `og:type` | 页面类型 | 详情页为 `article`，列表页与链接页为 `website` |
| `og:url` | 页面规范 URL | 统一更新为 `https://cafe3310.github.io/chocho-miemie-gallery/...` |
| `og:image` | 预览缩略图 | 支持输出多条 `og:image` 标签以涵盖文章内的全部图片资产，以便分享时进行多图挑选；若无配图，则使用默认封面 `gallery/2026-06-08-00-00_miemie-at-2018_miemie-7.jpg` |
| `og:description` | 页面摘要 | 详情页为文章描述，全站为 "just cats" 等说明 |
| `og:site_name` | 站点名称 | 统一为 `chocho-miemie gallery, cats of cafe3310` |
| `article:published_time` | 文章发布时间 | 仅在 `og:type` 为 `article` 时生成 |
| `article:author` | 文章作者 | 仅在 `og:type` 为 `article` 时生成 |
| `article:section` | 文章所属分类 | 仅在 `og:type` 为 `article` 时生成 |
| `twitter:card` | Twitter 卡片样式 | 设为 `summary_large_image` |
| `twitter:image` | Twitter 预览图 | 默认选用首张代表性图片 |

---

## 变更实施细节

### 1. 模版文件引入占位符
- 在 [templates/base.html](file:///Users/sipan/workspace/_working/jiujiu-miemie-gallery/templates/base.html) 的 `<head>` 中新增了 `<!-- {{META_OG}} -->` 占位符。
- 网页 `<title>` 的展示名后缀改用更为精简的 `chocho-miemie gallery`，而主页大标题 `<h1>` 更名为 `"chocho-miemie gallery, cats of cafe3310"`。

### 2. 构建脚本中 OGP 的动态生成
- 在 [src/build.py](file:///Users/sipan/workspace/_working/jiujiu-miemie-gallery/src/build.py) 中新增并优化了 `generate_og_meta` 函数，支持多图列表作为输入生成多条 `og:image`，并在页面类型为 `article` 时自动追加 `article:*` 专有元数据。
- 修复了 `build.py` 内的 YAML 简易解析器：兼容将 `[]`（如 `assets: []`）解析为真正的空列表对象而非字符串 `"[]"`，消除了啾啾无配图文章在详情页构建时的 `AttributeError` 崩溃。

### 3. 全局更名与规范 URL 替换
- 将构建脚本 `build.py` 中所有硬编码的规范静态 URL 从 `https://cafe3310.github.io/jiujiu-miemie-gallery/` 全面替换为最新的目标仓库路径 `https://cafe3310.github.io/chocho-miemie-gallery/`。
- 将设计规范文件 [DESIGN.md](file:///Users/sipan/workspace/_working/jiujiu-miemie-gallery/DESIGN.md) 和 [.impeccable/design.json](file:///Users/sipan/workspace/_working/jiujiu-miemie-gallery/.impeccable/design.json) 中的设计项目名统一更新为 `chocho-miemie-gallery`。

## 受影响文件

- 修改：`templates/base.html`
- 修改：`src/build.py`
- 修改：`DESIGN.md`
- 修改：`.impeccable/design.json`
- 新增：`backlog/2026-06-10-02-45-open-graph-and-site-rename.md`
- 删除（原过时文档）：`backlog/2026-06-10-01-49-open-graph-meta-tags.md`
- 删除（原过时文档）：`backlog/2026-06-10-02-36-rename-site-to-chocho-miemie.md`
