# Initialization of Variables
$global:innerText = ""
$global:inventory = @()
$backup_path  = "C:\Backups\SwitchConfigBackup\" + $(get-date -Format "yyyyMMdd")
$user = "switch_backup"
$password = "JkkTxw7Pv9K5AsRbnFGAb5UuBVZgzBuAcmxRRUBhmLb5VeLPvbg6nh8XY9hyt3qw"
$email_title =  "Switch Backup Configuration Failed!"

# Declaration of Function
# Get Device List from ISE Server
Function Get-DeviceList {
    param (
        [string] $User,
        [string] $Password
    )

    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

    Write-Host "Starting device list retrieval..."

    $a = iwr -uri "https://mtlhksvrpise.macroviewhk.com/admin/login.jsp?mid=external_auth_msg#administration/administration_networkresources/administration_networkresources_devices/networkdevices" -SessionVariable session

    $headers = @{
        "Cache-Control"="max-age=0"
        "Origin"="https://mtlhksvrpise.macroviewhk.com"
        "Upgrade-Insecure-Requests" = "1"
        "Accept"="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        "Sec-Fetch-User"="?1"
        "Sec-Fetch-Site"="same-origin"
        "Sec-Fetch-Mode"="navigate"
        "Referer"="https://mtlhksvrpise.macroviewhk.com/admin/login.jsp"
        "Accept-Encoding"="gzip, deflate, br"
        "Accept-Language"="en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6"
    }

    $b = iwr -uri "https://mtlhksvrpise.macroviewhk.com/admin/LoginAction.do" -Method POST -Body $('username='+ $User +'&password='+$password+'&authType=Internal&rememberme=on&name='+$user+'&password='+$password+'&authType=&newPassword=&destinationURL=&xeniaUrl=&locale=en&hasSelectedLocale=false') `
    -ContentType "application/x-www-form-urlencoded" -WebSession $session -Headers $headers

    $c = iwr -Method GET -uri "https://mtlhksvrpise.macroviewhk.com/admin/NetworkDevicesLPInputAction.do?command=restjson&start=0&count=1000&sort=name" -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36" `
    -WebSession $session

    $d = $c.Content | ConvertFrom-json

    Write-Host "Extracting Objects"

    $d.Items | foreach {
        $psObject = New-Object psobject
        Add-Member -InputObject $psobject -MemberType noteproperty -Name Hostname -Value $_.Name
        Add-Member -InputObject $psobject -MemberType noteproperty -Name IP -Value ($_.deviceIpMask.Split("/")[0])
        Add-Member -InputObject $psobject -MemberType noteproperty -Name DeviceType -Value $_.deviceType
        $global:inventory += $psObject.PSOBJECT.Copy()
    }
    $global:inventory = $global:inventory | where {$_.DeviceType -like "*Switch*"}

    Write-Host "Device list retrieval completed."
}

# Call the function
Get-DeviceList -User $user -Password $password

# Output the inventory
#Write-Host "Inventory:"
#$global:inventory | Format-Table -AutoSize

# Export the inventory to a CSV file
$global:inventory | Export-Csv -Path "C:\Users\matthewchs\Downloads\SwitchInventory.csv" -NoTypeInformation

Write-Host "Inventory exported to CSV file."