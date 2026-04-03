#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenFina 打包脚本
使用 PyInstaller 将应用打包为独立的可执行文件
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = PROJECT_ROOT / 'build'
DIST_DIR = PROJECT_ROOT / 'dist'
DATA_DIR = PROJECT_ROOT / 'data'
SPEC_NAME = 'OpenFina.spec'


def clean_build():
    """清理之前的构建文件"""
    for target_dir in (BUILD_DIR, DIST_DIR):
        if target_dir.exists():
            print(f"清理 {target_dir.name}/ 目录...")
            shutil.rmtree(target_dir)

    for file_path in PROJECT_ROOT.iterdir():
        if file_path.is_file() and file_path.suffix == '.spec' and file_path.name != SPEC_NAME:
            print(f"删除旧的 spec 文件: {file_path.name}")
            file_path.unlink()


def get_conda_python():
    """获取 Conda Qt 环境的 Python 路径"""
    candidates = []
    user_profile = os.environ.get('USERPROFILE', '')

    if sys.platform == 'win32':
        if user_profile:
            candidates.extend([
                os.path.join(user_profile, '.conda', 'envs', 'Qt', 'python.exe'),
                os.path.join(user_profile, 'anaconda3', 'envs', 'Qt', 'python.exe'),
                os.path.join(user_profile, 'miniconda3', 'envs', 'Qt', 'python.exe'),
            ])
        candidates.extend([
            r'C:\ProgramData\anaconda3\envs\Qt\python.exe',
            r'C:\ProgramData\miniconda3\envs\Qt\python.exe',
        ])

    for python_path in candidates:
        if os.path.exists(python_path):
            return python_path

    return sys.executable


def build():
    """执行打包"""
    print('=' * 60)
    print('OpenFina 打包工具')
    print('=' * 60)

    clean_build()
    DATA_DIR.mkdir(exist_ok=True)

    python_exe = get_conda_python()
    print(f'使用 Python: {python_exe}')

    cmd = [
        python_exe, '-m', 'PyInstaller',
        '--name=OpenFina',
        '--windowed',
        '--onedir',
        '--clean',
        '--noconfirm',
        '--add-data', 'icons;icons',
        '--add-data', 'source/subject.json;source',
        '--hidden-import', 'bcrypt',
        '--hidden-import', 'numpy',
        '--hidden-import', 'pandas',
        '--hidden-import', 'PySide6.QtCore',
        '--hidden-import', 'PySide6.QtGui',
        '--hidden-import', 'PySide6.QtWidgets',
        'app/bootstrap.py',
    ]

    print(f"\n执行命令: {' '.join(cmd)}")
    print('-' * 60)

    result = subprocess.run(cmd, capture_output=False, text=True, cwd=PROJECT_ROOT)

    if result.returncode == 0:
        print('\n' + '=' * 60)
        print('[OK] 打包成功!')
        print('=' * 60)
        print(f"\n输出目录: {DIST_DIR / 'OpenFina'}")
        print('\n使用说明:')
        print('1. 将整个 dist/OpenFina/ 目录复制到目标机器')
        print('2. 运行 OpenFina.exe 即可')
        print('3. 用户数据将自动保存在 data/ 目录中')
        print('\n目录结构:')
        print('  OpenFina/')
        print('  ├── OpenFina.exe     # 主程序')
        print('  ├── _internal/       # 依赖库和打包资源')
        print('  └── data/            # 用户数据（运行时创建）')
    else:
        print('\n' + '=' * 60)
        print('[FAIL] 打包失败!')
        print('=' * 60)
        print(f'返回码: {result.returncode}')
        return 1

    return 0


def build_single_file():
    """打包为单文件模式（可选）"""
    print('=' * 60)
    print('OpenFina 单文件打包工具')
    print('=' * 60)

    clean_build()
    DATA_DIR.mkdir(exist_ok=True)

    python_exe = get_conda_python()
    cmd = [
        python_exe, '-m', 'PyInstaller',
        '--name=OpenFina',
        '--windowed',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--add-data', 'icons;icons',
        '--add-data', 'source/subject.json;source',
        '--hidden-import', 'bcrypt',
        '--hidden-import', 'numpy',
        '--hidden-import', 'pandas',
        'app/bootstrap.py',
    ]

    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False, text=True, cwd=PROJECT_ROOT)

    if result.returncode == 0:
        print('\n[OK] 打包成功! 输出: dist/OpenFina.exe')
    else:
        print('\n[FAIL] 打包失败!')
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
