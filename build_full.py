#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenFina 完整打包脚本
一键完成：PyInstaller 打包 + Inno Setup 安装程序生成
"""

import os
import sys
import shutil
import subprocess
import argparse


def clean_build():
    """清理之前的构建文件"""
    print("=" * 60)
    print("步骤 1: 清理旧构建文件")
    print("=" * 60)
    
    dirs_to_remove = ['build']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"  清理 {dir_name}/ 目录...")
            shutil.rmtree(dir_name)
    
    # 保留 dist 目录，因为安装脚本输出在那里
    # 但清理旧的 PyInstaller 输出
    if os.path.exists('dist/OpenFina'):
        print("  清理旧的程序文件...")
        shutil.rmtree('dist/OpenFina')
    
    # 删除旧的 spec 文件
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            print(f"  删除旧的 spec 文件: {file}")
            os.remove(file)
    
    print("  ✓ 清理完成\n")


def pyinstaller_build():
    """执行 PyInstaller 打包"""
    print("=" * 60)
    print("步骤 2: PyInstaller 打包")
    print("=" * 60)
    
    # 确保 data 目录存在
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # PyInstaller 命令
    cmd = [
        sys.executable, '-m', 'PyInstaller',
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
        'ui/login.py'
    ]
    
    print(f"  执行: {' '.join(cmd[:5])}...")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("  ✗ PyInstaller 打包失败!")
        print(f"  错误: {result.stderr[-500:] if len(result.stderr) > 500 else result.stderr}")
        return False
    
    print("  ✓ PyInstaller 打包成功\n")
    return True


def find_inno_setup():
    """查找 Inno Setup 安装路径"""
    possible_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # 尝试从环境变量查找
    iscc = shutil.which('iscc')
    if iscc:
        return iscc
    
    return None


def inno_setup_build():
    """执行 Inno Setup 打包"""
    print("=" * 60)
    print("步骤 3: 创建安装程序 (Inno Setup)")
    print("=" * 60)
    
    iscc_path = find_inno_setup()
    
    if not iscc_path:
        print("  ✗ 未找到 Inno Setup!")
        print("  请从以下地址下载安装：")
        print("  https://jrsoftware.org/isinfo.php")
        print("\n  安装完成后，将 ISCC.exe 所在目录添加到系统 PATH，")
        print("  或修改本脚本中的 iscc_path 变量。\n")
        return False
    
    print(f"  找到 Inno Setup: {iscc_path}")
    
    # 检查安装脚本是否存在
    iss_script = os.path.join('installer', 'OpenFina_setup.iss')
    if not os.path.exists(iss_script):
        print(f"  ✗ 未找到安装脚本: {iss_script}")
        return False
    
    # 执行编译
    cmd = [iscc_path, iss_script]
    print(f"  执行: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("  ✗ Inno Setup 编译失败!")
        print(f"  错误: {result.stderr}")
        return False
    
    print("  ✓ 安装程序创建成功\n")
    return True


def show_result():
    """显示打包结果"""
    print("=" * 60)
    print("打包完成!")
    print("=" * 60)
    
    # 检查输出文件
    setup_file = None
    if os.path.exists('dist'):
        for f in os.listdir('dist'):
            if f.startswith('OpenFina_Setup') and f.endswith('.exe'):
                setup_file = f
                break
    
    if setup_file:
        setup_path = os.path.join('dist', setup_file)
        size_mb = os.path.getsize(setup_path) / (1024 * 1024)
        
        print(f"\n✓ 安装程序已生成:")
        print(f"  文件: {setup_path}")
        print(f"  大小: {size_mb:.2f} MB")
        print(f"\n使用说明:")
        print(f"  1. 将 {setup_file} 分发给用户")
        print(f"  2. 用户双击运行即可安装")
        print(f"  3. 安装后会在开始菜单和桌面创建快捷方式")
        print(f"\n分发方式:")
        print(f"  - 直接发送 {setup_file}")
        print(f"  - 上传到网盘或网站供下载")
        print(f"  - 制作成压缩包发送")
    else:
        print("\n✗ 未找到生成的安装程序")
        print("  请检查 dist/ 目录")


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
    
    print("\n" + "=" * 60)
    print("OpenFina 完整打包工具")
    print("=" * 60 + "\n")
    
    # 步骤 1: 清理
    clean_build()
    
    # 步骤 2: PyInstaller 打包
    if not args.skip_pyinstaller:
        if not pyinstaller_build():
            print("\n打包失败！")
            return 1
    else:
        print("=" * 60)
        print("步骤 2: 跳过 PyInstaller 打包")
        print("=" * 60)
        print("  （使用现有的 dist/OpenFina/ 目录）\n")
    
    # 步骤 3: Inno Setup 打包
    if not args.skip_inno:
        if not inno_setup_build():
            print("\n安装程序创建失败，但程序文件已准备好。")
            print("你可以手动使用 Inno Setup 编译 installer/OpenFina_setup.iss")
            return 1
    else:
        print("=" * 60)
        print("步骤 3: 跳过 Inno Setup")
        print("=" * 60)
    
    # 显示结果
    show_result()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())