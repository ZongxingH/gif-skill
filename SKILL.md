---
name: image-to-video
description: 使用豆包 Seedance API 将静态图片转换为动态视频和 GIF。从 scripts/key 文件读取 API 密钥，接收图片路径和视频描述作为参数，自动生成视频和 GIF 动图。
disable-model-invocation: true
user-invocable: true
argument-hint: [图片路径] [视频描述]
allowed-tools: Bash(python3 *), Read
---

# 图片生成视频和 GIF 工具

使用豆包 Seedance 1.5 Pro 模型将静态图片转换为动态视频，并自动生成 GIF 动图。

## 概述

此 skill 接收一张静态图片和视频描述，生成动态视频和 GIF。完整的工作流程包括：
1. 从 `scripts/key` 文件读取豆包 API 密钥
2. 将图片编码为 Base64 格式
3. 提交视频生成任务到豆包 API
4. 轮询任务状态直到完成
5. 下载生成的视频到 `videos` 目录
6. 自动将视频转换为 GIF 并保存到 `gifs` 目录

## 使用方法

### 命令格式

```bash
/image-to-video <图片路径> <视频描述>
```

### 参数说明

1. **图片路径**（必需）：要转换的图片文件路径
2. **视频描述**（可选）：描述视频内容的文本提示词，如果不提供则使用默认提示词

### 使用示例

```bash
# 使用自定义描述
/image-to-video photo.jpg 女孩微笑着看向镜头，背景虚化

# 使用默认描述
/image-to-video photo.jpg
```

## 配置要求

### API 密钥配置

在使用前，需要创建 `scripts/key` 文件并写入豆包 API 密钥：

```bash
echo "your_api_key_here" > scripts/key
```

### 其他依赖

- Python 3.6 或更高版本
- `requests` 库（安装命令：`pip install requests`）
- `imageio` 库（安装命令：`pip install imageio imageio-ffmpeg`）
- `Pillow` 库（安装命令：`pip install pillow`）
- 有效的豆包 API 密钥，需要有 Seedance 模型访问权限
- 支持的图片格式（PNG、JPG、JPEG 等）

**快速安装所有依赖**：
```bash
pip install requests imageio imageio-ffmpeg pillow
```

## 脚本位置

主脚本位于 `scripts/image_to_video.py`。

## 输出

生成的文件保存在以下目录：

### 视频文件
保存在 `videos` 目录下，文件名格式为：
```
videos/video_YYYYMMDD_HHMMSS.mp4
```

### GIF 文件
保存在 `gifs` 目录下，文件名格式为：
```
gifs/video_YYYYMMDD_HHMMSS.gif
```

**GIF 优化参数**：
- 最大宽度：480 像素（自动按比例缩放高度）
- 帧率：10 fps（从原视频抽帧）
- 自动优化文件大小

## API 详情

- **模型**: doubao-seedance-1-5-pro-251215
- **接口地址**: https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks
- **功能特性**:
  - 启用音频生成
  - 自适应宽高比
  - 无水印
  - 固定时长 5 秒

## 工作流程示例

1. 用户调用：`/image-to-video my_photo.jpg 女孩微笑着看向镜头`
2. 脚本从 `scripts/key` 读取 API 密钥
3. 脚本编码图片并创建任务
4. 脚本每 5 秒轮询一次任务状态
5. 完成后，视频下载到 `videos/` 目录
6. 自动将视频转换为 GIF 并保存到 `gifs/` 目录
7. 用户收到包含视频和 GIF 文件路径的确认信息

## 默认提示词

如果未提供视频描述参数，将使用默认描述：
> "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头，狐狸友善地抱着，镜头缓缓拉出，女孩的头发被风吹动，可以听到风声"

## 错误处理

脚本包含完善的错误处理机制：
- 图片文件缺失或无效
- API 密钥文件缺失或为空
- API 认证失败
- 网络错误
- 任务失败
- 下载错误
- 超时（10 分钟后，即 120 次轮询 × 5 秒）

## 任务

执行图片转视频脚本：

```bash
python3 scripts/image_to_video.py <图片路径> <视频描述>
```

示例：
```bash
python3 scripts/image_to_video.py photo.jpg "女孩微笑着看向镜头"
```
