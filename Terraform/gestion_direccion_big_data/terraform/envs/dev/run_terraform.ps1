# =============================================================
#  run_terraform.ps1  —  Ejecutor de Terraform para env: dev
# =============================================================
#  Uso:
#    .\run_terraform.ps1 -Command init
#    .\run_terraform.ps1 -Command plan
#    .\run_terraform.ps1 -Command apply
#    .\run_terraform.ps1 -Command destroy
#    .\run_terraform.ps1 -Command output
#    .\run_terraform.ps1 -Command validate
# =============================================================

param(
    [Parameter(Mandatory = $false)]
    [ValidateSet("init", "plan", "apply", "destroy", "output", "validate", "fmt")]
    [string]$Command = "plan"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── Rutas ────────────────────────────────────────────────────
$ScriptDir    = Split-Path -Parent $MyInvocation.MyCommand.Definition
$TerraformExe = [System.IO.Path]::GetFullPath((Join-Path $ScriptDir "..\..\..\..\Terraform\terraform.exe"))
$VarFile      = Join-Path $ScriptDir "dev.tfvars"

# ── Validaciones previas ─────────────────────────────────────
if (-not (Test-Path $TerraformExe)) {
    Write-Error "No se encontro terraform.exe en: $TerraformExe`nVerifica que el binario existe en Terraform\Terraform\terraform.exe"
    exit 1
}

if (-not (Test-Path $VarFile)) {
    Write-Error "No se encontro el archivo de variables: $VarFile"
    exit 1
}

# ── Info de entorno ───────────────────────────────────────────
Write-Host ""
Write-Host "============================================" -ForegroundColor DarkCyan
Write-Host "  Terraform — Entorno: dev" -ForegroundColor Cyan
Write-Host "  Comando  : $Command" -ForegroundColor Cyan
Write-Host "  Binario  : $TerraformExe" -ForegroundColor Gray
Write-Host "  Dir      : $ScriptDir" -ForegroundColor Gray
Write-Host "============================================" -ForegroundColor DarkCyan
Write-Host ""

# ── Cambiar al directorio de trabajo ─────────────────────────
Push-Location $ScriptDir

try {
    switch ($Command) {
        "init" {
            Write-Host "[1/1] Inicializando backend y modulos..." -ForegroundColor Yellow
            & $TerraformExe init
        }
        "validate" {
            & $TerraformExe validate
        }
        "fmt" {
            & $TerraformExe fmt -recursive
        }
        "plan" {
            Write-Host "[1/1] Generando plan de ejecucion..." -ForegroundColor Yellow
            & $TerraformExe plan -var-file="$VarFile"
        }
        "apply" {
            Write-Host "[1/1] Aplicando infraestructura..." -ForegroundColor Green
            & $TerraformExe apply -var-file="$VarFile"
        }
        "destroy" {
            Write-Host ""
            Write-Host "ATENCION: Esto eliminara la infraestructura del entorno dev." -ForegroundColor Red
            $confirm = Read-Host "Escribe 'si' para confirmar"
            if ($confirm -ne "si") {
                Write-Host "Operacion cancelada." -ForegroundColor Yellow
                exit 0
            }
            & $TerraformExe destroy -var-file="$VarFile"
        }
        "output" {
            & $TerraformExe output
        }
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Terraform termino con codigo de error: $LASTEXITCODE"
        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "Completado exitosamente." -ForegroundColor Green
}
finally {
    Pop-Location
}
