import os
import re
import json
import html
import copy
import shutil

# 获取 build.py 所在目录的上一级目录作为 repo_root
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source_dir = os.path.join(repo_root, "source")
templates_dir = os.path.join(repo_root, "templates")


# 一个简易的 YAML 解析器
# 一个支持多级嵌套的极简 YAML 解析器
def parse_yaml(yaml_text):
    data = {}
    # stack 元素为 [indent, key, container, type]
    stack = [(0, None, data, 'dict')]
    
    for line in yaml_text.split("\n"):
        if not line.strip() or line.strip().startswith("#"):
            continue
            
        indent = len(line) - len(line.lstrip(' '))
        stripped = line.strip()
        
        # 弹栈到合适的缩进父级
        while len(stack) > 1 and stack[-1][0] > indent:
            stack.pop()
            
        parent_indent, parent_key, parent_container, parent_type = stack[-1]
        
        if stripped.startswith("-"):
            # 如果父容器是 dict 且为空，纠正为 list
            if parent_type == 'dict':
                grand_indent, grand_key, grand_container, grand_type = stack[-2]
                grand_container[parent_key] = []
                stack[-1] = (parent_indent, parent_key, grand_container[parent_key], 'list')
                parent_container = grand_container[parent_key]
                parent_type = 'list'
                
            val_part = stripped[1:].strip()
            # 键值对列表项，如 - url: ...
            m = re.match(r'^([^:]+):\s+(.*)$', val_part)
            if m:
                k = m.group(1).strip()
                v = m.group(2).strip().strip('"').strip("'")
                item = {k: v}
                parent_container.append(item)
                stack.append((indent + 2, len(parent_container) - 1, item, 'dict'))
            else:
                # 纯字符串列表元素，如 - "https://..."
                v = val_part.strip('"').strip("'")
                parent_container.append(v)
            continue
            
        # 普通键值对，如 key: val
        m = re.match(r'^([^:]+):(.*)$', stripped)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            
            if val == "":
                parent_container[key] = {}
                stack.append((indent + 2, key, parent_container[key], 'dict'))
            else:
                v = val.strip('"').strip("'")
                if v == "[]":
                    parent_container[key] = []
                elif v == "{}":
                    parent_container[key] = {}
                else:
                    parent_container[key] = v
                
    return data

# 一个极简的 Markdown 到 HTML 解析器
def markdown_to_html(md_text):
    lines = md_text.split("\n")
    html_lines = []
    in_code_block = False
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith("```"):
            if in_code_block:
                in_code_block = False
                html_lines.append("</code></pre>")
            else:
                in_code_block = True
                html_lines.append("<pre><code>")
            continue
            
        if in_code_block:
            html_lines.append(html.escape(line))
            continue
            
        # 处理标题 ### 
        if stripped.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_content = html.escape(stripped[4:])
            html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
            html_lines.append(f"<h3>{html_content}</h3>")
            continue
            
        # 处理列表 * 或 -
        if stripped.startswith("* ") or stripped.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_content = html.escape(stripped[2:])
            html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
            html_lines.append(f"<li>{html_content}</li>")
            continue
            
        # 处理数字列表 1.
        if re.match(r'^\d+\.\s+', stripped):
            content = re.sub(r'^\d+\.\s+', '', stripped)
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_content = html.escape(content)
            html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
            html_lines.append(f"<li>{html_content}</li>")
            continue
            
        # 处理普通空行
        if stripped == "":
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue
            
        # 行内 code 替换为 <code>
        parts = stripped.split("`")
        if len(parts) > 1:
            processed = ""
            for idx, part in enumerate(parts):
                if idx % 2 == 1:
                    processed += f"<code>{html.escape(part)}</code>"
                else:
                    escaped_part = html.escape(part)
                    escaped_part = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', escaped_part)
                    processed += escaped_part
            html_lines.append(f"<p>{processed}</p>")
        else:
            html_content = html.escape(stripped)
            html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
            html_lines.append(f"<p>{html_content}</p>")
            
    if in_list:
        html_lines.append("</ul>")
        
    return "\n".join(html_lines)

# 统一渲染模板渲染器
def generate_og_meta(title, description, url, image_url, page_type="website", article_meta=None):
    if isinstance(image_url, list):
        images = image_url
    else:
        images = [image_url] if image_url else []

    lines = [
        f'<meta property="og:title" content="{html.escape(title)}">',
        f'<meta property="og:type" content="{html.escape(page_type)}">',
        f'<meta property="og:url" content="{html.escape(url)}">',
    ]
    for img in images:
        lines.append(f'<meta property="og:image" content="{html.escape(img)}">')

    lines.extend([
        f'<meta property="og:description" content="{html.escape(description)}">',
        '<meta property="og:site_name" content="chocho-miemie gallery, cats of cafe3310">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{html.escape(title)}">',
        f'<meta name="twitter:description" content="{html.escape(description)}">'
    ])

    if images:
        lines.append(f'<meta name="twitter:image" content="{html.escape(images[0])}">')

    if page_type == "article" and article_meta:
        if article_meta.get("published_time"):
            lines.append(f'<meta property="article:published_time" content="{html.escape(article_meta["published_time"])}">')
        if article_meta.get("author"):
            lines.append(f'<meta property="article:author" content="{html.escape(article_meta["author"])}">')
        if article_meta.get("section"):
            lines.append(f'<meta property="article:section" content="{html.escape(article_meta["section"])}">')

    return "\n  ".join(lines)


def render_page(content, title, description, path_prefix, nav_notes_active, nav_links_active, json_ld, base_template, meta_og=""):
    page = base_template
    page = page.replace("<!-- {{TITLE}} -->", title)
    page = page.replace("<!-- {{META_DESCRIPTION}} -->", description)
    page = page.replace("<!-- {{NAV_NOTES_ACTIVE}} -->", "active" if nav_notes_active else "")
    page = page.replace("<!-- {{NAV_LINKS_ACTIVE}} -->", "active" if nav_links_active else "")
    page = page.replace("<!-- {{CONTENT}} -->", content)
    page = page.replace("<!-- {{PATH_PREFIX}} -->", path_prefix)
    
    json_ld_str = f'<script type="application/ld+json">\n{json.dumps(json_ld, ensure_ascii=False, indent=2)}\n</script>'
    page = page.replace("<!-- {{JSON_LD}} -->", json_ld_str)
    page = page.replace("<!-- {{META_OG}} -->", meta_og)
    
    return page

def build_site():
    print("Building static site...")
    posts = []
    
    # 动态加载外部链接
    external_links = []
    links_path = os.path.join(source_dir, "_links.md")
    if os.path.exists(links_path):
        try:
            with open(links_path, 'r', encoding='utf-8') as f:
                content = f.read()
            parts = content.split("---")
            if len(parts) >= 3:
                meta = parse_yaml(parts[1])
                external_links = meta.get("links", [])
        except Exception as e:
            print(f"Error parsing _links.md: {e}")
            
    if not external_links:
        external_links = [
            {"name": "My Personal Portfolio", "url": "https://cafe3310.github.io/"},
            {"name": "Prompts Sharing", "url": "https://prompts.cafe3310.com/"},
            {"name": "Hugging Face Model Hub", "url": "https://huggingface.co/cafe3310"}
        ]
    
    if not os.path.exists(source_dir):
        print("Source directory does not exist.")
        return
        
    files = sorted(os.listdir(source_dir))
    for f in files:
        if not f.endswith(".md") or f.startswith("_"):
            continue
            
        path = os.path.join(source_dir, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # 拆分 Frontmatter
        parts = content.split("---")
        if len(parts) >= 3:
            yaml_text = parts[1]
            md_text = "---".join(parts[2:])
            
            meta = parse_yaml(yaml_text)
            body_html = markdown_to_html(md_text)
            
            meta["bodyHtml"] = body_html
            meta["filename"] = f
            posts.append(meta)
            print(f"  Parsed post: {meta.get('title')}")
            
    # 对 posts 按日期和文件名降序排列（确保同日期的文章以文件名的时间戳先后排序，最新的在顶上）
    posts.sort(key=lambda x: (x.get("date", ""), x.get("filename", "")), reverse=True)

    # 确保 docs/ 文件夹存在（在编译前先清空 docs 目录以清除历史残留文件）
    docs_dir = os.path.join(repo_root, "docs")
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir, ignore_errors=True)
        
    posts_output_dir = os.path.join(docs_dir, "posts")
    os.makedirs(posts_output_dir, exist_ok=True)

    # 读取所有 HTML 模板
    with open(os.path.join(templates_dir, "base.html"), 'r', encoding='utf-8') as f:
        base_template = f.read()
    with open(os.path.join(templates_dir, "index.html"), 'r', encoding='utf-8') as f:
        index_content_template = f.read()
    with open(os.path.join(templates_dir, "links.html"), 'r', encoding='utf-8') as f:
        links_content_template = f.read()
    with open(os.path.join(templates_dir, "post.html"), 'r', encoding='utf-8') as f:
        post_content_template = f.read()

    # 1. 生成 index.html (NOTES 列表页)
    post_list_html = []
    for post in posts:
        post_list_html.append(f"""
        <article class="post-item">
          <a href="posts/{post.get('id')}.html" style="text-decoration: none; color: inherit; display: block;">
            <h2 class="post-title">{post.get('title')}</h2>
            <p class="post-desc">{post.get('description')}</p>
          </a>
        </article>
        """)
    post_list_str = "\n".join(post_list_html)
    index_content = index_content_template.replace("<!-- {{POST_LIST}} -->", post_list_str)

    # index JSON-LD 包含 Website 和全部文章的文章列表描述，利于搜索引擎识别和抓取
    index_json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": "https://cafe3310.github.io/chocho-miemie-gallery/#website",
                "name": "chocho-miemie gallery, cats of cafe3310",
                "url": "https://cafe3310.github.io/chocho-miemie-gallery/",
                "description": "原创角色 chocho & miemie 的画廊、LoRA 经验与微调经验分享 Playground。"
            }
        ]
    }
    for post in posts:
        index_json_ld["@graph"].append({
            "@type": "TechArticle",
            "headline": post.get("title"),
            "description": post.get("description"),
            "datePublished": post.get("date"),
            "url": f"https://cafe3310.github.io/chocho-miemie-gallery/posts/{post.get('id')}.html",
            "author": {
                "@type": "Person",
                "name": post.get("author") or "cafe3310"
            }
        })

    index_meta_og = generate_og_meta(
        title="chocho-miemie gallery, cats of cafe3310",
        description="just cats",
        url="https://cafe3310.github.io/chocho-miemie-gallery/index.html",
        image_url="https://cafe3310.github.io/chocho-miemie-gallery/gallery/2026-06-08-00-00_miemie-at-2018_miemie-7.jpg",
        page_type="website"
    )

    index_html_output = render_page(
        content=index_content,
        title="Notes",
        description="just cats",
        path_prefix=".",
        nav_notes_active=True,
        nav_links_active=False,
        json_ld=index_json_ld,
        base_template=base_template,
        meta_og=index_meta_og
    )
    with open(os.path.join(docs_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html_output)
    print("  Generated index.html")

    # 2. 生成 links.html (LINKS 频道页)
    links_html = []
    for link in external_links:
        links_html.append(f"""
        <a href="{link['url']}" target="_blank" rel="noopener noreferrer" class="link-card">
          <span class="link-card-title">{link['name']}</span>
          <span class="link-card-url">{link['url'].replace("https://", "")} &rarr;</span>
        </a>
        """)
    links_str = "\n".join(links_html)
    links_content = links_content_template.replace("<!-- {{LINKS_LIST}} -->", links_str)

    links_json_ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Links - chocho-miemie gallery",
        "description": "Other channels and resources for chocho-miemie gallery, cats of cafe3310",
        "url": "https://cafe3310.github.io/chocho-miemie-gallery/links.html"
    }

    links_meta_og = generate_og_meta(
        title="Links",
        description="Other channels and resources for chocho-miemie gallery, cats of cafe3310",
        url="https://cafe3310.github.io/chocho-miemie-gallery/links.html",
        image_url="https://cafe3310.github.io/chocho-miemie-gallery/gallery/2026-06-08-00-00_miemie-at-2018_miemie-7.jpg",
        page_type="website"
    )

    links_html_output = render_page(
        content=links_content,
        title="Links",
        description="Other channels and resources for chocho-miemie gallery, cats of cafe3310",
        path_prefix=".",
        nav_notes_active=False,
        nav_links_active=True,
        json_ld=links_json_ld,
        base_template=base_template,
        meta_og=links_meta_og
    )
    with open(os.path.join(docs_dir, "links.html"), 'w', encoding='utf-8') as f:
        f.write(links_html_output)
    print("  Generated links.html")

    # 3. 生成详情页 (posts/<post_id>.html)
    for post in posts:
        # 组装画廊项目，并将路径映射至父级目录（../gallery/...）
        gallery_items = []
        for idx, asset in enumerate(post.get("assets", [])):
            url = asset.get("url", "")
            if url.startswith("./"):
                url = "../" + url[2:]
            
            alt_text = asset.get("alt") or asset.get("title") or ""
            if post.get("assetsType") == "video":
                media_html = f'<video src="{url}" autoplay loop muted playsinline></video>'
                item_class = "gallery-item video-item"
            else:
                media_html = f'<img src="{url}" alt="{html.escape(alt_text)}" loading="lazy">'
                item_class = "gallery-item"
                
            caption_html = ""
            if asset.get("title"):
                caption_html = f'<div class="asset-caption">{html.escape(asset.get("title"))}</div>'
                
            gallery_items.append(f"""
            <div class="gallery-container">
              <div class="{item_class}" data-idx="{idx}">
                {media_html}
              </div>
              {caption_html}
            </div>
            """)
        post_gallery_str = "\n".join(gallery_items)

        # 构造复制给 JS 运行态的数据（里面的 asset 同样也需要重映射路径以供 modal 正确调用）
        post_data_copy = copy.deepcopy(post)
        for asset in post_data_copy.get("assets", []):
            if asset.get("url", "").startswith("./"):
                asset["url"] = "../" + asset["url"][2:]

        # 填充 post.html 局部模板
        post_content = post_content_template
        post_content = post_content.replace("<!-- {{POST_DATE}} -->", post.get("date", ""))
        post_content = post_content.replace("<!-- {{POST_CATEGORY}} -->", post.get("category", ""))
        post_content = post_content.replace("<!-- {{POST_TITLE}} -->", post.get("title", ""))
        post_content = post_content.replace("<!-- {{POST_BODY}} -->", post.get("bodyHtml", ""))
        post_content = post_content.replace("<!-- {{POST_GALLERY}} -->", post_gallery_str)
        post_content = post_content.replace("<!-- {{POST_DATA_JSON}} -->", json.dumps(post_data_copy, ensure_ascii=False))

        # 动态从 pageMeta 中提取并组装作者及关联数据 (sameAs, owns 等)
        page_meta = post.get("pageMeta")
        if not isinstance(page_meta, dict):
            page_meta = {}
            
        author_data = {
            "@type": "Person",
            "name": page_meta.get("author") or post.get("author") or "cafe3310"
        }
        
        same_as = page_meta.get("authorSameAs") or page_meta.get("sameAs")
        if same_as:
            if isinstance(same_as, str):
                same_as = [s.strip() for s in same_as.split(",") if s.strip()]
            author_data["sameAs"] = same_as
            
        owns = page_meta.get("owns")
        if owns:
            owns_list = []
            for item in owns:
                if isinstance(item, dict):
                    owns_list.append({
                        "@type": "Thing",
                        "name": item.get("name", ""),
                        "description": item.get("description", "")
                    })
            author_data["owns"] = owns_list

        # 为该篇文章配置极度具体的 TechArticle / BlogPosting JSON-LD 描述，以包含它独特的媒体资产
        post_json_ld = {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": post.get("title"),
            "description": post.get("description"),
            "datePublished": post.get("date"),
            "url": f"https://cafe3310.github.io/chocho-miemie-gallery/posts/{post.get('id')}.html",
            "author": author_data,
            "about": [
                {
                    "@type": "ImageObject" if post.get("assetsType") == "image" else "VideoObject",
                    "name": asset.get("title") or asset.get("alt") or "",
                    "caption": asset.get("title") or asset.get("alt") or "",
                    "contentUrl": f"https://cafe3310.github.io/chocho-miemie-gallery{asset.get('url')[1:]}"
                } for asset in post.get("assets", [])
            ]
        }

        # 寻找所有资产作为 og:image
        post_images = []
        assets = post.get("assets", [])
        if assets and post.get("assetsType") == "image":
            for asset in assets:
                first_asset_url = asset.get("url", "")
                if first_asset_url.startswith("./"):
                    post_images.append("https://cafe3310.github.io/chocho-miemie-gallery/" + first_asset_url[2:])
                elif first_asset_url.startswith("gallery/"):
                    post_images.append(f"https://cafe3310.github.io/chocho-miemie-gallery/{first_asset_url}")

        if not post_images:
            post_images.append("https://cafe3310.github.io/chocho-miemie-gallery/gallery/2026-06-08-00-00_miemie-at-2018_miemie-7.jpg")

        article_meta = {
            "published_time": post.get("date"),
            "author": post.get("author") or "cafe3310",
            "section": post.get("category")
        }

        post_meta_og = generate_og_meta(
            title=post.get("title", ""),
            description=post.get("description", ""),
            url=f"https://cafe3310.github.io/chocho-miemie-gallery/posts/{post.get('id')}.html",
            image_url=post_images,
            page_type="article",
            article_meta=article_meta
        )

        # 调用 render_page 生成最终 the HTML 文件内容
        post_html_output = render_page(
            content=post_content,
            title=post.get("title", ""),
            description=post.get("description", ""),
            path_prefix="..",
            nav_notes_active=True,
            nav_links_active=False,
            json_ld=post_json_ld,
            base_template=base_template,
            meta_og=post_meta_og
        )

        post_output_path = os.path.join(posts_output_dir, f"{post.get('id')}.html")
        with open(post_output_path, 'w', encoding='utf-8') as f:
            f.write(post_html_output)
        print(f"  Generated posts/{post.get('id')}.html")

    # 4. 拷贝脚本、样式及 gallery 资产
    src_app = os.path.join(repo_root, "src", "app.js")
    src_css = os.path.join(repo_root, "src", "styles.css")
    
    if os.path.exists(src_app):
        shutil.copy(src_app, os.path.join(docs_dir, "app.js"))
        print("  Copied app.js to docs/")
    if os.path.exists(src_css):
        shutil.copy(src_css, os.path.join(docs_dir, "styles.css"))
        print("  Copied styles.css to docs/")
        
    src_gallery = os.path.join(repo_root, "gallery")
    if os.path.exists(src_gallery):
        dest_gallery = os.path.join(docs_dir, "gallery")
        if os.path.exists(dest_gallery):
            shutil.rmtree(dest_gallery)
        shutil.copytree(src_gallery, dest_gallery)
        print("  Copied gallery/ to docs/gallery/")

    # 5. 拷贝根目录下的 Google 验证文件（如 google*.html）
    for file_name in os.listdir(repo_root):
        if file_name.startswith("google") and file_name.endswith(".html"):
            src_file = os.path.join(repo_root, file_name)
            dest_file = os.path.join(docs_dir, file_name)
            shutil.copy(src_file, dest_file)
            print(f"  Copied verification file: {file_name} to docs/")

    print(f"Site built successfully! Output root: {docs_dir}")

if __name__ == "__main__":
    build_site()
