## 变更概述

- 新增图片处理机制与协作规范：
  1. 新增 `src/process_images.py` 脚本，基于 ImageMagick 和 ExifTool 对图片进行最大长边 2048px 缩放与 JPEG 95% 格式转换，并在清除 EXIF 时保留 ICC 配置文件、注入版权信息。
  2. 新建 `inbox/` 目录（配置 `.gitignore` 过滤其临时内容），并在 `agents.md` 中补充 “Blog 协作工作流”。
- 重构构建脚本 `src/build.py` 与前端 `src/app.js`：
  1. 增强 YAML 解析器以支持字典嵌套和纯字符串列表。
  2. 隔离界面标题 `title` 与 SEO 描述 `alt`（若 `title` 为空则不生成 `.asset-caption` 节点）。
  3. 支持从 `pageMeta` 动态渲染 JSON-LD 结构化数据，并在每次编译前自动清空 `docs/` 目录以防残留。

## 影响文件

- 新增：`src/process_images.py`、`inbox/.gitkeep`、`source/2026-06-08-00-00_miemie-at-2018.md`、`gallery/2026-06-08-00-00_miemie-at-2018_miemie-*.jpg`
- 修改：`src/build.py`、`src/app.js`、`agents.md`、`.gitignore`
