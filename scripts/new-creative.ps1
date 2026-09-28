param(
  [Parameter(Mandatory=$true)][string]$Slug,
  [string]$Objective = "conversion"
)

$ErrorActionPreference = "Stop"
# Uma pasta por peca (sem data/formato/versao no nome). Ver docs/NAMING.md.
$root = Join-Path "outputs" $Slug

if (Test-Path $root) {
  throw "A peca '$Slug' ja existe em $root. Para uma nova versao, rode o gerador com --nova-versao (versoes anteriores vao para versoes/)."
}
New-Item -ItemType Directory -Path $root | Out-Null
foreach ($d in @("projeto", "previews", "versoes", ".tesseract-work")) {
  New-Item -ItemType Directory -Path (Join-Path $root $d) | Out-Null
}

$date = Get-Date -Format "yyyy-MM-dd"
$brief = @("# Brief - $Slug","","Criado em: $date","Objetivo: $Objective","Formatos: feed-4x5, stories-9x16","","Preencha/aponte:","- URL do produto","- snapshot comercial (data/<slug>/)","- assets autorizados","- hook/headline/CTA","- restricoes")
Set-Content -Path (Join-Path $root "brief.md") -Value $brief -Encoding UTF8
Set-Content -Path (Join-Path $root "notes.md") -Value "# Notas - v01" -Encoding UTF8
Set-Content -Path (Join-Path $root "versao.txt") -Value "v01" -Encoding UTF8
Write-Host "Peca criada:" $root
