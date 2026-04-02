# OpenFina
An open financial system

## 打包

### 绿色版

在项目根目录执行：

```powershell
python build_exe.py
```

如果需要单文件版本：

```powershell
python build_exe.py --single
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

在项目根目录执行：

```powershell
python build_full.py
```

如果只想先生成 PyInstaller 包，不生成安装程序：

```powershell
python build_full.py --skip-inno
```

安装版输出目录：

```text
dist/
```

说明：
- `build_exe.py` 会优先查找本机 Conda 的 `Qt` 环境来执行 PyInstaller。
- 绿色版需要整体复制 `dist/OpenFina/` 目录，不能只复制 `OpenFina.exe`。
- 运行后的用户数据和日志会写入 `dist/OpenFina/data/`。
