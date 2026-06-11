# 站点域名与元数据一致性分析方案

- **背景**：用户要求检查线上站点 `https://cafe3310.github.io/chocho-miemie-album/` 与本地项目 `jiujiu-miemie-gallery` 的情况。
- **问题**：当前存在 4 个不同的站点命名和域名，导致本地编译生成的静态页面中包含大量错误的硬编码域名。
  - 线上实际部署地址：`https://cafe3310.github.io/chocho-miemie-album/`
  - 代码中硬编码域名：`https://cafe3310.github.io/chocho-miemie-gallery/`（见 `src/build.py`）
  - 配置文件所写域名：`https://cafe3310.github.io/jiujiu-miemie-gallery/`（见 `source/_meta.md`）
  - 本地 Git 仓库源：`git@github.com:cafe3310/miemie-jiujiu-album.git`
- **目的**：消除代码中的硬编码，以 `source/_meta.md` 作为唯一配置源动态生成全站的 canonical 链接、Open Graph 标签 and JSON-LD 数据，保证与线上实际部署域名完全一致。

## 实施方案

- 动态解析 `source/_meta.md`：
  - 在 `src/build.py` 中编写对 `source/_meta.md` 的读取与解析逻辑。
  - 提取其中的 `site_url`、`site_name` 与 `site_description` 作为全局配置。
- 消除硬编码：
  - 修改 `get_post_images` 函数，传入 `site_url` 动态拼接。
  - 修改 `generate_og_meta` 函数，其中的 `site_name` 采用动态参数传入。
  - 替换 `build_site` 中所有关于首页和详情页的硬编码 URL。
- 更新元配置：
  - 更新 `source/_meta.md` 中的 `site_url` 值为线上的实际地址 `https://cafe3310.github.io/chocho-miemie-album/`。
  - 统一 `site_name` 为 `chocho-miemie gallery`（与网页展示名保持一致）。
- 重新构建验证：
  - 执行 `python3 src/build.py` 重建静态文件。
  - 验证 `docs/index.html` 中的链接是否正确。
