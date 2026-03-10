; OpenFina 安装脚本 - Inno Setup
; 编译命令: iscc OpenFina_setup.iss

#define MyAppName "OpenFina"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "OpenFina Team"
#define MyAppURL "https://github.com/CoffeeManHaidian/OpenFina"
#define MyAppExeName "OpenFina.exe"

[Setup]
; 应用信息
AppId={{A8B4C2D1-E5F6-4A7B-8C9D-0E1F2A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; 默认安装目录
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes

; 输出设置
OutputDir=..\dist
OutputBaseFilename={#MyAppName}_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; 安装程序图标（可选）
; SetupIconFile=..\icons\user.ico

; 版本信息
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} 财务管理系统安装程序
VersionInfoTextVersion={#MyAppVersion}
VersionInfoCopyright=Copyright (C) 2024 {#MyAppPublisher}

; 权限要求
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; 其他设置
ChangesAssociations=no
DisableStartupPrompt=yes
DisableWelcomePage=no
DisableDirPage=no
DisableReadyPage=no
DisableFinishedPage=no

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; 主程序
Source: "..\dist\OpenFina\OpenFina.exe"; DestDir: "{app}"; Flags: ignoreversion
; 依赖库目录
Source: "..\dist\OpenFina\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
; 图标资源
Source: "..\dist\OpenFina\_internal\icons\*"; DestDir: "{app}\_internal\icons"; Flags: ignoreversion recursesubdirs createallsubdirs
; 数据源文件
Source: "..\dist\OpenFina\_internal\source\subject.json"; DestDir: "{app}\_internal\source"; Flags: ignoreversion

[Dirs]
; 创建数据目录（安装时不复制内容，由程序运行时创建）
Name: "{app}\data"; Permissions: users-modify

[Icons]
; 开始菜单
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
; 桌面快捷方式
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
; 快速启动（仅旧版Windows）
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; 安装完成后询问是否运行
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; 卸载时保留用户数据，只删除程序文件
; 如果要删除数据，取消下面行的注释
; Type: filesandordirs; Name: "{app}\data"

[Registry]
; 写入卸载信息到注册表
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}_is1"; ValueType: string; ValueName: "DisplayName"; ValueData: "{#MyAppName}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}_is1"; ValueType: string; ValueName: "UninstallString"; ValueData: "{uninstallexe}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}_is1"; ValueType: string; ValueName: "DisplayIcon"; ValueData: "{app}\{#MyAppExeName}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}_is1"; ValueType: string; ValueName: "DisplayVersion"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}_is1"; ValueType: string; ValueName: "Publisher"; ValueData: "{#MyAppPublisher}"; Flags: uninsdeletekey

[Code]
// 自定义代码 - 安装前检查
function InitializeSetup(): Boolean;
begin
  // 可以在这里添加版本检查逻辑
  Result := true;
end;

// 卸载前询问是否保留用户数据
function InitializeUninstall(): Boolean;
var
  ResultCode: Integer;
begin
  Result := true;
  
  // 检查是否存在用户数据
  if DirExists(ExpandConstant('{app}\data')) then
  begin
    if MsgBox('检测到用户数据目录。' + #13#10 + 
              '是否要删除用户数据？' + #13#10 + 
              '数据位置: ' + ExpandConstant('{app}\data') + #13#10 + #13#10 +
              '警告：删除后数据无法恢复！', 
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      // 删除数据目录
      DelTree(ExpandConstant('{app}\data'), true, true, true);
    end;
  end;
end;

// 安装完成后显示信息
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // 安装完成后的自定义操作
  end;
end;