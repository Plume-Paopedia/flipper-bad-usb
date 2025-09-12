# Guide d'Installation - Flipper Zero BadUSB Extracteur d'Images

## Prérequis

### Matériel requis
- **Flipper Zero** avec firmware officiel ou custom (Unleashed/RogueMaster recommandé)
- **Câble USB-C** pour connexion au Flipper Zero
- **Ordinateur cible** Windows 7/8/10/11
- **Carte microSD** (recommandée, au moins 8GB pour stocker les payloads)

### Vérifications préliminaires
1. **Firmware Flipper Zero** : Assurez-vous d'avoir une version récente
2. **Module BadUSB** : Vérifiez que le module fonctionne (test avec un payload simple)
3. **Permissions** : Les payloads fonctionnent sans privilèges administrateur

## Installation des Payloads

### Méthode 1: Installation via qFlipper (Recommandée)

1. **Téléchargement**
   ```
   Téléchargez tous les fichiers .txt du dossier /payloads/
   ```

2. **Connexion du Flipper Zero**
   - Connectez votre Flipper Zero via USB
   - Lancez qFlipper

3. **Copie des payloads**
   - Naviguez vers `/ext/badusb/` sur la SD card
   - Créez un dossier `image_extractors/`
   - Copiez tous les fichiers .txt dans ce dossier

4. **Vérification**
   - Débranchez le Flipper Zero
   - Allez dans `BadUSB` → `image_extractors/`
   - Vérifiez que tous les payloads sont visibles

### Méthode 2: Installation manuelle SD Card

1. **Retrait de la carte SD**
   - Éteignez le Flipper Zero
   - Retirez délicatement la carte microSD

2. **Copie sur PC**
   - Insérez la carte SD dans votre PC
   - Naviguez vers `ext/badusb/`
   - Créez le dossier `image_extractors/`
   - Copiez tous les fichiers .txt

3. **Réinsertion**
   - Réinsérez la carte SD dans le Flipper Zero
   - Redémarrez l'appareil

## Structure des Payloads

### Organisation recommandée sur SD Card
```
/ext/badusb/image_extractors/
├── quick_extract.txt          # Extraction rapide (< 5 min)
├── full_extract.txt           # Extraction complète (10-30 min)
├── stealth_extract.txt        # Extraction furtive
├── smart_extract.txt          # Extraction intelligente avec déduplication
├── universal_extract.txt      # Compatible toutes versions Windows
└── custom/                    # Vos payloads personnalisés
    ├── payload_generator.bat
    └── [payloads personnalisés]
```

## Configuration du Flipper Zero

### Paramètres BadUSB
1. **Accès au menu**
   ```
   Menu Principal → BadUSB → Config
   ```

2. **Layout clavier** (Important!)
   - Par défaut: `EN (US)`
   - Pour AZERTY: Changez en `FR` si disponible
   - Ou utilisez les versions AZERTY des payloads

3. **Paramètres de délai**
   - Les payloads incluent `DEFAULT_DELAY` optimisé
   - Modifiez si nécessaire selon votre système cible

### Test de fonctionnement

1. **Test basique**
   - Connectez le Flipper Zero à un PC de test
   - Chargez `quick_extract.txt`
   - Vérifiez que les commandes s'exécutent correctement

2. **Vérification clavier**
   - Si les caractères sont incorrects, ajustez le layout
   - Testez particulièrement `@`, `\`, et les caractères spéciaux

## Dépannage Installation

### Problème: Payloads non visibles
**Solution:**
- Vérifiez l'extension `.txt`
- Assurez-vous que les fichiers ne sont pas corrompus
- Reformatez la SD card si nécessaire (FAT32)

### Problème: Erreurs de caractères
**Solution:**
- Changez le layout clavier dans BadUSB settings
- Utilisez les versions universelles (CMD pur)

### Problème: Firmware non compatible
**Solution:**
- Mettez à jour vers firmware officiel récent
- Ou utilisez Unleashed/RogueMaster pour plus de fonctionnalités

## Sécurisation des Payloads

### Protection des fichiers
```
Renommez vos payloads avec des noms discrets:
- quick_extract.txt → maintenance.txt
- full_extract.txt → system_check.txt
- stealth_extract.txt → update_check.txt
```

### Masquage sur SD Card
```
Créez des sous-dossiers pour organiser:
/ext/badusb/
├── demos/              # Payloads de démonstration
├── maintenance/        # Payloads d'extraction (nom discret)
└── tools/             # Utilitaires et générateurs
```

## Validation de l'Installation

### Checklist finale
- [ ] Flipper Zero connecté et reconnu
- [ ] Module BadUSB accessible
- [ ] Tous les payloads présents dans `/ext/badusb/image_extractors/`
- [ ] Layout clavier configuré
- [ ] Test sur machine de développement réussi

### Tests recommandés
1. **Test du payload rapide** sur votre propre PC
2. **Vérification des permissions** (pas d'admin requis)
3. **Test de la génération de rapports**
4. **Validation de l'ouverture automatique des dossiers**

## Maintenance

### Mises à jour
- Vérifiez régulièrement les nouvelles versions
- Sauvegardez vos configurations personnalisées
- Testez les nouveaux payloads avant utilisation

### Sauvegarde
```
Sauvegardez régulièrement:
- Votre configuration Flipper Zero
- Vos payloads personnalisés
- Vos paramètres de layout clavier
```

## Support

### En cas de problème
1. Consultez d'abord ce guide
2. Vérifiez les [Issues GitHub](https://github.com/Plume-Paopedia/flipper-bad-usb/issues)
3. Testez avec un payload plus simple
4. Vérifiez la compatibilité firmware

### Logs de débogage
```
Pour diagnostiquer:
1. Utilisez d'abord universal_extract.txt (plus stable)
2. Vérifiez les rapports générés pour identifier les erreurs
3. Testez sur plusieurs versions de Windows
```