#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenFina 打包脚本
使用 PyInstaller 将应用打包为独立的可执行文件
"""

import os
import sys
import shutil
import subprocess


def clean_build():
    """清理之前的构建文件"""
    dirs_to_remove = ['build', 'dist']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"清理 {dir_name}/ 目录...")
            shutil.rmtree(dir_name)
    
    # 删除之前的 spec 文件
    for file in os.listdir('.'):
        if file.endswith('.spec') and file != 'OpenFina.spec':
            print(f"删除旧的 spec 文件: {file}")
            os.remove(file)


def get_conda_python():
    """获取 Conda Qt 环境的 Python 路径"""
    # 尝试找到 Conda Qt 环境的 Python
    conda_base = os.path.expanduser("~/anaconda3")  # 或 miniconda3
    if not os.path.exists(conda_base):
        conda_base = os.path.expanduser("~/miniconda3")
    
    # Windows 上的路径
    if sys.platform == 'win32':
        python_path = os.path.join(conda_base, "envs", "Qt", "python.exe")
        if os.path.exists(python_path):
            return python_path
    
    # 如果找不到，尝试使用当前 Python
    return sys.executable


def build():
    """执行打包"""
    print("=" * 60)
    print("OpenFina 打包工具")
    print("=" * 60)
    
    # 清理旧构建
    clean_build()
    
    # 确保 data 目录存在（但保持为空，由程序运行时创建）
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # 获取 Python 解释器路径
    python_exe = get_conda_python()
    print(f"使用 Python: {python_exe}")
    
    # PyInstaller 命令
    cmd = [
        python_exe, '-m', 'PyInstaller',
        '--name=OpenFina',
        '--windowed',           # 无控制台窗口
        '--onedir',             # 单目录模式（推荐，启动快）
        # '--onefile',          # 单文件模式（如需使用，取消注释并注释掉 --onedir）
        '--clean',              # 清理临时文件
        '--noconfirm',          # 不确认覆盖
        # 添加数据文件
        '--add-data', 'icons;icons',           # 图标目录
        '--add-data', 'source/subject.json;source',  # 会计科目数据
        # 添加隐藏导入
        '--hidden-import', 'bcrypt',
        '--hidden-import', 'numpy',
        '--hidden-import', 'pandas',
        '--hidden-import', 'PySide6.QtCore',
        '--hidden-import', 'PySide6.QtGui',
        '--hidden-import', 'PySide6.QtWidgets',
        # 入口文件
        'ui/login.py'
    ]
    
    print(f"\n执行命令: {' '.join(cmd)}")
    print("-" * 60)
    
    # 执行打包
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✓ 打包成功!")
        print("=" * 60)
        print(f"\n输出目录: dist/OpenFina/")
        print("\n使用说明:")
        print("1. 将整个 dist/OpenFina/ 目录复制到目标机器")
        print("2. 运行 OpenFina.exe 即可")
        print("3. 用户数据将自动保存在 data/ 目录中")
        print("\n目录结构:")
        print("  OpenFina/")
        print("  ├── OpenFina.exe     # 主程序")
        print("  ├── _internal/       # 依赖库")
        print("  ├── icons/           # 图标资源")
        print("  ├── source/          # 数据文件")
        print("  └── data/            # 用户数据（运行时创建）")
    else:
        print("\n" + "=" * 60)
        print("✗ 打包失败!")
        print("=" * 60)
        print(f"返回码: {result.returncode}")
        return 1
    
    return 0


def build_single_file():
    """打包为单文件模式（可选）"""
    print("=" * 60)
    print("OpenFina 单文件打包工具")
    print("=" * 60)
    
    clean_build()
    
    python_exe = get_conda_python()
    
    cmd = [
        python_exe, '-m', 'PyInstaller',
        '--name=OpenFina',
        '--windowed',
        '--onefile',            # 单文件模式
        '--clean',
        '--noconfirm',
        '--add-data', 'icons;icons',
        '--add-data', 'source/subject.json;source',
        '--hidden-import', 'bcrypt',
        '--hidden-import', 'numpy',
        '--hidden-import', 'pandas',
        'ui/login.py'
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode == 0:
        print("\n✓ 打包成功! 输出: dist/OpenFina.exe")
    else:
        print("\n✗ 打包失败!")
        return 1
    
    return 0


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenFina 打包工具')
    parser.add_argument(
        '--single', 
        action='store_true',
        help='打包为单文件模式（默认是单目录模式）'
    )
    
    args = parser.parse_args()
    
    if args.single:
        sys.exit(build_single_file())
    else:
        sys.exit(build())