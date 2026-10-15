$src = "C:\Users\AHAN\.gemini\antigravity\scratch\ApexHub\dist\ApexHub"
$dest = "C:\Users\AHAN\AppData\Local\Programs\ApexHub"

Write-Host "1. Installing files to: $dest"
if (Test-Path $dest) {
    Remove-Item -Recurse -Force $dest
}
Copy-Item -Recurse -Force -Path $src -Destination $dest

# Copy icon to dest root for easy shortcut referencing
Copy-Item -Force -Path "C:\Users\AHAN\.gemini\antigravity\scratch\ApexHub\assets\icon.ico" -Destination "$dest\icon.ico"

Write-Host "2. Creating Windows Shortcuts..."
$wsh = New-Object -ComObject WScript.Shell

# Desktop Shortcut
$desktopPath = Join-Path $env:USERPROFILE "Desktop\Apex Hub.lnk"
$sc = $wsh.CreateShortcut($desktopPath)
$sc.TargetPath = "$dest\ApexHub.exe"
$sc.WorkingDirectory = $dest
$sc.IconLocation = "$dest\icon.ico"
$sc.Description = "Apex Hub - Gaming Peripheral Control Suite"
$sc.Save()
Write-Host "   -> Desktop Shortcut created at: $desktopPath"

# Start Menu Shortcut
$programsDir = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
$smPath = Join-Path $programsDir "Apex Hub.lnk"
$smSc = $wsh.CreateShortcut($smPath)
$smSc.TargetPath = "$dest\ApexHub.exe"
$smSc.WorkingDirectory = $dest
$smSc.IconLocation = "$dest\icon.ico"
$smSc.Description = "Apex Hub - Gaming Peripheral Control Suite"
$smSc.Save()
Write-Host "   -> Start Menu Shortcut created at: $smPath"

Write-Host "3. Verifying Installation..."
$installedExe = "$dest\ApexHub.exe"
if ((Test-Path $installedExe) -and (Test-Path $desktopPath) -and (Test-Path $smPath)) {
    Write-Host "SUCCESS: Apex Hub has been successfully installed!" -ForegroundColor Green
} else {
    Write-Host "ERROR: Installation verification failed." -ForegroundColor Red
}
