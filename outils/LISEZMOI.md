# Outils de production des visuels

- `visuel.py` : génère un visuel PNG 1080x1350 (météo ou article avec photo) à partir d'une fiche JSON. Voir l'en-tête du fichier.
- `chercher_photo.py` et `telecharger_photo.py` : recherche de photos sur Wikimedia Commons et Unsplash, avec auteur et licence.
- `photos/` : photos déjà validées, réutilisables sans crédit sur le visuel (laisser `credit` vide) :
  - `stade-nuit.jpg` : Alex Simpson / Unsplash
  - `stade-raymond-kopa.jpg` : M. Mouchoir / Wikimedia Commons, domaine public
  - `patinage.jpg` : Kelli McClintock / Unsplash

## Règle sur les crédits photo

Choix éditorial d'Angers Direct : pas de crédit affiché sur les photos d'illustration (Unsplash, domaine public).
Le crédit n'est affiché que lorsque la licence l'impose, par exemple une photo Wikimedia sous CC BY ou CC BY-SA : « Photo : Auteur / Wikimedia Commons, CC BY-SA 4.0 ».
Dans le doute, préférer une photo Unsplash.

Les images publiées vont dans un dossier daté (`AAAA-MM-JJ/`). Lien public : `https://raw.githubusercontent.com/angersdirect-a11y/angersdirect-visuels/main/<dossier>/<fichier>.png`.

## Visuels sport (`sport.py`)

Cinq modèles, sur le style des maquettes Angers Direct : `score` (score final avec buteurs et statistiques), `classement` (Ligue 1, ligne d'Angers surlignée), `calendrier` (matchs du mois), `jdm_story` (jour de match 1080x1920) et `jdm_paysage` (jour de match 1920x1080).
Exemples de fiches dans `outils/exemples/`. Logos des 18 clubs de Ligue 1 dans `outils/logos/<slug>.png`, trouvés automatiquement à partir du nom du club (laisser `logo` vide). Il manque `stade-rennais.png` : en attendant, les initiales s'affichent.
Pour un résultat : publier `score` + `classement` en carrousel (Facebook et fil Instagram), en validation (autoPublish false).
Ne jamais remplir une statistique, un buteur ou une ligne de classement sans l'avoir vérifié sur deux sources.
