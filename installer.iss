; ==============================================
; Inno Setup script for your Tkinter App
; ==============================================

[Setup]
AppName=Tính tiền học Hạnh Phúc
AppVersion=1.0.0
DefaultDirName={autopf}\HanhPhuc
DefaultGroupName=Hanh Phuc
OutputDir=installer
OutputBaseFilename=HanhPhucSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
; Include your packaged app folder
Source: "build\HanhPhuc\*"; DestDir: "{app}"; Flags: recursesubdirs

[Run]
Filename: "{app}\HanhPhuc.exe"; Description: "Launch App"; Flags: nowait postinstall skipifsilent