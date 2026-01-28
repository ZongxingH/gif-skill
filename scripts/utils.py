"""
工具函数模块
包含图片编码、API 密钥加载等辅助功能
"""

import os
import sys
import base64
from pathlib import Path


def encode_image_to_base64(image_path):
    """将图片编码为 base64 格式

    Args:
        image_path: 图片文件路径

    Returns:
        str: Base64 编码的图片数据 URL
    """
    try:
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # 获取图片格式
        image_format = Path(image_path).suffix.lower().replace('.', '')
        if image_format == 'jpg':
            image_format = 'jpeg'

        return f"data:image/{image_format};base64,{encoded_string}"
    except FileNotFoundError:
        print(f"错误: 找不到图片文件 {image_path}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 编码图片时出错 - {str(e)}")
        sys.exit(1)


def load_api_key():
    """从 scripts/key 文件加载 API Key

    Returns:
        str: API 密钥
    """
    script_dir = Path(__file__).parent
    key_file = script_dir / 'key'

    try:
        with open(key_file, 'r') as f:
            api_key = f.read().strip()

        if not api_key:
            print(f"错误: {key_file} 文件为空")
            sys.exit(1)

        return api_key
    except FileNotFoundError:
        print(f"错误: 找不到 API Key 文件 {key_file}")
        print("请创建 scripts/key 文件并将豆包 API Key 写入其中")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取 API Key 文件失败 - {str(e)}")
        sys.exit(1)


def validate_image_path(image_path):
    """验证图片文件是否存在

    Args:
        image_path: 图片文件路径

    Returns:
        bool: 文件是否存在
    """
    if not os.path.exists(image_path):
        print(f"错误: 图片文件不存在 - {image_path}")
        return False
    return True
