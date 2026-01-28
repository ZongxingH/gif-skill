#!/bin/bash

# Image to Video Skill 安装脚本

set -e

echo "============================================================"
echo "Image to Video Skill 安装程序"
echo "============================================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python 3，请先安装 Python 3.6 或更高版本"
    exit 1
fi

echo "✓ 检测到 Python 3"
python3 --version
echo ""

# 检查 pip 是否安装
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "错误: 未找到 pip，请先安装 pip"
    exit 1
fi

echo "✓ 检测到 pip"
echo ""

# 安装依赖
echo "正在安装 Python 依赖..."
pip3 install requests imageio imageio-ffmpeg pillow 2>/dev/null || pip install requests imageio imageio-ffmpeg pillow
echo "✓ 依赖安装完成"
echo ""

# 询问安装范围
echo "请选择安装范围："
echo "1) 项目级别（仅当前项目可用）"
echo "2) 个人级别（所有项目可用）"
read -p "请输入选项 [1/2]: " choice

case $choice in
    1)
        INSTALL_DIR=".claude/skills/image-to-video"
        echo ""
        echo "将安装到项目目录: $INSTALL_DIR"
        ;;
    2)
        INSTALL_DIR="$HOME/.claude/skills/image-to-video"
        echo ""
        echo "将安装到个人目录: $INSTALL_DIR"
        ;;
    *)
        echo "无效的选项，退出安装"
        exit 1
        ;;
esac

# 创建目标目录
mkdir -p "$INSTALL_DIR"

# 复制文件
echo ""
echo "正在复制文件..."
cp SKILL.md "$INSTALL_DIR/"
cp -r scripts "$INSTALL_DIR/"
mkdir -p "$INSTALL_DIR/videos"
mkdir -p "$INSTALL_DIR/gifs"

echo "✓ 文件复制完成"
echo ""

# 设置执行权限
chmod +x "$INSTALL_DIR/scripts/image_to_video.py"

echo "============================================================"
echo "✓ 安装完成！"
echo "============================================================"
echo ""
echo "使用方法："
echo "  在 Claude Code 中运行: /image-to-video"
echo "  或带参数运行: /image-to-video path/to/image.png"
echo ""
echo "直接运行脚本："
echo "  python3 $INSTALL_DIR/scripts/image_to_video.py"
echo ""
echo "============================================================"
