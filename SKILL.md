---
name: image-to-gif
description: 使用豆包 Seedance API 将静态图片转换为动态 GIF。从 scripts/key 文件读取 API 密钥，接收图片路径和动画描述作为参数，自动生成高质量 GIF 动图。使用 ffmpeg 两步调色板法优化颜色质量。
disable-model-invocation: true
user-invocable: true
argument-hint: [图片路径] [动画描述]
allowed-tools: Bash(python3 *), Read
---

# 图片生成 GIF 工具

使用豆包 Seedance 1.0 Pro 模型将静态图片转换为动态 GIF 动图。

## 概述

此 skill 接收一张静态图片和动画描述，生成高质量 GIF 动图。完整的工作流程包括：
1. 从 `scripts/key` 文件读取豆包 API 密钥
2. 将图片编码为 Base64 格式
3. 提交视频生成任务到豆包 API
4. 轮询任务状态直到完成
5. 下载生成的临时视频
6. 使用 ffmpeg 两步调色板法将视频转换为高质量 GIF
7. 自动删除临时视频文件，节省磁盘空间
8. 输出 GIF 的绝对路径

## 使用方法

### 命令格式

```bash
/image-to-gif <图片路径> <动画描述>
```

### 参数说明

1. **图片路径**（必需）：要转换的图片文件路径
2. **动画描述**（可选）：描述动画内容的文本提示词，如果不提供则使用默认提示词

### 使用示例

```bash
# 使用自定义描述
/image-to-gif photo.jpg 女孩微笑着看向镜头，背景虚化

# 使用默认描述
/image-to-gif photo.jpg
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
- `ffmpeg` 命令行工具（用于高质量 GIF 转换）
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt-get install ffmpeg`
  - Windows: 从 https://ffmpeg.org/download.html 下载
- 有效的豆包 API 密钥，需要有 Seedance 模型访问权限
- 支持的图片格式（PNG、JPG、JPEG 等）

**快速安装所有依赖**：
```bash
# Python 依赖
pip install requests

# ffmpeg（根据系统选择）
brew install ffmpeg  # macOS
```

## 脚本位置

主脚本位于 `scripts/image_to_video.py`。

## 输出

生成的 GIF 文件保存在 `gifs` 目录下，文件名格式为：
```
gifs/video_YYYYMMDD_HHMMSS.gif
```

**GIF 优化特性**：
- 使用 ffmpeg 两步调色板法，颜色质量更高
- 最大宽度：480 像素（自动按比例缩放高度）
- 帧率：10 fps（从原视频抽帧）
- 使用 Lanczos 算法保证缩放质量
- 自动优化文件大小（通常 2-6 MB）
- 输出 GIF 的绝对路径，方便后续使用

**临时文件处理**：
- 临时视频文件会在 GIF 生成后自动删除
- 只保留最终的 GIF 文件，节省磁盘空间

## API 详情

- **模型**: doubao-seedance-1-0-pro-250528
- **接口地址**: https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks
- **功能特性**:
  - 自适应宽高比
  - 无水印
  - 固定时长 5 秒
  - 生成临时视频后转换为 GIF

## 工作流程示例

1. 用户调用：`/image-to-gif my_photo.jpg 女孩微笑着看向镜头`
2. 脚本从 `scripts/key` 读取 API 密钥
3. 脚本编码图片并创建任务
4. 脚本每 5 秒轮询一次任务状态
5. 完成后，临时视频下载到 `videos/` 目录
6. 使用 ffmpeg 两步调色板法将视频转换为高质量 GIF
7. GIF 保存到 `gifs/` 目录
8. 自动删除临时视频文件
9. 输出 GIF 的绝对路径

## 默认提示词

如果未提供动画描述参数，将使用默认描述：
> "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头，狐狸友善地抱着，镜头缓缓拉出，女孩的头发被风吹动，可以听到风声"

## 错误处理

脚本包含完善的错误处理机制：
- 图片文件缺失或无效
- API 密钥文件缺失或为空
- API 认证失败
- 网络错误
- 任务失败
- 下载错误
- ffmpeg 未安装或转换失败
- 超时（10 分钟后，即 120 次轮询 × 5 秒）

## 任务

执行图片转 GIF 脚本：

```bash
python3 scripts/image_to_video.py <图片路径> <动画描述>
```

示例：
```bash
python3 scripts/image_to_video.py photo.jpg "女孩微笑着看向镜头"
```
