$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptPath

Write-Host "Starting Server..."
Start-Process python -ArgumentList "chat_server.py"
Start-Sleep -Seconds 2

Write-Host "Starting Client 1..."
Start-Process python -ArgumentList "chat_cmdl_client.py"
Start-Sleep -Seconds 1

Write-Host "Starting Client 2..."
Start-Process python -ArgumentList "chat_cmdl_client.py"
Start-Sleep -Seconds 1

Write-Host "All systems launched!"
