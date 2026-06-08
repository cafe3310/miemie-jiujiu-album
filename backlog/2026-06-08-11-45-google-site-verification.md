# 记录：Google Search Console 所有权验证配置

- **背景**：用户需要为托管在 GitHub Pages 的 `jiujiu-miemie-gallery` 静态站点验证 Google 搜索引擎的所有权。
- **问题**：Google 的所有权验证需要将一个特定的 HTML 验证文件放在站点的根目录下。然而，目前的构建脚本 `src/build.py` 在编译前会清空整个 `docs/` 目录，这会导致手动放入 `docs/` 的验证文件在下次构建时被删除。
- **为什么需要这份文档**：本记录旨在登记为了解决该问题对构建脚本所做的调整，以及验证文件在项目结构中的存储方案，保证后续构建和部署的一致性。

## 变更概述

- 将 Google 验证文件 `google76add3f4cabc303f.html` 从临时缓冲区 `inbox/` 移动至项目根目录，作为持久保留的验证资源。
- 修改构建脚本 `src/build.py`：
  1. 在每次构建的最后阶段，扫描项目根目录下所有符合 `google*.html` 命名规则的验证文件。
  2. 自动将其复制到输出目录 `docs/` 下，防止在 `docs/` 被清空重建时丢失。
- 运行构建脚本完成重新编译，验证了 `docs/google76add3f4cabc303f.html` 的正确生成。

## 影响文件

- 新增（移动自 `inbox/`）：`google76add3f4cabc303f.html` (项目根目录下)
- 修改：`src/build.py`
- 新增：`backlog/2026-06-08-11-45-google-site-verification.md`
