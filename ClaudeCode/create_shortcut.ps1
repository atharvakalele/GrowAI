$WshShell = New-Object -comObject WScript.Shell
$Desktop = [System.Environment]::GetFolderPath('Desktop')
$LinkPath = "$Desktop\AutoGrow AI Dashboard.lnk"
$Shortcut = $WshShell.CreateShortcut($LinkPath)
$Shortcut.TargetPath = 'C:\Users\Clu\Documents\Be Extra Carefull Sonet Amazon Bussiness Grouth Automation AI\ClaudeCode\run_dashboard.bat'
$Shortcut.WorkingDirectory = 'C:\Users\Clu\Documents\Be Extra Carefull Sonet Amazon Bussiness Grouth Automation AI'
$Shortcut.IconLocation = 'C:\Windows\System32\imageres.dll, 109'
$Shortcut.Description = 'AutoGrow AI Dashboard'
$Shortcut.Save()
Write-Host "Shortcut created at: $LinkPath"
