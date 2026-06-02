## 变更概述

- 创建了 `source/_links.md` 文件，将外部链接元数据以 YAML 格式进行配置。
- 修改了 `src/build.py` 中的 `build_site` 函数，使之动态加载并解析 `source/_links.md` 中的链接数据，如果文件不存在则回退至默认配置。
- 重新运行 `python3 src/build.py` 编译生成静态 docs。

## 影响文件

- 新增：`source/_links.md`
- 修改：`src/build.py`
