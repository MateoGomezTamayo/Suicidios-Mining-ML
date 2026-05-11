# =============================================================
#  deploy.ps1  —  Punto de entrada principal Terraform
# =============================================================
#  Uso desde la carpeta Terraform/:
#    .\deploy.ps1 -Env dev -Command init
#    .\deploy.ps1 -Env dev -Command plan
#    .\deploy.ps1 -Env dev -Command apply
# =============================================================

param(
    [Parameter(Mandatory = $false)]
    [ValidateSet("dev")]
    [string]$Env = "dev",

    [Parameter(Mandatory = $false)]
    [ValidateSet("init", "plan", "apply", "destroy", "output", "validate", "fmt")]
    [string]$Command = "plan"
)

$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Definition
$EnvScript  = Join-Path $ScriptDir "gestion_direccion_big_data\terraform\envs\$Env\run_terraform.ps1"

if (-not (Test-Path $EnvScript)) {
    Write-Error "No se encontro el script para el entorno '$Env' en: $EnvScript"
    exit 1
}

Write-Host "Delegando a entorno: $Env" -ForegroundColor Cyan
& $EnvScript -Command $Command
exit $LASTEXITCODE
