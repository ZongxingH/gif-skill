# 图片生成 GIF Skill

这是一个使用豆包 API 将图片转换为 GIF 动图的 Claude Code Skill。

## 目录

- [功能特点](#功能特点)
- [快速开始](#快速开始)
- [安装](#安装)
- [配置](#配置)
- [使用方法](#使用方法)
- [输出说明](#输出说明)
- [高级配置](#高级配置)
- [常见问题](#常见问题)
- [API 说明](#api-说明)
- [开发说明](#开发说明)

## 功能特点

- ✅ 支持多种图片格式（PNG、JPG、JPEG 等）
- ✅ 自动将图片编码为 Base64 格式
- ✅ 调用豆包 Seedance 1.0 Pro 模型生成视频
- ✅ 自动轮询任务状态直到完成
- ✅ 自动下载生成的视频到本地
- ✅ **使用 ffmpeg 高质量转换视频为 GIF 动图**
- ✅ **两步调色板法优化 GIF 颜色质量**
- ✅ **智能优化 GIF 大小（调整分辨率和帧率）**
- ✅ **自动清理临时视频文件，节省磁盘空间**
- ✅ **输出 GIF 绝对路径，方便后续使用**
- ✅ API 密钥从文件读取，安全便捷

## 快速开始

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install requests

# 安装 ffmpeg（用于视频转 GIF）
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# 从 https://ffmpeg.org/download.html 下载并安装
```

### 2. 配置 API 密钥

创建 `scripts/key` 文件并写入你的豆包 API 密钥：

```bash
# 方式 1: 使用 echo 命令
echo "your_api_key_here" > scripts/key

# 方式 2: 复制示例文件后编辑
cp scripts/key.example scripts/key
# 然后编辑 scripts/key 文件，替换为你的实际 API 密钥
```

**重要提示**：
- 不要将 `scripts/key` 文件提交到 Git 仓库
- 该文件已添加到 `.gitignore`，确保密钥安全

### 3. 运行

```bash
# 使用自定义描述
python3 scripts/image_to_video.py photo.jpg "女孩微笑着看向镜头"

# 使用默认描述
python3 scripts/image_to_video.py photo.jpg
```

### 4. 查看结果

生成的文件保存在以下目录：

**GIF 文件**：`gifs/video_20260128_143025.gif`

**注意**：原视频文件会在 GIF 生成后自动删除，以节省磁盘空间。最终输出会显示 GIF 的绝对路径。

## 安装

### 方式 1: 快速安装（推荐）

运行自动安装脚本：

```bash
./install.sh
```

脚本会自动：
1. 检查 Python 和 pip 是否安装
2. 检查 ffmpeg 是否安装
3. 安装所有 Python 依赖（requests）
4. 询问安装范围（项目级别或个人级别）
5. 复制文件到相应目录

### 方式 2: 手动安装

#### 项目级别安装

将此 skill 安装到当前项目：

```bash
mkdir -p .claude/skills/image-to-video
cp SKILL.md .claude/skills/image-to-video/
cp -r scripts .claude/skills/image-to-video/
mkdir -p .claude/skills/image-to-video/videos
mkdir -p .claude/skills/image-to-video/gifs
```

#### 个人级别安装

将此 skill 安装到所有项目：

```bash
mkdir -p ~/.claude/skills/image-to-video
cp SKILL.md ~/.claude/skills/image-to-video/
cp -r scripts ~/.claude/skills/image-to-video/
mkdir -p ~/.claude/skills/image-to-video/videos
mkdir -p ~/.claude/skills/image-to-video/gifs
```

## 配置

### API 密钥配置

#### 获取 API 密钥

1. 访问豆包 API 平台
2. 注册/登录账号
3. 创建 API Key
4. 确保有 Seedance 模型的访问权限

#### 配置密钥文件

```bash
echo "your_api_key_here" > scripts/key
```

#### 更换 API 密钥

直接编辑 `scripts/key` 文件，替换为新的 API 密钥即可。

### 自定义默认提示词

编辑 `scripts/image_to_video.py` 中的 `default_prompt` 变量（第 314 行）：

```python
prompt = "你的自定义默认提示词"
```

### 自定义 GIF 参数

在 `scripts/image_to_video.py` 中修改 `convert_video_to_gif` 函数的参数（第 89 行）：

```python
# 调整 GIF 参数
gif_path = convert_video_to_gif(
    output_path,
    max_width=320,      # GIF 最大宽度（默认 480 像素）
    fps=8,              # GIF 帧率（默认 10 fps）
    delete_video=True   # 是否删除原视频（默认 True）
)

# 参数说明：
# max_width: GIF 最大宽度，降低可减小文件大小
# fps: GIF 帧率，降低可减小文件大小
# delete_video: 是否在生成 GIF 后删除原视频文件
```

### 保留原视频文件

如果需要保留原视频文件，修改 `delete_video` 参数：

```python
gif_path = convert_video_to_gif(output_path, delete_video=False)
```

### 自定义视频参数

在脚本中可以修改以下参数（第 321 行）：

```python
duration = 5  # 视频时长（秒）
```

在 `create_video_generation_task` 函数中可以修改：

```python
"generate_audio": True,    # 是否生成音频
"ratio": "adaptive",       # 视频比例（"16:9", "9:16", "1:1", "adaptive"）
"watermark": False         # 是否添加水印
```

## 使用方法

### 方式 1: 作为 Claude Code Skill 使用（推荐）

在 Claude Code 中运行：

```bash
/image-to-gif <图片路径> <动画描述>
```

示例：

```bash
# 使用自定义描述
/image-to-gif photo.jpg 女孩微笑着看向镜头，背景虚化

# 使用默认描述
/image-to-gif photo.jpg
```

### 方式 2: 直接运行 Python 脚本

```bash
python3 scripts/image_to_video.py <图片路径> <动画描述>
```

示例：

```bash
# 使用自定义描述
python3 scripts/image_to_video.py photo.jpg "女孩微笑着看向镜头"

# 使用默认描述
python3 scripts/image_to_video.py photo.jpg
```

### 完整运行示例

```bash
$ python3 scripts/image_to_video.py photo.jpg "女孩微笑着看向镜头"

============================================================
图片生成 GIF Skill
============================================================

正在加载 API Key...
✓ API Key 加载成功

动画描述: 女孩微笑着看向镜头

------------------------------------------------------------
步骤 1: 编码图片为 Base64...
图片编码完成

步骤 2: 创建视频生成任务...
正在创建视频生成任务...
任务创建成功，任务 ID: cgt-2025****

步骤 3: 等待视频生成...
开始轮询任务状态（每 5 秒检查一次）...
[1/120] 任务状态: processing
[2/120] 任务状态: processing
...
[15/120] 任务状态: succeeded
视频生成成功！

步骤 4: 下载生成的视频...
正在下载视频到 videos/video_20260128_143025.mp4...
视频下载成功: videos/video_20260128_143025.mp4

步骤 5: 转换视频为 GIF...
正在处理视频: videos/video_20260128_143025.mp4
目标帧率: 10 fps，最大宽度: 480px
正在生成调色板...
正在生成 GIF: gifs/video_20260128_143025.gif
✓ GIF 生成成功: gifs/video_20260128_143025.gif
✓ GIF 大小: 5.77 MB
✓ 已删除原视频文件: videos/video_20260128_143025.mp4

------------------------------------------------------------
✓ 所有步骤完成！
✓ GIF 已保存到: /Users/username/project/gifs/video_20260128_143025.gif
============================================================
```

## 输出说明

### GIF 文件

- **位置**：`gifs/` 目录
- **格式**：GIF
- **命名**：`video_YYYYMMDD_HHMMSS.gif`
- **优化参数**：
  - 最大宽度：480 像素（自动按比例缩放高度）
  - 帧率：10 fps（从原视频抽帧）
  - 使用 ffmpeg 两步调色板法优化颜色
  - 使用 Lanczos 算法保证缩放质量
  - 通常文件大小：2-6 MB
- **输出**：显示 GIF 的绝对路径，方便后续使用

### 视频文件处理

- **临时视频**：下载到 `videos/` 目录
- **自动清理**：GIF 生成成功后自动删除原视频文件
- **优势**：节省磁盘空间，只保留最终的 GIF 文件

## 高级配置

### ffmpeg 转换原理

本 skill 使用 ffmpeg 的两步调色板法生成高质量 GIF：

**步骤 1：生成调色板**
```bash
ffmpeg -i video.mp4 -vf "fps=10,scale=480:-1:flags=lanczos,palettegen" palette.png
```

**步骤 2：使用调色板生成 GIF**
```bash
ffmpeg -i video.mp4 -i palette.png -lavfi "fps=10,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif
```

**优势**：
- 两步法可以生成最优的 256 色调色板
- Lanczos 算法提供最佳的缩放质量
- paletteuse 滤镜优化颜色映射和抖动
- 比直接转换或 Python 库质量更高

### 批量处理

创建批量处理脚本 `batch_process.sh`：

```bash
#!/bin/bash

# 批量处理多张图片
for image in images/*.png; do
    echo "Processing $image..."
    python3 scripts/image_to_video.py "$image" "默认提示词"
done
```

使用方法：

```bash
chmod +x batch_process.sh
./batch_process.sh
```

## 常见问题

### Q: 如何获取豆包 API 密钥？

A:
1. 访问豆包 API 平台
2. 注册/登录账号
3. 创建 API Key
4. 确保有 Seedance 模型的访问权限

### Q: API 密钥存储在哪里？

A: API 密钥存储在 `scripts/key` 文件中，该文件已添加到 `.gitignore`，不会被提交到 Git 仓库。

### Q: 视频生成需要多长时间？

A: 通常需要 1-3 分钟，取决于服务器负载。

### Q: 支持哪些图片格式？

A: 支持常见的图片格式：PNG、JPG、JPEG、GIF、BMP 等。

### Q: GIF 文件太大怎么办？

A: 可以在脚本中调整以下参数来减小 GIF 文件大小：
- `max_width`: 降低最大宽度（默认 480 像素）
- `fps`: 降低帧率（默认 10 fps）

编辑 `scripts/image_to_video.py` 第 89 行的 `convert_video_to_gif` 函数调用。

### Q: 可以保留原视频文件吗？

A: 可以，修改 `scripts/image_to_video.py` 第 89 行：

```python
gif_path = convert_video_to_gif(output_path, delete_video=False)
```

### Q: 为什么使用 ffmpeg 而不是 Python 库？

A: ffmpeg 方案有以下优势：
- 性能更好，转换速度更快
- 内存占用更小，流式处理
- 颜色质量更高（两步调色板法）
- 支持更多优化选项
- 代码更简洁易维护

### Q: 如何检查 ffmpeg 是否安装？

A: 在终端运行：

```bash
ffmpeg -version
```

如果显示版本信息，说明已安装。如果提示命令不存在，请按照快速开始中的说明安装 ffmpeg。

### Q: 生成失败怎么办？

A: 检查：
1. `scripts/key` 文件是否存在且包含有效的 API 密钥
2. 图片文件是否存在
3. 网络连接是否正常
4. API 配额是否充足
5. 是否安装了所有依赖：`pip install requests`
6. 是否安装了 ffmpeg：`ffmpeg -version`

### Q: 如何自定义动画效果？

A: 在命令中提供详细的动画描述参数，例如：

```bash
/image-to-gif photo.jpg 镜头缓缓推进，人物微笑，背景虚化，添加动态光影效果
```

## API 说明

### 创建任务 API

- **URL**: `https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`
- **方法**: POST
- **模型**: doubao-seedance-1-5-pro-251215

**请求参数**：

```json
{
  "model": "doubao-seedance-1-5-pro-251215",
  "content": [
    {
      "type": "text",
      "text": "视频描述提示词"
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "data:image/png;base64,<Base64编码>"
      }
    }
  ],
  "generate_audio": true,
  "ratio": "adaptive",
  "duration": 5,
  "watermark": false
}
```

**响应**：

```json
{
  "id": "cgt-2025****"
}
```

### 查询任务 API

- **URL**: `https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}`
- **方法**: GET

**响应**：

```json
{
  "id": "cgt-2025****",
  "model": "doubao-seedance-1-5-pro-251215",
  "status": "succeeded",
  "content": {
    "video_url": "https://ark-content-generation-cn-beijing.tos-cn-beijing.volces.com/****"
  },
  "usage": {
    "completion_tokens": 246840,
    "total_tokens": 246840
  },
  "created_at": 1765510475,
  "updated_at": 1765510559
}
```

### 任务状态

- `pending`: 等待中
- `processing`/`running`: 处理中
- `succeeded`: 成功
- `failed`: 失败

### 参数说明

- `model`: 使用的模型名称
- `content`: 包含文本提示词和图片的数组
- `generate_audio`: 是否生成音频（true/false）
- `ratio`: 视频比例（"adaptive", "16:9", "9:16", "1:1"）
- `duration`: 视频时长（秒）
- `watermark`: 是否添加水印（true/false）

## 开发说明

### 项目结构

```
gif-skill/
├── SKILL.md              # Claude Skill 配置文件
├── README.md             # 项目说明文档（本文件）
├── install.sh            # 自动安装脚本
├── .gitignore            # Git 忽略文件配置
├── scripts/              # 脚本目录
│   ├── image_to_video.py # 主程序入口
│   ├── utils.py          # 工具函数模块
│   ├── api.py            # API 交互模块
│   ├── converter.py      # 视频转换模块
│   ├── key.example       # API 密钥示例文件
│   └── key               # API 密钥文件（需自行创建）
├── videos/               # 视频输出目录
│   └── .gitkeep          # 保持目录结构
└── gifs/                 # GIF 输出目录
    └── .gitkeep          # 保持目录结构
```

### 模块说明

- **image_to_video.py**: 主程序入口，协调各模块完成图片到 GIF 的转换
- **utils.py**: 工具函数模块，包含图片编码、API 密钥加载等辅助功能
- **api.py**: API 交互模块，处理与豆包 API 的所有交互
- **converter.py**: GIF 转换模块，使用 ffmpeg 处理视频到 GIF 的高质量转换

### 添加新功能

如果需要扩展此 skill，可以：

1. 在 `scripts/` 目录下添加新的 Python 模块
2. 在相应模块中添加功能函数
3. 在 `image_to_video.py` 中导入并使用新功能
4. 更新 `SKILL.md` 中的说明
5. 在 `allowed-tools` 中添加需要的工具权限

**模块化设计**：
- `utils.py`: 添加通用工具函数
- `api.py`: 添加新的 API 交互功能
- `converter.py`: 添加新的转换功能

### 调试

直接运行 Python 脚本进行调试：

```bash
python3 scripts/image_to_video.py photo.jpg "测试描述"
```

### 测试

确保安装了依赖后，使用测试图片进行测试：

```bash
# 准备测试图片和 API 密钥
echo "your_api_key" > scripts/key

# 运行脚本
python3 scripts/image_to_video.py test.jpg "测试视频描述"
```

### 错误处理

脚本包含完善的错误处理机制：
- 图片文件缺失或无效
- API 密钥文件缺失或为空
- API 认证失败
- 网络错误
- 任务失败
- 下载错误
- GIF 转换失败
- 超时（10 分钟后，即 120 次轮询 × 5 秒）

### Claude Skill 配置

`SKILL.md` 文件遵循 Claude Code Skill 规范，包含以下配置：

**Frontmatter 配置**：
- `name`: image-to-video
- `description`: 功能描述
- `disable-model-invocation`: true（需要用户手动触发）
- `user-invocable`: true（用户可调用）
- `argument-hint`: [图片路径] [视频描述]
- `allowed-tools`: Bash(python3 *), Read

## 注意事项

1. 确保图片文件路径正确且文件存在
2. API Key 需要有效的豆包授权
3. 视频生成可能需要一定时间，请耐心等待
4. 默认每 5 秒轮询一次任务状态
5. 最长等待时间为 10 分钟（120 次 × 5 秒）
6. **GIF 转换需要系统安装 ffmpeg**
7. **原视频文件会在 GIF 生成后自动删除**
8. `scripts/key` 文件不会被提交到 Git 仓库
9. 最终输出会显示 GIF 的绝对路径

## 许可证

MIT License

---

**相关文档**：
- [SKILL.md](SKILL.md) - Claude Skill 规范配置
- [scripts/key.example](scripts/key.example) - API 密钥示例文件
