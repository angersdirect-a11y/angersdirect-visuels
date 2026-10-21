# Outils de production des visuels

- `visuel.py` : génère un visuel PNG 1080x1350 (météo ou article avec photo) à partir d'une fiche JSON. Voir l'en-tête du fichier.
- `chercher_photo.py` et `telecharger_photo.py` : recherche de photos sur Wikimedia Commons et Unsplash, avec auteur et licence.
- `photos/` : photos déjà validées, réutilisables.
  - `stade-nuit.jpg` : Alex Simpson / Unsplash (« Photo d'illustration : Alex Simpson / Unsplash »)
  - `stade-raymond-kopa.jpg` : M. Mouchoir / Wikimedia Commons, domaine public (« Stade Raymond-Kopa. Photo : M. Mouchoir / Wikimedia Commons »)
  - `patinage.jpg` : Kelli McClintock / Unsplash (« Photo d'illustration : Kelli McClintock / Unsplash »)

Les images publiées vont dans un dossier daté (`AAAA-MM-JJ/`). Lien public : `https://raw.githubusercontent.com/angersdirect-a11y/angersdirect-visuels/main/<dossier>/<fichier>.png`.
