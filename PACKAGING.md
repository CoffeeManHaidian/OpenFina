# OpenFina 打包指南

## 概述

本文档说明如何将 OpenFina 打包为独立的 Windows 可执行文件（.exe），以便分发给没有 Python 环境的用户使用。

## 目录结构

```
OpenFina/
├── ui/login.py           # 程序入口
├── main.py               # 主窗口
├── models/               # 数据模型
├── utils/                # 工具模块
│   ├── path_helper.py    # 路径处理（新增）
│   └── ...
├── icons/                # 图标资源
├── source/               # 数据文件
│   └── subject.json      # 会计科目
├── data/                 # 用户数据（运行时创建）
│   ├── users.db          # 用户数据库
│   ├── settings.json     # 用户配置
│   └── {公司}_{年份}_vouchers.db  # 凭证数据
├── build_exe.py          # 打包脚本
└── PACKAGING.md          # 本文件
```

## 打包前准备

### 1. 安装 PyInstaller

在 Conda Qt 环境中安装 PyInstaller：

```bash
conda activate Qt
pip install pyinstaller
```

### 2. 安装项目依赖

确保所有依赖已安装：

```bash
pip install PySide6 bcrypt numpy pandas
```

## 打包方法

### 方法1：使用打包脚本（推荐）

```bash
# 激活 Conda 环境
conda activate Qt

# 使用默认单目录模式打包（推荐，启动快）
python build_exe.py

# 或使用单文件模式打包（只有一个exe文件，启动较慢）
python build_exe.py --single
```

### 方法2：手动打包

```bash
# 单目录模式（推荐）
pyinstaller --name=OpenFina \
    --windowed \
    --onedir \
    --clean \
    --noconfirm \
    --add-data "icons;icons" \
    --add-data "source/subject.json;source" \
    --hidden-import bcrypt \
    --hidden-import numpy \
    --hidden-import pandas \
    ui/login.py

# 单文件模式
pyinstaller --name=OpenFina \
    --windowed \
    --onefile \
    --clean \
    --noconfirm \
    --add-data "icons;icons" \
    --add-data "source/subject.json;source" \
    ui/login.py
```

## 打包输出

打包成功后，输出目录结构：

```
dist/OpenFina/
├── OpenFina.exe          # 主程序（约 5-10 MB）
├── _internal/            # Python 运行时和依赖库
│   ├── python3.dll
│   ├── PySide6/
│   ├── numpy/
│   └── ...
├── icons/                # 图标资源
│   ├── close.png
│   ├── user.png
│   └── ...
├── source/               # 数据文件
│   └── subject.json      # 会计科目
└── data/                 # 用户数据（首次运行时创建）
    ├── users.db
    ├── settings.json
    └── ...
```

## 分发方式

### 方式1：复制整个目录（简单）

将整个 `dist/OpenFina/` 目录压缩为 zip，分发给用户。

**优点：**
- 启动速度快
- 用户数据易于备份和迁移
- 文件更新方便

### 方式2：使用安装程序（推荐）

使用 Inno Setup 创建专业的安装程序。

**优点：**
- 专业的外观和用户体验
- 自动创建桌面快捷方式和开始菜单项
- 支持卸载功能
- 可自定义安装路径
- 可添加版本信息和数字签名

## 路径改造说明

为了支持打包后的 exe 环境，对以下文件进行了路径改造：

| 文件 | 修改内容 |
|------|----------|
| `utils/path_helper.py` | 新增：路径处理工具模块 |
| `ui/login.py` | 修改：数据库、配置、图标路径改为动态获取 |
| `models/voucher.py` | 修改：导入 path_helper |
| `ui/certificate.py` | 修改：凭证数据库路径改为动态获取 |
| `utils/subject.py` | 修改：会计科目 JSON 路径改为动态获取 |

### 关键代码

```python
# 判断是否为打包环境
if getattr(sys, 'frozen', False):
    # 打包后的 exe 环境
    app_dir = os.path.dirname(sys.executable)
else:
    # 开发环境
    app_dir = os.path.dirname(os.path.dirname(__file__))
```

## 使用 Inno Setup 创建安装程序

### 1. 安装 Inno Setup

1. 访问官网：https://jrsoftware.org/isinfo.php
2. 下载并安装 Inno Setup 6（或更高版本）
3. 安装时勾选"Add to PATH"选项（方便命令行使用）

### 2. 快速创建安装程序（推荐）

使用集成的完整打包脚本，一键完成所有步骤：

```powershell
# 激活环境并执行完整打包
conda activate Qt
python build_full.py
```

这将自动执行：
1. 清理旧构建文件
2. PyInstaller 打包程序
3. Inno Setup 生成安装程序

### 3. 分步创建安装程序

如果已经用 PyInstaller 打包好了，可以跳过打包步骤：

```powershell
# 只创建安装程序（使用已有的 dist/OpenFina/）
python build_full.py --skip-pyinstaller
```

### 4. 手动编译安装脚本

如果需要自定义安装程序，可以手动编辑和编译：

```powershell
# 编辑安装脚本
notepad installer/OpenFina_setup.iss

# 编译（需要 Inno Setup 在 PATH 中）
iscc installer\OpenFina_setup.iss
```

或在 Windows 资源管理器中：
1. 右键点击 `installer/OpenFina_setup.iss`
2. 选择 **Compile**

### 5. 安装脚本功能说明

`installer/OpenFina_setup.iss` 包含以下功能：

| 功能 | 说明 |
|------|------|
| 现代安装界面 | 使用 WizardStyle=modern 的现代风格 |
| 中文语言支持 | 自动使用简体中文界面 |
| 桌面快捷方式 | 可选创建桌面图标 |
| 开始菜单项 | 自动创建程序组 |
| 卸载功能 | 完整的卸载程序 |
| 数据保护 | 卸载时询问是否保留用户数据 |
| 注册表信息 | 在"程序和功能"中显示 |

### 6. 自定义安装程序

编辑 `installer/OpenFina_setup.iss`，修改以下内容：

```pascal
; 应用信息
#define MyAppName "OpenFina"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "你的公司名"

; 安装程序图标（准备 .ico 文件）
SetupIconFile=..\icons\app.ico

; 输出文件名
OutputBaseFilename=OpenFina_Setup_v1.0.0
```

### 7. 输出文件

打包完成后，在 `dist/` 目录下会生成：

```
dist/
├── OpenFina/                    # PyInstaller 输出（可直接使用）
│   ├── OpenFina.exe
│   └── _internal/
└── OpenFina_Setup_v1.0.0.exe   # Inno Setup 安装程序（约 30-50 MB）
```

### 8. 用户安装流程

用户收到 `OpenFina_Setup_v1.0.0.exe` 后：

1. **双击运行安装程序**
2. **选择安装目录**（默认为 C:\Program Files\OpenFina）
3. **选择组件**
   - 创建桌面快捷方式（默认勾选）
4. **等待安装完成**
5. **选择是否立即运行**

安装完成后：
- 桌面会出现 OpenFina 图标
- 开始菜单中有程序组和卸载选项
- 用户数据保存在安装目录的 `data/` 文件夹中

### 9. 卸载程序

用户可以通过以下方式卸载：
- 开始菜单 → OpenFina → 卸载
- 控制面板 → 程序和功能 → OpenFina → 卸载
- 安装目录下的 `unins000.exe`

卸载时会询问是否删除用户数据，保护用户的重要财务信息。

## 常见问题

### Q1: 打包后运行时提示找不到模块？

**A:** 确保使用了 `--hidden-import` 参数添加所有依赖模块。

### Q2: 打包后图标不显示？

**A:** 检查 `icons/` 目录是否正确包含在打包输出中，路径应为相对路径。

### Q3: 用户数据保存在哪里？

**A:** 在 exe 所在目录的 `data/` 文件夹中。首次运行时会自动创建。

### Q4: 如何更新已分发的程序？

**A:** 
1. 保留用户的 `data/` 目录
2. 替换其他文件
3. 或者重新打包后只分发 exe 文件（单目录模式）

### Q5: 杀毒软件误报？

**A:** 这是 PyInstaller 打包程序的常见问题。可以：
- 将程序添加到杀毒软件白名单
- 使用代码签名证书签名
- 向杀毒软件厂商提交误报

## 技术细节

### 单目录 vs 单文件模式

| 特性 | 单目录（--onedir） | 单文件（--onefile） |
|------|-------------------|-------------------|
| 启动速度 | 快 | 慢（需要解压）|
| 文件大小 | 分散在多个文件 | 单个文件 |
| 更新维护 | 方便（只需替换部分文件） | 需要替换整个 exe |
| 用户体验 | 需要复制整个文件夹 | 只需一个文件 |

**推荐：使用单目录模式**，除非明确要求单文件。

### 数据库初始化

打包后的程序会自动处理数据库初始化：
- `users.db`：首次运行时自动创建用户表
- `{公司}_{年份}_vouchers.db`：首次录入凭证时自动创建凭证表
- `settings.json`：首次保存设置时自动创建

无需手动准备数据库文件。