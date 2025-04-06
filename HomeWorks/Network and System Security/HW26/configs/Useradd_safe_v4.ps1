
Import-Module ActiveDirectory

# ======= OU ========
$baseDN = "DC=lab68,DC=com"

function Ensure-OU {
    param ($Name, $ParentDN)

    $ouDN = "OU=$Name,$ParentDN"

    if (-not (Get-ADOrganizationalUnit -LDAPFilter "(distinguishedName=$ouDN)" -ErrorAction SilentlyContinue)) {
        New-ADOrganizationalUnit -Name $Name -Path $ParentDN
    }
}

# Создание иерархии OU
Ensure-OU -Name "Accounts" -ParentDN $baseDN
Ensure-OU -Name "VIP" -ParentDN "OU=Accounts,$baseDN"
Ensure-OU -Name "Sysadmins" -ParentDN "OU=Accounts,$baseDN"
Ensure-OU -Name "Progr" -ParentDN "OU=Accounts,$baseDN"
Ensure-OU -Name "Buhg" -ParentDN "OU=Accounts,$baseDN"
Ensure-OU -Name "HR" -ParentDN "OU=Accounts,$baseDN"
Ensure-OU -Name "ADM" -ParentDN $baseDN

# ======= Users ========
$users = @(
    @{Name="Alex";    OU="VIP"},
    @{Name="Gleb";    OU="Progr"},
    @{Name="Petr";    OU="Sysadmins"},
    @{Name="Anton";   OU="Progr"},
    @{Name="Igor";    OU="Sysadmins"},
    @{Name="Vasya";   OU="Progr"},
    @{Name="Pavel";   OU="Progr"},
    @{Name="Boris";   OU="Progr"},
    @{Name="Lida";    OU="Buhg"},
    @{Name="Sveta";   OU="VIP"},
    @{Name="Nata";    OU="HR"},
    @{Name="Yana";    OU="HR"},
    @{Name="Maria";   OU="Buhg"},
    @{Name="Ada";     OU="Progr"},
    @{Name="ADMPtr";  OU="ADM"},
    @{Name="ADMIgor"; OU="ADM"}
)

foreach ($u in $users) {
    $username = $u.Name
    $oupath = if ($u.OU -eq "ADM") { "OU=ADM,$baseDN" } else { "OU=$($u.OU),OU=Accounts,$baseDN" }

    if (-not (Get-ADUser -Filter "Name -eq '$username'" -SearchBase $oupath -ErrorAction SilentlyContinue)) {
        New-ADUser -Name $username `
            -GivenName $username `
            -UserPrincipalName "$username@lab68.com" `
            -Path $oupath `
            -AccountPassword (ConvertTo-SecureString "P@ssw0rd!" -AsPlainText -Force) `
            -Enabled $true
    }
}

# ======= Groups and Members ========
$groups = @(
    @{Name="VIP"; OU="VIP"; Members="Alex","Sveta","Petr","Ada","Maria","Anton"},
    @{Name="Sysadmins"; OU="Sysadmins"; Members="Petr","Igor"},
    @{Name="HR"; OU="HR"; Members="Nata","Yana"},
    @{Name="Buhg"; OU="Buhg"; Members="Maria","Lida"},
    @{Name="Progr"; OU="Progr"; Members="Gleb","Vasya","Pavel","Boris","Ada"}
)

foreach ($g in $groups) {
    $gname = $g.Name
    $gpath = "OU=$($g.OU),OU=Accounts,$baseDN"

    if (-not (Get-ADGroup -Filter "Name -eq '$gname'" -SearchBase $gpath -ErrorAction SilentlyContinue)) {
        New-ADGroup -Name $gname -Path $gpath -GroupCategory Security -GroupScope Global
    }

    foreach ($member in $g.Members) {
        Add-ADGroupMember -Identity $gname -Members $member -ErrorAction SilentlyContinue
    }
}

# ======= Domain Admins ========
Add-ADGroupMember -Identity "Domain Admins" -Members "ADMPtr", "ADMIGor" -ErrorAction SilentlyContinue
