## 变更概述

- 修改了 `src/build.py`，使构建流程忽略所有以 `_` 开头的 Markdown 文件，防止 `_meta.md` 被解析为文章。
- 成功运行 `python3 src/build.py` 重新构建了静态站点。

## 影响文件

- 修改：`src/build.py`
