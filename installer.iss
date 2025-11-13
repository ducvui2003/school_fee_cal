[Setup]
AppName=HanhPhuc
AppVersion=1.0.0
DefaultDirName={autopf}\HanhPhuc
DefaultGroupName=HanhPhuc
OutputDir=output
OutputBaseFilename=HanhPhucInstaller
Compression=lzma
SolidCompression=yes
UninstallDisplayIcon={app}\HanhPhuc.exe

[Files]
Source: "dist\HanhPhuc.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\HanhPhuc"; Filename: "{app}\HanhPhuc.exe"
Name: "{commondesktop}\HanhPhuc"; Filename: "{app}\HanhPhuc.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\HanhPhuc.exe"; Description: "Launch HanhPhuc"; Flags: nowait postinstall skipifsilent