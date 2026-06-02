## 变更概述

- 重构 `templates/post.html`，将 `gallery-section` 移动到 `post-content` 上方，实现图片展示置于文字内容顶部。
- 修改 `src/styles.css`，为 `.gallery-section` 增加 `margin-bottom: 3.5rem` 的间距。
- 简化 `source/cute-cats.md`、`source/line-stickers.md` 与 `source/wallpaper-engine.md` 内的文章正文及 metadata 标题/描述为极简的 1-2 句占位文字。
- 执行 `python3 src/build.py` 重新编译生成静态站点至 `docs/`。

## 影响文件

- 修改：`templates/post.html`
- 修改：`src/styles.css`
- 修改：`source/cute-cats.md`
- 修改：`source/line-stickers.md`
- 修改：`source/wallpaper-engine.md`
