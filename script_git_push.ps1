Param(
    [Parameter(Mandatory=$true)]
    [string]$CommitMessage,

    [string]$Branch = "main",

    [switch]$IncludeGuion
)

$ErrorActionPreference = "Stop"

Write-Host "Verificando repositorio..." -ForegroundColor Cyan
if (-not (Test-Path ".git")) {
    throw "No se encontro .git en la carpeta actual."
}

Write-Host "Remoto configurado:" -ForegroundColor Cyan
git remote -v

if ($IncludeGuion) {
    Write-Host "Agregando todos los cambios (incluye guion)..." -ForegroundColor Yellow
    git add .
} else {
    Write-Host "Agregando cambios excepto guion_video_taller_sivigila.txt..." -ForegroundColor Yellow
    git add .
    git reset -- guion_video_taller_sivigila.txt 2>$null
}

$status = git status --short
if (-not $status) {
    Write-Host "No hay cambios para commit." -ForegroundColor Green
    exit 0
}

Write-Host "Cambios listos para commit:" -ForegroundColor Cyan
git status --short

Write-Host "Creando commit..." -ForegroundColor Cyan
git commit -m "$CommitMessage"

Write-Host "Subiendo a origin/$Branch..." -ForegroundColor Cyan
git push origin $Branch

Write-Host "Proceso finalizado correctamente." -ForegroundColor Green
