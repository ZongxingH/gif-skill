"""
API 交互模块
处理与豆包 API 的所有交互，包括创建任务、查询状态、下载视频
"""

import sys
import time
import os
import requests
from pathlib import Path
from datetime import datetime


def create_video_generation_task(api_key, image_base64, prompt, duration=5):
    """创建视频生成任务

    Args:
        api_key: 豆包 API 密钥
        image_base64: Base64 编码的图片
        prompt: 视频描述提示词
        duration: 视频时长（秒）

    Returns:
        str: 任务 ID
    """
    url = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "doubao-seedance-1-0-pro-250528",
        "content": [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_base64
                }
            }
        ],
        "ratio": "adaptive",
        "duration": duration,
        "watermark": False
    }

    try:
        print("正在创建视频生成任务...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        task_id = result.get('id')

        if not task_id:
            print(f"错误: 无法获取任务 ID - {result}")
            sys.exit(1)

        print(f"任务创建成功，任务 ID: {task_id}")
        return task_id

    except requests.exceptions.RequestException as e:
        print(f"错误: 创建任务失败 - {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应内容: {e.response.text}")
        sys.exit(1)


def check_task_status(api_key, task_id):
    """查询任务状态

    Args:
        api_key: 豆包 API 密钥
        task_id: 任务 ID

    Returns:
        dict: 任务状态信息
    """
    url = f"https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"错误: 查询任务状态失败 - {str(e)}")
        return None


def poll_task_until_complete(api_key, task_id, poll_interval=5, max_attempts=120):
    """轮询任务直到完成

    Args:
        api_key: 豆包 API 密钥
        task_id: 任务 ID
        poll_interval: 轮询间隔（秒）
        max_attempts: 最大轮询次数

    Returns:
        dict: 完成的任务信息
    """
    print(f"开始轮询任务状态（每 {poll_interval} 秒检查一次）...")

    for attempt in range(max_attempts):
        result = check_task_status(api_key, task_id)

        if not result:
            print("无法获取任务状态，继续等待...")
            time.sleep(poll_interval)
            continue

        status = result.get('status')
        print(f"[{attempt + 1}/{max_attempts}] 任务状态: {status}")

        if status == 'succeeded':
            print("视频生成成功！")
            return result
        elif status == 'failed':
            print(f"任务失败: {result}")
            sys.exit(1)
        elif status in ['pending', 'processing', 'running']:
            time.sleep(poll_interval)
        else:
            print(f"未知状态: {status}")
            time.sleep(poll_interval)

    print(f"错误: 任务超时（已等待 {max_attempts * poll_interval} 秒）")
    sys.exit(1)


def download_video(video_url, output_dir='videos'):
    """下载视频到指定目录

    Args:
        video_url: 视频下载 URL
        output_dir: 输出目录

    Returns:
        str: 下载的视频文件路径
    """
    # 创建输出目录
    Path(output_dir).mkdir(exist_ok=True)

    # 生成文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(output_dir, f'video_{timestamp}.mp4')

    try:
        print(f"正在下载视频到 {output_path}...")
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"视频下载成功: {output_path}")
        return output_path

    except requests.exceptions.RequestException as e:
        print(f"错误: 下载视频失败 - {str(e)}")
        sys.exit(1)
