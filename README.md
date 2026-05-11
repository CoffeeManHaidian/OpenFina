# OpenFina
An open financial system

## 环境要求

- Python `3.10` 到 `3.12`
- Windows 10/11

## 安装依赖

在项目根目录执行：

```powershell
python -m pip install -U pip
python -m pip install .
```

如果需要打包依赖，一并安装：

```powershell
python -m pip install .[packaging]
```

如果你使用 Conda，建议在 `Qt` 环境中执行以上命令。

## 启动程序

开发环境下直接运行：

```powershell
python app/bootstrap.py
```

`app/bootstrap.py` 是正式启动入口，负责应用初始化、自动登录恢复和登录页/主界面切换。

## 当前版本

当前发布版本：`v2.1.1`

Release 说明见 [docs/RELEASE_v2.1.1.md](docs/RELEASE_v2.1.1.md)。

## 项目目录

```text
app/        主应用入口
ui/         界面代码、.ui、资源文件
models/     数据模型
utils/      工具函数
source/     静态业务数据
scripts/    打包和辅助脚本
docs/       项目文档
```

主目录保留 `README.md`、`pyproject.toml`、`OpenFina.spec` 等项目说明文件。

## 打包

### 绿色版

先确保已经安装打包依赖：

```powershell
python -m pip install .[packaging]
```

在项目根目录执行：

```powershell
python scripts/build_exe.py
```

如果需要单文件版本：

```powershell
python scripts/build_exe.py --single
```

绿色版输出目录：

```text
dist/OpenFina/
```

主程序：

```text
dist/OpenFina/OpenFina.exe
```

### 安装版

先确保已经安装打包依赖，并且本机已安装 Inno Setup：

```powershell
python -m pip install .[packaging]
```

在项目根目录执行：

```powershell
python scripts/build_full.py
```

如果只想先生成 PyInstaller 包，不生成安装程序：

```powershell
python scripts/build_full.py --skip-inno
```

安装版输出目录：

```text
dist/
```

说明：
- 项目依赖由 [pyproject.toml](D:/QtProcess/OpenFina/pyproject.toml) 管理。
- [scripts/build_exe.py](D:/QtProcess/OpenFina/scripts/build_exe.py) 会优先查找本机 Conda 的 `Qt` 环境来执行 PyInstaller。
- 绿色版需要整体复制 `dist/OpenFina/` 目录，不能只复制 `OpenFina.exe`。
- 运行后的用户数据和日志会写入 `dist/OpenFina/data/`。
