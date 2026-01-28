"""
视频转换模块
处理视频到 GIF 的转换功能
"""

import os
import subprocess
import shutil
from pathlib import Path


def check_ffmpeg_installed():
    """检查系统是否安装了 ffmpeg

    Returns:
        bool: 是否安装了 ffmpeg
    """
    return shutil.which('ffmpeg') is not None


def convert_video_to_gif(video_path, output_dir='gifs', max_width=480, fps=10, delete_video=False):
    """将视频转换为 GIF（使用 ffmpeg）

    Args:
        video_path: 视频文件路径
        output_dir: GIF 输出目录
        max_width: GIF 最大宽度（像素），用于控制文件大小
        fps: GIF 帧率，降低帧率可以减小文件大小
        delete_video: 是否在生成 GIF 后删除原视频文件

    Returns:
        str: GIF 文件路径，失败返回 None
    """
    # 检查 ffmpeg 是否安装
    if not check_ffmpeg_installed():
        print("错误: 未找到 ffmpeg")
        print("请先安装 ffmpeg:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  Windows: 从 https://ffmpeg.org/download.html 下载")
        return None

    # 创建输出目录
    Path(output_dir).mkdir(exist_ok=True)

    # 生成 GIF 文件名
    video_name = Path(video_path).stem
    gif_path = os.path.join(output_dir, f'{video_name}.gif')

    try:
        print()
        print("步骤 5: 转换视频为 GIF...")
        print(f"正在处理视频: {video_path}")
        print(f"目标帧率: {fps} fps，最大宽度: {max_width}px")

        # 使用 ffmpeg 生成高质量 GIF
        # 两步法：先生成调色板，再使用调色板生成 GIF，可以获得更好的颜色质量
        palette_path = os.path.join(output_dir, 'palette.png')

        # 步骤 1: 生成调色板
        palette_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'fps={fps},scale={max_width}:-1:flags=lanczos,palettegen',
            '-y',  # 覆盖已存在的文件
            palette_path
        ]

        print("正在生成调色板...")
        result = subprocess.run(
            palette_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"错误: 生成调色板失败")
            print(f"错误信息: {result.stderr}")
            return None

        # 步骤 2: 使用调色板生成 GIF
        gif_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', palette_path,
            '-lavfi', f'fps={fps},scale={max_width}:-1:flags=lanczos[x];[x][1:v]paletteuse',
            '-y',  # 覆盖已存在的文件
            gif_path
        ]

        print(f"正在生成 GIF: {gif_path}")
        result = subprocess.run(
            gif_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 清理临时调色板文件
        if os.path.exists(palette_path):
            os.remove(palette_path)

        if result.returncode != 0:
            print(f"错误: 生成 GIF 失败")
            print(f"错误信息: {result.stderr}")
            return None

        # 获取文件大小
        if os.path.exists(gif_path):
            file_size = os.path.getsize(gif_path)
            file_size_mb = file_size / (1024 * 1024)

            print(f"✓ GIF 生成成功: {gif_path}")
            print(f"✓ GIF 大小: {file_size_mb:.2f} MB")

            # 删除原视频文件（如果指定）
            if delete_video and os.path.exists(video_path):
                try:
                    os.remove(video_path)
                    print(f"✓ 已删除原视频文件: {video_path}")
                except Exception as e:
                    print(f"警告: 删除视频文件失败 - {str(e)}")

            return gif_path
        else:
            print("错误: GIF 文件未生成")
            return None

    except Exception as e:
        print(f"错误: 转换 GIF 失败 - {str(e)}")
        return None
