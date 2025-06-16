param(
    [int]$Exponent = 82589933
)

# Load BigInteger
Add-Type -AssemblyName System.Numerics

Write-Host "Computing 2^$Exponent - 1 …"
$t0 = Get-Date

# Fast exponentiation
$P = [System.Numerics.BigInteger]::Pow(2, $Exponent) - 1

$elapsed = (Get-Date) - $t0
Write-Host "✅ Done in $([math]::Round($elapsed.TotalSeconds,3)) s; P has $($P.ToString().Length) digits"
