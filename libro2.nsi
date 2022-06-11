Name "Libro2"
OutFile "installer\libro2.win32.installer.exe"
RequestExecutionLevel admin
Unicode True
InstallDir $PROGRAMFILES\Libro2

Page directory
Page instfiles

Section "Install Libro2"
    SetOutPath $INSTDIR
    File /r "dist\libro2\*"

    ; Write the installation path into the registry
    WriteRegStr HKLM SOFTWARE\Libro2 "Install_Dir" "$INSTDIR"
  
    ; Write the uninstall keys for Windows
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Libro2" "DisplayName" "Libro2"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Libro2" "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Libro2" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Libro2" "NoRepair" 1
    WriteUninstaller "$INSTDIR\uninstall.exe"  
SectionEnd

Section "Start Menu Shortcuts"
  CreateShortcut "$SMPROGRAMS\Libro2.lnk" "$INSTDIR\libro2.exe"
SectionEnd

Section "Uninstall"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Libro2"
    DeleteRegKey HKLM SOFTWARE\Libro2  

    Delete $INSTDIR\uninstall.exe
    Delete "$SMPROGRAMS\Libro2.lnk"
    RMDir /r "$INSTDIR"
SectionEnd