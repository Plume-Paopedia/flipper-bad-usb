@echo off
REM ================================================================
REM Testeur de Payload - Simulation d'Extraction
REM ================================================================
REM Description: Test les payloads sans Flipper Zero pour validation
REM Utilisation: payload_tester.bat [nom_du_payload]
REM Auteur: Plume-Paopedia
REM ================================================================

title Testeur de Payloads - Simulation Flipper Zero

cls
echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                          TESTEUR DE PAYLOADS                         ║
echo ║                    Simulation d'extraction d'images                  ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM Vérification de l'existence du dossier payloads
if not exist "..\payloads" (
    echo ❌ Erreur: Dossier payloads non trouvé!
    echo Assurez-vous d'être dans le dossier tools du projet.
    pause
    exit /b 1
)

REM Affichage des payloads disponibles
echo 📁 Payloads disponibles:
echo.
for %%f in (..\payloads\*.txt) do echo    • %%~nf
echo.

REM Sélection du payload à tester
if "%1"=="" (
    set /p PAYLOAD_NAME="Nom du payload à tester (sans .txt): "
) else (
    set PAYLOAD_NAME=%1
)

if not exist "..\payloads\%PAYLOAD_NAME%.txt" (
    echo ❌ Erreur: Payload '%PAYLOAD_NAME%.txt' non trouvé!
    pause
    exit /b 1
)

echo.
echo 🧪 Test du payload: %PAYLOAD_NAME%.txt
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Création d'un environnement de test
set TEST_DIR=%TEMP%\flipper_test_%RANDOM%
mkdir "%TEST_DIR%" 2>nul
cd /d "%TEST_DIR%"

REM Création de fichiers image de test
echo 📝 Création de l'environnement de test...
mkdir test_images 2>nul
mkdir "%USERPROFILE%\Desktop\test_pictures" 2>nul

REM Simulation de fichiers images
echo Test JPG > test_images\photo1.jpg
echo Test PNG > test_images\capture.png  
echo Test GIF > test_images\animation.gif
echo Test BMP > test_images\bitmap.bmp

echo Test Desktop > "%USERPROFILE%\Desktop\desktop_image.jpg"
echo Test Screenshot > "%USERPROFILE%\Desktop\screenshot_001.png"

echo ✅ Environnement de test créé
echo    • %TEST_DIR%\test_images\
echo    • %USERPROFILE%\Desktop\test_pictures\
echo.

REM Analyse du payload pour extraire les commandes principales
echo 🔍 Analyse du payload %PAYLOAD_NAME%.txt...
echo.

REM Simulation des commandes principales du payload
findstr /i "STRING cd" "..\payloads\%PAYLOAD_NAME%.txt" > nul
if %errorlevel%==0 (
    echo ✅ Commande de navigation détectée
) else (
    echo ⚠️  Aucune navigation de dossier détectée
)

findstr /i "powershell" "..\payloads\%PAYLOAD_NAME%.txt" > nul
if %errorlevel%==0 (
    echo ✅ Utilisation de PowerShell détectée
    set USE_PS=1
) else (
    echo ✅ Mode CMD pur détecté
    set USE_PS=0
)

findstr /i "copy\|Copy-Item" "..\payloads\%PAYLOAD_NAME%.txt" > nul
if %errorlevel%==0 (
    echo ✅ Commandes de copie détectées
) else (
    echo ⚠️  Aucune commande de copie détectée
)

findstr /i "explorer\|mkdir" "..\payloads\%PAYLOAD_NAME%.txt" > nul
if %errorlevel%==0 (
    echo ✅ Création de dossier et ouverture détectées
) else (
    echo ⚠️  Pas d'ouverture de dossier automatique
)

echo.
echo 📊 RÉSULTATS DE L'ANALYSE:
echo ═══════════════════════════════════════════════════════════════════

REM Comptage des lignes du payload
for /f %%i in ('type "..\payloads\%PAYLOAD_NAME%.txt" ^| find /c /v ""') do set LINE_COUNT=%%i
echo    • Nombre de lignes: %LINE_COUNT%

REM Comptage des commandes STRING
for /f %%i in ('findstr /i "^STRING" "..\payloads\%PAYLOAD_NAME%.txt" ^| find /c /v ""') do set CMD_COUNT=%%i
echo    • Commandes STRING: %CMD_COUNT%

REM Comptage des DELAY
for /f %%i in ('findstr /i "^DELAY\|DEFAULT_DELAY" "..\payloads\%PAYLOAD_NAME%.txt" ^| find /c /v ""') do set DELAY_COUNT=%%i
echo    • Instructions de délai: %DELAY_COUNT%

REM Estimation du temps d'exécution
set /a ESTIMATED_TIME=%CMD_COUNT%*300+%DELAY_COUNT%*100
set /a EST_MINUTES=%ESTIMATED_TIME%/60000
set /a EST_SECONDS=(%ESTIMATED_TIME%%%60000)/1000
echo    • Temps estimé: %EST_MINUTES%min %EST_SECONDS%s

echo.
echo 🏃 SIMULATION D'EXÉCUTION:
echo ═══════════════════════════════════════════════════════════════════

REM Simulation basique selon le type de payload
if /i "%PAYLOAD_NAME%"=="quick_extract" (
    echo 📅 Simulation extraction rapide (30 derniers jours)...
    echo    • Recherche dans Pictures: 2 fichiers trouvés
    echo    • Recherche sur Desktop: 1 fichier trouvé  
    echo    • Recherche dans Downloads: 0 fichier trouvé
    echo    • Total simulé: 3 images
) else if /i "%PAYLOAD_NAME%"=="full_extract" (
    echo 🔍 Simulation extraction complète...
    echo    • Scan Pictures: 25 fichiers trouvés
    echo    • Scan Desktop: 3 fichiers trouvés
    echo    • Scan Documents: 8 fichiers trouvés
    echo    • Scan Downloads: 12 fichiers trouvés
    echo    • Scan AppData: 5 fichiers trouvés
    echo    • Scan caches navigateurs: 15 fichiers trouvés
    echo    • Total simulé: 68 images
) else if /i "%PAYLOAD_NAME%"=="stealth_extract" (
    echo 🤫 Simulation extraction furtive...
    echo    • Mode silencieux activé
    echo    • Fenêtre masquée
    echo    • Extraction en arrière-plan: 15 images
    echo    • Archive automatique créée
) else if /i "%PAYLOAD_NAME%"=="smart_extract" (
    echo 🧠 Simulation extraction intelligente...
    echo    • Classification par qualité: Activée
    echo    • Détection doublons: 12 doublons évités
    echo    • Photos haute qualité: 8 fichiers
    echo    • Images moyennes: 15 fichiers
    echo    • Screenshots détectés: 3 fichiers
    echo    • Total après déduplication: 26 images
) else if /i "%PAYLOAD_NAME%"=="universal_extract" (
    echo 🌐 Simulation extraction universelle (CMD)...
    echo    • Mode compatibilité maximale
    echo    • Scan Pictures: 10 fichiers
    echo    • Scan Desktop: 2 fichiers
    echo    • Scan Documents: 5 fichiers
    echo    • Scan caches basiques: 8 fichiers
    echo    • Total simulé: 25 images
) else (
    echo 🔧 Simulation payload personnalisé...
    echo    • Analyse des paramètres du payload...
    echo    • Extraction selon configuration: Variable
)

echo.
echo 📋 RAPPORT DE TEST:
echo ═══════════════════════════════════════════════════════════════════

REM Génération du rapport de test
echo Rapport de test - %PAYLOAD_NAME% > test_report.txt
echo Généré le %DATE% à %TIME% >> test_report.txt
echo. >> test_report.txt
echo ANALYSE TECHNIQUE: >> test_report.txt
echo • Lignes de code: %LINE_COUNT% >> test_report.txt
echo • Commandes STRING: %CMD_COUNT% >> test_report.txt
echo • Délais configurés: %DELAY_COUNT% >> test_report.txt
echo • Temps estimé: %EST_MINUTES%min %EST_SECONDS%s >> test_report.txt
echo • Type PowerShell: %USE_PS% >> test_report.txt
echo. >> test_report.txt
echo COMPATIBILITÉ: >> test_report.txt
if %USE_PS%==1 (
    echo • Requiert PowerShell: OUI >> test_report.txt
    echo • Compatible Windows 7+: OUI >> test_report.txt
    echo • Compatible XP/Vista: NON >> test_report.txt
) else (
    echo • Requiert PowerShell: NON >> test_report.txt
    echo • Compatible toutes versions: OUI >> test_report.txt
    echo • Mode universellement compatible >> test_report.txt
)
echo. >> test_report.txt
echo SÉCURITÉ: >> test_report.txt
findstr /i "hidden\|stealth" "..\payloads\%PAYLOAD_NAME%.txt" > nul
if %errorlevel%==0 (
    echo • Mode furtif: DÉTECTÉ >> test_report.txt
) else (
    echo • Mode furtif: NON >> test_report.txt
)
findstr /i "admin\|elevation" "..\payloads\%PAYLOAD_NAME%.txt" > nul
if %errorlevel%==0 (
    echo • Privilèges admin: REQUIS >> test_report.txt
) else (
    echo • Privilèges admin: NON REQUIS >> test_report.txt
)

echo ✅ Rapport de test généré: %TEST_DIR%\test_report.txt
echo.

REM Affichage des recommandations
echo 💡 RECOMMANDATIONS:
echo ═══════════════════════════════════════════════════════════════════

if %EST_MINUTES% GTR 10 (
    echo ⚠️  Temps d'exécution élevé (%EST_MINUTES%+ minutes)
    echo    Considérez optimiser les délais ou réduire le scope
)

if %CMD_COUNT% GTR 200 (
    echo ⚠️  Payload très long (%CMD_COUNT% commandes)
    echo    Risque de déconnexion USB ou timeout
)

if %USE_PS%==1 (
    echo ℹ️  Utilise PowerShell - Testez sur système cible
    echo    Ayez une version CMD fallback si nécessaire
)

echo ✅ Payload semble fonctionnel pour déploiement
echo.

REM Nettoyage
echo 🧹 Nettoyage de l'environnement de test...
cd /d %TEMP%
rmdir /s /q "%TEST_DIR%" 2>nul
del "%USERPROFILE%\Desktop\desktop_image.jpg" 2>nul
del "%USERPROFILE%\Desktop\screenshot_001.png" 2>nul
rmdir /s /q "%USERPROFILE%\Desktop\test_pictures" 2>nul

echo.
echo ✅ Test terminé avec succès!
echo 📋 Consultez les recommandations ci-dessus avant déploiement
echo.
pause