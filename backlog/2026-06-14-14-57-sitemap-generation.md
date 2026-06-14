- **背景**：用户需要为当前的静态博客网站加入 Sitemap 以便于 Google 等搜索引擎抓取。
- **问题**：目前项目在构建时（`src/build.py`）只生成了页面 HTML、样式、脚本和媒体资源，没有生成 `sitemap.xml` 网站地图和引导搜索引擎的 `robots.txt`。
- **目的**：在静态博客构建过程中，基于已有的页面（首页、链接页、所有文章详情页）和动态解析出的 `site_url`，自动生成符合标准规范的 `sitemap.xml` 和 `robots.txt`，输出到 `docs/` 目录。

## 方案设计

1. **Sitemap 结构设计**
   - 首页：`{site_url}index.html`（或 `{site_url}`），通常使用最新文章的更新时间作为它的 `lastmod`。优先级设置为 `1.0`，更新频率 `daily`。
   - 链接页：`{site_url}links.html`。优先级设置为 `0.5`，更新频率 `weekly`。
   - 文章页：`{site_url}posts/{post_id}.html`。使用文章本身的 `date` 作为 `lastmod`。优先级设置为 `0.8`，更新频率 `monthly`。

2. **Robots.txt 设计**
   - 引导搜索引擎爬虫并指向生成的 `sitemap.xml`，格式如下：
     ```text
     User-agent: *
     Allow: /

     Sitemap: {site_url}sitemap.xml
     ```

3. **构建脚本修改**
   - 修改 `src/build.py`，在构建的最后阶段生成这两个文件。
   - 使用 Python 原生库（如 `xml.etree.ElementTree` 或简单的字符串格式化）组装 `sitemap.xml`。由于 sitemap 格式简单稳定，使用格式化 XML 字符串最为直接与便于定制。
