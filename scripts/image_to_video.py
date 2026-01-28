#!/usr/bin/env python3
"""
图片生成视频 Skill
使用豆包 API 将图片转换为视频，并自动生成 GIF
"""

import sys
import os
from utils import encode_image_to_base64, load_api_key, validate_image_path
from api import create_video_generation_task, poll_task_until_complete, download_video
from converter import convert_video_to_gif


def main():
    """主函数"""
    # 解析命令行参数
    if len(sys.argv) < 2:
        print("=" * 60)
        print("图片生成视频 Skill")
        print("=" * 60)
        print()
        print("使用方法:")
        print("  python3 scripts/image_to_video.py <图片路径> <视频描述>")
        print()
        print("示例:")
        print("  python3 scripts/image_to_video.py photo.jpg '女孩微笑着看向镜头'")
        print()
        sys.exit(1)

    image_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else None

    print("=" * 60)
    print("图片生成视频 Skill")
    print("=" * 60)
    print()

    # 检查图片文件是否存在
    if not validate_image_path(image_path):
        sys.exit(1)

    # 从文件加载 API Key
    print("正在加载 API Key...")
    api_key = load_api_key()
    print("✓ API Key 加载成功")
    print()

    # 如果没有提供提示词，使用默认值
    if not prompt:
        prompt = "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头，狐狸友善地抱着，镜头缓缓拉出，女孩的头发被风吹动，可以听到风声"
        print(f"使用默认提示词: {prompt}")
    else:
        print(f"视频描述: {prompt}")
    print()

    # 固定视频时长为 5 秒
    duration = 5

    print()
    print("-" * 60)

    # 步骤 1: 编码图片
    print("步骤 1: 编码图片为 Base64...")
    image_base64 = encode_image_to_base64(image_path)
    print("图片编码完成")
    print()

    # 步骤 2: 创建视频生成任务
    print("步骤 2: 创建视频生成任务...")
    task_id = create_video_generation_task(api_key, image_base64, prompt, duration)
    print()

    # 步骤 3: 轮询任务状态
    print("步骤 3: 等待视频生成...")
    result = poll_task_until_complete(api_key, task_id)
    print()

    # 步骤 4: 下载视频
    print("步骤 4: 下载生成的视频...")
    video_url = result.get('content', {}).get('video_url')

    if not video_url:
        print(f"错误: 无法获取视频 URL - {result}")
        sys.exit(1)

    output_path = download_video(video_url)
    print()

    # 步骤 5: 转换为 GIF
    gif_path = convert_video_to_gif(output_path, delete_video=True)
    print()

    print("-" * 60)
    print("✓ 所有步骤完成！")
    if gif_path:
        # 输出 GIF 的绝对路径
        abs_gif_path = os.path.abspath(gif_path)
        print(f"✓ GIF 已保存到: {abs_gif_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
