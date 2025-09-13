#!/usr/bin/env python3
"""
Flipper Zero BadUSB - Webhook Payload Validator
===============================================
Description: Validation et test des payloads avec webhook Discord
Auteur: Plume-Paopedia
Version: 1.0
Usage: python webhook_validator.py [payload_name]
"""

import os
import re
import sys
import json
import requests
import argparse
from datetime import datetime
from pathlib import Path

# Configuration
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1416477793264603249/dxrIG93WCYqELVdSEXtQ7aqioc3MglF1m06Kee476so3zrsRllBg"
PAYLOADS_DIR = Path("../payloads")

def send_discord_message(message, file_path=None):
    """Envoie un message Discord avec ou sans fichier."""
    try:
        if file_path and Path(file_path).exists() and Path(file_path).stat().st_size < 8 * 1024 * 1024:
            # Envoi avec fichier
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'content': message}
                response = requests.post(WEBHOOK_URL, data=data, files=files, timeout=10)
        else:
            # Envoi message seul
            data = {'content': message}
            response = requests.post(WEBHOOK_URL, json=data, timeout=10)
        
        response.raise_for_status()
        return True, "Message envoyé avec succès"
    except requests.exceptions.RequestException as e:
        return False, f"Erreur webhook: {e}"

def analyze_payload(payload_path):
    """Analyse un payload BadUSB."""
    if not payload_path.exists():
        return None, f"Payload {payload_path} introuvable"
    
    try:
        with open(payload_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(payload_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            return None, f"Impossible de lire le fichier: {e}"
    
    analysis = {
        'name': payload_path.stem,
        'lines': len(content.split('\n')),
        'size': len(content),
        'commands': {
            'STRING': len(re.findall(r'^STRING', content, re.MULTILINE)),
            'DELAY': len(re.findall(r'^DELAY|DEFAULT_DELAY', content, re.MULTILINE)),
            'GUI': len(re.findall(r'^GUI', content, re.MULTILINE)),
            'ENTER': len(re.findall(r'^ENTER', content, re.MULTILINE))
        },
        'features': {
            'powershell': 'powershell' in content.lower(),
            'webhook': 'webhook' in content.lower(),
            'discord': 'discord' in content.lower(),
            'stealth': 'hidden' in content.lower() or 'stealth' in content.lower(),
            'error_handling': 'catch' in content.lower() or 'error' in content.lower()
        },
        'estimated_duration_seconds': 0
    }
    
    # Estimation de la durée
    base_delay = 300  # DEFAULT_DELAY typique
    delays = re.findall(r'DELAY (\d+)', content)
    total_delay = sum(int(d) for d in delays) if delays else analysis['commands']['DELAY'] * base_delay
    string_time = analysis['commands']['STRING'] * 100  # ~100ms par commande STRING
    analysis['estimated_duration_seconds'] = (total_delay + string_time) / 1000
    
    return analysis, None

def create_test_report(payload_name, analysis, test_webhook=False):
    """Crée un rapport de test détaillé."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = f"""
═══════════════════════════════════════════════════════════════
RAPPORT DE VALIDATION PAYLOAD - {payload_name.upper()}
═══════════════════════════════════════════════════════════════
Généré le: {timestamp}
Outil: Webhook Payload Validator v1.0

ANALYSE TECHNIQUE:
• Lignes de code: {analysis['lines']}
• Taille du fichier: {analysis['size']} octets
• Commandes STRING: {analysis['commands']['STRING']}
• Instructions DELAY: {analysis['commands']['DELAY']}
• Commandes GUI: {analysis['commands']['GUI']}
• Actions ENTER: {analysis['commands']['ENTER']}
• Durée estimée: {analysis['estimated_duration_seconds']:.1f} secondes

FONCTIONNALITÉS DÉTECTÉES:
• PowerShell: {'✅ OUI' if analysis['features']['powershell'] else '❌ NON'}
• Webhook Discord: {'✅ OUI' if analysis['features']['webhook'] else '❌ NON'}
• Support Discord: {'✅ OUI' if analysis['features']['discord'] else '❌ NON'}
• Mode furtif: {'✅ OUI' if analysis['features']['stealth'] else '❌ NON'}
• Gestion d'erreurs: {'✅ OUI' if analysis['features']['error_handling'] else '❌ NON'}

ÉVALUATION:
"""
    
    # Score de qualité
    score = 0
    if analysis['features']['error_handling']: score += 20
    if analysis['features']['webhook']: score += 30
    if analysis['commands']['STRING'] > 50: score += 20
    if analysis['estimated_duration_seconds'] < 300: score += 15  # Moins de 5 min
    if analysis['lines'] > 100: score += 15
    
    if score >= 80:
        report += "🟢 EXCELLENT (Score: {}%) - Payload professionnel et complet\n".format(score)
    elif score >= 60:
        report += "🟡 BIEN (Score: {}%) - Payload fonctionnel avec améliorations possibles\n".format(score)
    elif score >= 40:
        report += "🟠 MOYEN (Score: {}%) - Payload basique, fonctionnalités limitées\n".format(score)
    else:
        report += "🔴 FAIBLE (Score: {}%) - Payload très basique ou incomplet\n".format(score)
    
    # Recommandations
    report += "\nRECOMMANDATIONS:\n"
    if not analysis['features']['error_handling']:
        report += "• Ajouter la gestion d'erreurs (try/catch)\n"
    if not analysis['features']['webhook']:
        report += "• Intégrer l'envoi via webhook Discord\n"
    if analysis['estimated_duration_seconds'] > 600:
        report += "• Réduire la durée d'exécution (actuellement très longue)\n"
    if analysis['commands']['STRING'] < 20:
        report += "• Enrichir le payload avec plus de fonctionnalités\n"
    
    # Compatibilité
    report += "\nCOMPATIBILITÉ:\n"
    if analysis['features']['powershell']:
        report += "• Windows 7/8/10/11 avec PowerShell 2.0+\n"
        report += "• Nécessite ExecutionPolicy Bypass\n"
    else:
        report += "• Compatible tous Windows (CMD pur)\n"
    
    report += "\n═══════════════════════════════════════════════════════════════\n"
    
    if test_webhook:
        report += "\nTEST WEBHOOK DISCORD:\n"
        success, message = send_discord_message(f"🧪 **Test de validation payload: {payload_name}**")
        report += f"• Envoi test: {'✅ SUCCÈS' if success else '❌ ÉCHEC'}\n"
        if not success:
            report += f"• Erreur: {message}\n"
    
    return report

def validate_all_payloads():
    """Valide tous les payloads du dossier."""
    if not PAYLOADS_DIR.exists():
        print(f"❌ Dossier payloads introuvable: {PAYLOADS_DIR}")
        return
    
    payload_files = list(PAYLOADS_DIR.glob("*.txt"))
    if not payload_files:
        print(f"❌ Aucun payload trouvé dans {PAYLOADS_DIR}")
        return
    
    print(f"🔍 Validation de {len(payload_files)} payloads...")
    print("=" * 60)
    
    results = []
    
    for payload_file in payload_files:
        print(f"\n📄 Analyse de {payload_file.name}...")
        analysis, error = analyze_payload(payload_file)
        
        if error:
            print(f"❌ Erreur: {error}")
            continue
        
        # Affichage résumé
        webhook_status = "✅" if analysis['features']['webhook'] else "❌"
        duration = f"{analysis['estimated_duration_seconds']:.1f}s"
        commands = analysis['commands']['STRING']
        
        print(f"   • Webhook: {webhook_status} | Durée: {duration} | Commandes: {commands}")
        
        results.append((payload_file.name, analysis))
    
    # Envoi résumé Discord
    summary = f"📊 **Validation de {len(results)} payloads BadUSB**\n\n"
    
    for name, analysis in results:
        webhook_emoji = "✅" if analysis['features']['webhook'] else "❌"
        powershell_emoji = "⚡" if analysis['features']['powershell'] else "📟"
        stealth_emoji = "🥷" if analysis['features']['stealth'] else "👁️"
        
        summary += f"• **{name}**: {webhook_emoji} {powershell_emoji} {stealth_emoji} "
        summary += f"({analysis['estimated_duration_seconds']:.0f}s, {analysis['commands']['STRING']} cmds)\n"
    
    summary += f"\n🕐 **Validé le:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    summary += f"\n🛠️ **Outil:** Webhook Payload Validator"
    
    success, message = send_discord_message(summary)
    if success:
        print(f"\n✅ Résumé envoyé sur Discord!")
    else:
        print(f"\n❌ Impossible d'envoyer sur Discord: {message}")
    
    # Sauvegarde rapport local
    report_file = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"RAPPORT GLOBAL DE VALIDATION\n")
        f.write(f"Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        for name, analysis in results:
            f.write(create_test_report(name, analysis))
            f.write("\n\n")
    
    print(f"📄 Rapport détaillé sauvé: {report_file}")

def main():
    parser = argparse.ArgumentParser(description="Validateur de payloads BadUSB avec webhook Discord")
    parser.add_argument('payload', nargs='?', help='Nom du payload à valider (optionnel)')
    parser.add_argument('--test-webhook', action='store_true', help='Tester la connectivité webhook')
    parser.add_argument('--all', action='store_true', help='Valider tous les payloads')
    
    args = parser.parse_args()
    
    print("🧪 Flipper Zero - Webhook Payload Validator")
    print("=" * 45)
    
    if args.all:
        validate_all_payloads()
        return
    
    if args.test_webhook:
        print("🌐 Test de connectivité webhook Discord...")
        test_msg = f"🧪 **Test de connectivité**\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n🛠️ Webhook Payload Validator"
        success, message = send_discord_message(test_msg)
        if success:
            print("✅ Webhook fonctionnel!")
        else:
            print(f"❌ Webhook non fonctionnel: {message}")
        return
    
    if args.payload:
        payload_path = PAYLOADS_DIR / f"{args.payload}.txt"
        if not payload_path.exists():
            payload_path = PAYLOADS_DIR / args.payload
        
        print(f"📄 Validation de {payload_path.name}...")
        analysis, error = analyze_payload(payload_path)
        
        if error:
            print(f"❌ Erreur: {error}")
            return
        
        report = create_test_report(payload_path.stem, analysis, test_webhook=True)
        print(report)
        
        # Sauvegarde
        report_file = f"validation_{payload_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📄 Rapport sauvé: {report_file}")
    else:
        print("Usage:")
        print("  python webhook_validator.py [payload_name]  # Valider un payload")
        print("  python webhook_validator.py --all           # Valider tous")
        print("  python webhook_validator.py --test-webhook  # Test webhook")

if __name__ == "__main__":
    main()