$exec_name = "eu4"
$queryParameters = '__InstanceCreationEvent', (New-Object TimeSpan 0,0,1), "TargetInstance isa 'Win32_Process' and TargetInstance.Name = '$exec_name.exe'"
$Query = New-Object System.Management.WqlEventQuery -ArgumentList $queryParameters
$ProcessWatcher = New-Object System.Management.ManagementEventWatcher $Query
Register-ObjectEvent -InputObject $ProcessWatcher -EventName "EventArrived" -Action $Function:startAU2ifEU4

function startAU2ifEU4 {
    if (Get-Process | Select-String $exec_name)
    {
        taskkill /im $exec_name.exe /F #Kill process
        Start-Process "steam://rungameid/1066890" #Launch Automobilista2
    }
}