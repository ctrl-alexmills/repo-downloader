; Inno Setup script for Repo Downloader
; Builds  Output\RepoDownloader-Setup-<version>.exe  from  dist\Repo Downloader.exe
;
; Build the exe first (build_exe.bat), then:
;   iscc /DMyAppVersion=1.0.0 installer.iss
; The GitHub release workflow does both steps automatically.

#ifndef MyAppVersion
  #define MyAppVersion "0.0.0-dev"
#endif

#define MyAppName "Repo Downloader"
#define MyAppExeName "Repo Downloader.exe"
#define MyAppURL "https://github.com/ctrl-alexmills/Github-POC"

[Setup]
; Never change AppId - Windows uses it to recognise upgrades and uninstalls
AppId={{8C623921-1505-4161-A267-397464770FAD}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=Alex Mills
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
; Install just for the current user: no admin prompt needed.
; {autopf} then means  %LOCALAPPDATA%\Programs
PrivilegesRequired=lowest
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
OutputDir=Output
OutputBaseFilename=RepoDownloader-Setup-{#MyAppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent
