#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import shutil

# 默认版权信息
DEFAULT_ARTIST = "cafe3310"
DEFAULT_COPYRIGHT = "© 2026 cafe3310. Licensed under CC BY-NC-SA 4.0."

def check_dependencies():
    """检查 magick (ImageMagick) 和 exiftool 是否可用"""
    magick_ok = shutil.which("magick") is not None
    # 兼容较旧版本的 convert 命令
    convert_ok = shutil.which("convert") is not None or magick_ok
    exiftool_ok = shutil.which("exiftool") is not None
    
    if not (magick_ok or convert_ok):
        print("错误: 未找到 ImageMagick (magick 或 convert)。请先安装 ImageMagick。", file=sys.stderr)
        sys.exit(1)
    if not exiftool_ok:
        print("错误: 未找到 exiftool。请先安装 exiftool。", file=sys.stderr)
        sys.exit(1)
    return "magick" if magick_ok else "convert"

def get_image_info(cmd_name, file_path):
    """获取图片的宽度、高度和格式。返回 (width, height, format)"""
    try:
        # 使用 identify 获取图片宽度、高度和格式名
        cmd = [cmd_name, "identify", "-format", "%[width] %[height] %m", file_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        parts = result.stdout.strip().split()
        if len(parts) >= 3:
            w = int(parts[0])
            h = int(parts[1])
            fmt = parts[2].upper()
            return w, h, fmt
    except Exception as e:
        print(f"获取图片信息失败 {file_path}: {e}", file=sys.stderr)
    return None

def process_single_image(cmd_name, file_path, output_dir=None, artist=DEFAULT_ARTIST, copyright_text=DEFAULT_COPYRIGHT):
    """处理单张图片"""
    info = get_image_info(cmd_name, file_path)
    if not info:
        return False
    
    w, h, fmt = info
    max_dim = max(w, h)
    is_jpeg = fmt in ("JPEG", "JPG")
    
    # 决定输出路径
    file_dir, file_name = os.path.split(file_path)
    base_name, _ = os.path.splitext(file_name)
    target_ext = ".jpg"
    
    if output_dir:
        out_dir = output_dir
    else:
        out_dir = file_dir
        
    output_path = os.path.join(out_dir, base_name + target_ext)
    
    need_resize = max_dim > 2048
    need_convert = not is_jpeg
    
    # 如果是 JPEG 且最长边 <= 2048，则直接复制（或原地跳过），保留原始无损质量
    if is_jpeg and not need_resize:
        if file_path != output_path:
            shutil.copy2(file_path, output_path)
            print(f"-> 复制 JPEG 并保留原始质量: {file_name}")
        else:
            print(f"-> JPEG 规格已符合要求，跳过缩放与转换: {file_name}")
    else:
        # 需要处理（缩放或格式转换）
        action_str = []
        if need_resize:
            action_str.append(f"缩放最长边至 2048px (原图 {w}x{h})")
        if need_convert:
            action_str.append(f"转换格式为 JPEG (原格式 {fmt})")
        
        print(f"-> 处理中 ({', '.join(action_str)}): {file_name}")
        
        # 使用 ImageMagick 转换/缩放。> 语法确保只有在大图时才缩小
        im_cmd = [cmd_name, file_path, "-resize", "2048x2048>", "-quality", "95", output_path]
        try:
            subprocess.run(im_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"ImageMagick 处理失败 {file_path}: {e}", file=sys.stderr)
            return False
            
        # 如果是原地处理，且原图是非 JPEG 格式，转换成功后删除原非 JPEG 格式文件
        if not output_dir and need_convert and os.path.exists(output_path):
            try:
                os.remove(file_path)
                print(f"   已删除原非 JPEG 文件: {file_name}")
            except Exception as e:
                print(f"   删除原非 JPEG 文件失败: {e}", file=sys.stderr)

    # 统一使用 exiftool 清理 exif 并写入版权。--icc_profile:all 选项用于保留色彩配置文件以防止偏色
    et_cmd = [
        "exiftool",
        "-all=",
        "--icc_profile:all",
        f"-Copyright={copyright_text}",
        f"-Artist={artist}",
        f"-By-line={artist}",
        f"-CopyrightNotice={copyright_text}",
        f"-Creator={artist}",
        f"-Rights={copyright_text}",
        "-overwrite_original",
        output_path
    ]
    
    try:
        subprocess.run(et_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
        print(f"   已清理 EXIF 并写入版权: {artist}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"exiftool 写入版权失败 {output_path}: {e.stderr.decode().strip()}", file=sys.stderr)
        return False

def main():
    cmd_name = check_dependencies()
    
    parser = argparse.ArgumentParser(description="画廊图片统一处理工具：最长边2048px，保留原JPEG质量，其他格式转95% JPEG，移除敏感元数据（保留色彩配置文件）并注入版权信息。")
    parser.add_argument("paths", nargs="*", help="输入的文件或目录路径。如果为空，默认处理 gallery 目录。")
    parser.add_argument("-o", "--output", help="输出目录。如果不指定，则原地覆盖（并自动清理非 JPEG 原图）。")
    parser.add_argument("-a", "--artist", default=DEFAULT_ARTIST, help=f"创作者名称 (默认: {DEFAULT_ARTIST})")
    parser.add_argument("-c", "--copyright", default=DEFAULT_COPYRIGHT, help=f"版权声明文本 (默认: {DEFAULT_COPYRIGHT})")
    
    args = parser.parse_args()
    
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_gallery = os.path.join(repo_root, "gallery")
    
    input_paths = args.paths
    if not input_paths:
        input_paths = [default_gallery]
        print(f"未指定输入路径，默认处理项目 gallery 目录: {default_gallery}")
        
    supported_extensions = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".tiff")
    files_to_process = []
    
    for path in input_paths:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for f in files:
                    if f.lower().endswith(supported_extensions):
                        files_to_process.append(os.path.join(root, f))
        elif os.path.isfile(path):
            if path.lower().endswith(supported_extensions):
                files_to_process.append(path)
            else:
                print(f"跳过不支持的文件格式: {path}", file=sys.stderr)
        else:
            print(f"路径不存在: {path}", file=sys.stderr)
            
    if not files_to_process:
        print("未找到需要处理的图片文件。")
        sys.exit(0)
        
    print(f"找到 {len(files_to_process)} 张待处理的图片。")
    
    if args.output:
        os.makedirs(args.output, exist_ok=True)
        
    success_count = 0
    for file_path in files_to_process:
        if process_single_image(cmd_name, file_path, args.output, args.artist, args.copyright):
            success_count += 1
            
    print(f"\n处理完成: 成功 {success_count}/{len(files_to_process)} 张图片。")

if __name__ == "__main__":
    main()
