#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenFina 完整打包脚本
一键完成：PyInstaller 打包 + Inno Setup 安装程序生成
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = PROJECT_ROOT / 'build'
DIST_DIR = PROJECT_ROOT / 'dist'
APP_DIST_DIR = DIST_DIR / 'OpenFina'
DATA_DIR = PROJECT_ROOT / 'data'
INSTALLER_DIR = PROJECT_ROOT / 'installer'
SPEC_NAME = 'OpenFina.spec'


def get_conda_python():
    """优先获取 Conda Qt 环境中的 Python。"""
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


def clean_build():
    """清理之前的构建文件"""
    print('=' * 60)
    print('步骤 1: 清理旧构建文件')
    print('=' * 60)

    if BUILD_DIR.exists():
        print('  清理 build/ 目录...')
        shutil.rmtree(BUILD_DIR)

    if APP_DIST_DIR.exists():
        print('  清理旧的程序文件...')
        shutil.rmtree(APP_DIST_DIR)

    for file_path in PROJECT_ROOT.iterdir():
        if file_path.is_file() and file_path.suffix == '.spec' and file_path.name != SPEC_NAME:
            print(f'  删除旧的 spec 文件: {file_path.name}')
            file_path.unlink()

    print('  [OK] 清理完成\n')


def pyinstaller_build():
    """执行 PyInstaller 打包"""
    print('=' * 60)
    print('步骤 2: PyInstaller 打包')
    print('=' * 60)

    DATA_DIR.mkdir(exist_ok=True)

    python_exe = get_conda_python()
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
        'ui/login.py',
    ]

    print(f'  使用 Python: {python_exe}')
    print(f"  执行: {' '.join(cmd[:5])}...")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)

    if result.returncode != 0:
        print('  [FAIL] PyInstaller 打包失败!')
        print(f"  错误: {result.stderr[-500:] if len(result.stderr) > 500 else result.stderr}")
        return False

    print('  [OK] PyInstaller 打包成功\n')
    return True


def find_inno_setup():
    """查找 Inno Setup 安装路径"""
    possible_paths = [
        r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
        r'C:\Program Files\Inno Setup 6\ISCC.exe',
        r'C:\Program Files (x86)\Inno Setup 5\ISCC.exe',
        r'C:\Program Files\Inno Setup 5\ISCC.exe',
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    iscc = shutil.which('iscc')
    if iscc:
        return iscc

    return None


def inno_setup_build():
    """执行 Inno Setup 打包"""
    print('=' * 60)
    print('步骤 3: 创建安装程序 (Inno Setup)')
    print('=' * 60)

    iscc_path = find_inno_setup()

    if not iscc_path:
        print('  [FAIL] 未找到 Inno Setup!')
        print('  请从以下地址下载安装：')
        print('  https://jrsoftware.org/isinfo.php')
        print('\n  安装完成后，将 ISCC.exe 所在目录添加到系统 PATH，')
        print('  或修改本脚本中的 iscc_path 变量。\n')
        return False

    print(f'  找到 Inno Setup: {iscc_path}')

    iss_script = INSTALLER_DIR / 'OpenFina_setup.iss'
    if not iss_script.exists():
        print(f'  [FAIL] 未找到安装脚本: {iss_script}')
        return False

    cmd = [iscc_path, str(iss_script)]
    print(f"  执行: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)

    if result.returncode != 0:
        print('  [FAIL] Inno Setup 编译失败!')
        print(f'  错误: {result.stderr}')
        return False

    print('  [OK] 安装程序创建成功\n')
    return True


def show_result():
    """显示打包结果"""
    print('=' * 60)
    print('打包完成!')
    print('=' * 60)

    setup_file = None
    if DIST_DIR.exists():
        for file_name in os.listdir(DIST_DIR):
            if file_name.startswith('OpenFina_Setup') and file_name.endswith('.exe'):
                setup_file = file_name
                break

    if setup_file:
        setup_path = DIST_DIR / setup_file
        size_mb = os.path.getsize(setup_path) / (1024 * 1024)

        print('\n[OK] 安装程序已生成:')
        print(f'  文件: {setup_path}')
        print(f'  大小: {size_mb:.2f} MB')
        print('\n使用说明:')
        print(f'  1. 将 {setup_file} 分发给用户')
        print('  2. 用户双击运行即可安装')
        print('  3. 安装后会在开始菜单和桌面创建快捷方式')
        print('\n分发方式:')
        print(f'  - 直接发送 {setup_file}')
        print('  - 上传到网盘或网站供下载')
        print('  - 制作成压缩包发送')
    else:
        print('\n[FAIL] 未找到生成的安装程序')
        print('  请检查 dist/ 目录')


def main():
    parser = argparse.ArgumentParser(description='OpenFina 完整打包工具')
    parser.add_argument(
        '--skip-pyinstaller',
        action='store_true',
        help='跳过 PyInstaller 打包（如果已经打包过）'
    )
    parser.add_argument(
        '--skip-inno',
        action='store_true',
        help='跳过 Inno Setup（只执行 PyInstaller 打包）'
    )

    args = parser.parse_args()

    print('\n' + '=' * 60)
    print('OpenFina 完整打包工具')
    print('=' * 60 + '\n')

    clean_build()

    if not args.skip_pyinstaller:
        if not pyinstaller_build():
            print('\n打包失败！')
            return 1
    else:
        print('=' * 60)
        print('步骤 2: 跳过 PyInstaller 打包')
        print('=' * 60)
        print('  （使用现有的 dist/OpenFina/ 目录）\n')

    if not args.skip_inno:
        if not inno_setup_build():
            print('\n安装程序创建失败，但程序文件已准备好。')
            print('你可以手动使用 Inno Setup 编译 installer/OpenFina_setup.iss')
            return 1
    else:
        print('=' * 60)
        print('步骤 3: 跳过 Inno Setup')
        print('=' * 60)

    show_result()
    return 0


if __name__ == '__main__':
    sys.exit(main())
