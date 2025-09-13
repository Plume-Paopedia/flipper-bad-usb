# 🔗 Documentation Webhook Discord

## Vue d'ensemble

Les payloads BadUSB avec intégration Discord webhook permettent de recevoir automatiquement les résultats d'extraction, les rapports d'erreur et les échantillons d'images directement sur Discord.

## 🚀 Payloads avec Webhook

### 1. `webhook_extract.txt` - Extraction avec Webhook
**Fonctionnalités principales :**
- Extraction d'images avec filtres personnalisables
- Envoi automatique des résultats sur Discord
- Rapport de progression en temps réel
- Échantillons d'images envoyés automatiquement
- Gestion complète des erreurs avec notification

**Utilisation recommandée :** Extraction standard avec suivi Discord

### 2. `smart_webhook.txt` - Extraction Intelligente + Webhook
**Fonctionnalités avancées :**
- Classification automatique par catégories (HQ, Screenshots, Récentes, Cache)
- Déduplication par hash MD5
- Organisation en dossiers thématiques
- Envoi Discord par catégorie avec émojis spécifiques
- Rapport d'efficacité détaillé

**Utilisation recommandée :** Extraction professionnelle avec analyse poussée

### 3. `error_reporter.txt` - Diagnostic Système + Webhook
**Fonctionnalités spécialisées :**
- Diagnostic système complet (OS, matériel, services)
- Analyse des logs Windows (System + Application)
- Test de connectivité réseau
- Rapport de santé du système
- Envoi automatique du diagnostic sur Discord

**Utilisation recommandée :** Diagnostic système et rapport d'état

### 4. `webhook_test.txt` - Test de Connectivité
**Fonctionnalités de validation :**
- Test de connectivité Discord
- Test d'envoi de message simple
- Test d'envoi de fichier
- Diagnostic réseau complet
- Validation complète du webhook

**Utilisation recommandée :** Validation avant déploiement des autres payloads

## 🛠️ Configuration du Webhook

### Étape 1 : Création du Webhook Discord

1. **Accès aux paramètres du salon :**
   - Sur Discord, allez sur le salon souhaité
   - Clic droit → "Modifier le salon" 
   - Onglet "Intégrations"

2. **Création du webhook :**
   - Cliquez sur "Créer un webhook"
   - Donnez-lui un nom (ex: "Flipper-BadUSB")
   - Copiez l'URL du webhook

3. **URL format :**
   ```
   https://discord.com/api/webhooks/[WEBHOOK_ID]/[WEBHOOK_TOKEN]
   ```

### Étape 2 : Configuration dans les Payloads

**Modification manuelle :**
1. Ouvrez le fichier payload (ex: `webhook_extract.txt`)
2. Trouvez la ligne :
   ```
   STRING $webhookUrl = "https://discordapp.com/api/webhooks/..."
   ```
3. Remplacez l'URL par votre webhook Discord
4. Sauvegardez le fichier

**Utilisation du générateur :**
1. Utilisez `webhook_generator.py` pour créer un payload personnalisé
2. L'outil demande automatiquement votre URL webhook
3. Le payload généré utilise votre configuration

### Étape 3 : Test et Validation

```bash
# Test de connectivité
python tools/webhook_validator.py --test-webhook

# Validation d'un payload
python tools/webhook_validator.py webhook_extract

# Test complet sur Flipper Zero
# Utilisez webhook_test.txt pour un test complet
```

## 📊 Types de Messages Discord

### Messages de Démarrage
```
🔄 **Extraction démarrée** sur DESKTOP-ABC123
⏰ Début: 14:30:15
```

### Messages de Progression
```
📊 **Progression**: 150 images extraites (25.6 MB)
📂 **Scan en cours:** Pictures
⚡ **Progression:** 150 extraites | 12 doublons évités | 25.6 MB
```

### Messages de Fin
```
🎯 **Extraction terminée!**

📊 **Statistiques:**
• Images extraites: **247**
• Taille totale: **86.3 MB**
• Machine: **DESKTOP-ABC123**
• Utilisateur: **john.doe**
• Durée: **8min 23s**
• Efficacité: **87.3%**

📁 **Répartition par catégorie:**
• ⭐ **HighQuality**: 45 images
• 📸 **Screenshots**: 12 images
• 🆕 **Recent**: 89 images
• 💾 **Cache**: 23 images
```

### Messages d'Erreur
```
❌ **ERREUR CRITIQUE**: Access denied sur DESKTOP-ABC123
⚠️ **Erreurs détectées** (12 erreurs):
```
• Accès refusé au dossier C:\Users\Admin\Pictures
• Service Spooler: Arrêté
• Connectivité réseau limitée
```
```

### Messages avec Fichiers
```
📄 **Rapport détaillé ci-joint**
[RAPPORT_EXTRACTION.txt]

🖼️ **Échantillon des images** (3/247):
[sample_image_1.jpg]
[sample_image_2.png]
[sample_image_3.gif]
```

## 🔧 Outils Python

### webhook_validator.py

**Installation :**
```bash
cd tools/
pip install -r requirements.txt
```

**Utilisation :**
```bash
# Test webhook
python webhook_validator.py --test-webhook

# Validation payload
python webhook_validator.py webhook_extract

# Validation globale
python webhook_validator.py --all
```

**Fonctionnalités :**
- Analyse technique complète des payloads
- Score de qualité avec recommandations
- Test de connectivité Discord
- Rapport détaillé automatique

### webhook_generator.py

**Utilisation :**
```bash
python webhook_generator.py
```

**Configuration interactive :**
1. Nom du payload et métadonnées
2. Sélection des emplacements à scanner
3. Choix des types d'images (standard, RAW, professionnel)
4. Configuration des filtres (taille, âge)
5. Options avancées (progression, mode furtif)
6. Génération automatique du payload

**Avantages :**
- Interface guidée intuitive
- Validation automatique des paramètres
- Code DuckyScript optimisé généré
- Webhook Discord intégré nativement
- Estimation de durée précise

## 🚨 Sécurité et Bonnes Pratiques

### Protection du Webhook

⚠️ **L'URL webhook est sensible** - elle donne accès à votre salon Discord !

**Recommandations :**
1. **Salon dédié** : Créez un salon spécifique pour les rapports BadUSB
2. **Permissions restreintes** : Limitez l'accès au salon
3. **Surveillance** : Surveillez l'utilisation pour détecter les abus
4. **Rotation** : Changez périodiquement l'URL webhook
5. **Pas de partage public** : Ne partagez jamais l'URL complète

### Gestion des Erreurs

Les payloads incluent une gestion robuste des erreurs :

1. **Fallback local** : Sauvegarde locale si Discord indisponible
2. **Rate limiting** : Respect des limites Discord API
3. **Retry logic** : Tentatives répétées en cas d'échec temporaire
4. **Logs d'erreur** : Journalisation locale des problèmes webhook

## 📈 Performance et Optimisations

### Impact sur les Performances

**Temps additionnel dû au webhook :**
- Envoi messages simples : +1-2 secondes
- Envoi avec fichiers : +3-10 secondes selon taille
- Total impact : +10-30 secondes par extraction

**Optimisations implémentées :**
- Compression automatique des images > 8MB
- Rate limiting pour éviter les erreurs Discord
- Envois en batch pour réduire la latence
- Fallback silencieux en cas de problème réseau

### Recommandations d'Usage

**Pour extraction rapide :**
- Utilisez `webhook_extract.txt` (rapport standard)
- Activez seulement les notifications essentielles

**Pour analyse complète :**
- Utilisez `smart_webhook.txt` (classification avancée)
- Exploitez les rapports par catégorie

**Pour diagnostic système :**
- Utilisez `error_reporter.txt` (santé du système)
- Idéal pour surveillance périodique

## 🔄 Dépannage

### Problèmes Courants

**Webhook ne fonctionne pas :**
1. Vérifiez l'URL (format correct)
2. Testez avec `webhook_test.txt`
3. Vérifiez les permissions Discord
4. Contrôlez la connectivité réseau

**Messages coupés :**
- Discord limite à 2000 caractères par message
- Les payloads divisent automatiquement les longs messages

**Images non envoyées :**
- Limite Discord : 8MB par fichier
- Vérifiez la taille des images
- Les gros fichiers sont référencés, pas envoyés

**Erreurs de rate limiting :**
- Discord limite : 30 requêtes/minute
- Les payloads incluent des délais automatiques
- Attendez quelques minutes avant de relancer

### Logs de Dépannage

**Logs locaux :**
- Erreurs webhook : `%TEMP%\discord_webhook_errors.log`
- Rapports d'extraction : `RAPPORT_EXTRACTION.txt`
- Logs système : `diagnostic_[timestamp].txt`

**Validation Python :**
```bash
# Test complet avec rapport détaillé
python webhook_validator.py webhook_extract

# Le rapport inclut :
# - Analyse technique
# - Test de connectivité  
# - Recommandations
# - Score de qualité
```

## 📚 Exemples d'Usage

### Scénario 1 : Reconnaissance Rapide
```
1. Utilisez webhook_test.txt (validation)
2. Puis webhook_extract.txt (extraction)
3. Surveillez Discord pour les résultats
4. Images importantes envoyées automatiquement
```

### Scénario 2 : Analyse Professionnelle
```
1. Configurez smart_webhook.txt
2. Extraction avec classification automatique
3. Rapport Discord par catégorie
4. Dossiers locaux organisés
```

### Scénario 3 : Diagnostic Système
```
1. Lancez error_reporter.txt
2. Diagnostic complet en 2-5 minutes
3. Rapport système sur Discord
4. Identification des problèmes
```

Ce système webhook transforme les payloads BadUSB traditionnels en outils modernes connectés, facilitant le suivi et l'analyse des résultats en temps réel.