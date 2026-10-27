# Outils de production des visuels

- `visuel.py` : génère un visuel PNG 1080x1350 à partir d'une fiche JSON : `meteo`, `article` (carte blanche avec photo, style principal), `fiche` (carte de carrousel avec gros chiffre, pour la rubrique pratique), `sombre` (infos urgentes). Voir l'en-tête du fichier.
- `chercher_photo.py` et `telecharger_photo.py` : recherche de photos sur Wikimedia Commons et Unsplash, avec auteur et licence.
- `photos/stade-tribunes.jpg` (football), `photos/patinoire.jpg` (hockey, vidéo de la rédaction) et `photos/basket.jpg` (Unsplash) : fonds dégradés des visuels sport, choisis avec le champ `sport` de la fiche.
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
Exemples de fiches dans `outils/exemples/`. Champs `sport` (football, hockey, basket) et `competition` (« Ligue 1 » par défaut, « Ligue Magnus », « Nationale 1 ») : `journee` ne contient que la journée (« 8e journée »). Logos des 18 clubs de Ligue 1 dans `outils/logos/<slug>.png`, trouvés automatiquement à partir du nom du club (laisser `logo` vide). Un club sans fichier (promu, coupe) s'affiche avec ses initiales.
Pour un résultat : publier `score` + `classement` en carrousel (Facebook et fil Instagram), en validation (autoPublish false).
Ne jamais remplir une statistique, un buteur ou une ligne de classement sans l'avoir vérifié sur deux sources.

## Stories : toujours en 1080x1920

Instagram et Facebook recadrent une story qui n'est pas au format 9:16 : le haut, le bas et les côtés d'un visuel 1080x1350 sont coupés.
Avant toute story, passer le visuel par `python3 outils/story.py visuel.png visuel-story.png` (le visuel entier au centre, fond flouté autour).
Un post Facebook et une story Instagram ne peuvent donc pas partager le même média : programmer deux publications séparées (Facebook POST avec le 1080x1350, story avec la version 1080x1920).

## Calendriers officiels

- Angers SCO (Ligue 1) : ligue1.com, angers-sco.fr ; deuxième source L'Équipe ou FotMob.
- Ducs d'Angers (Ligue Magnus, hockey) : lesducsdangers.fr, hockeyfrance.com ; deuxième source planetehockey.com ou Sofascore.
- Étoile Angers Basket, « l'EAB » (Nationale 1) : nm1.ffbb.com (fiche équipe 33-angers), etoile-angers-basket.com.
- Angers SCO Handball (Nationale 1 masculine, poule Fédérale) : handball.angers-sco.fr, ffhandball.fr ou scorenco.com.
Logos : `logos/ducs-angers.png`, `logos/eab.png`, `logos/sco-handball.png`, `logos/les-sables-basket.png`, `logos/chamonix-pionniers.png`, `logos/nice-aigles.png`, et les 12 clubs de Ligue Magnus 2026-27 (amiens-gothiques, anglet-hormadi, bordeaux-boxers, briancon-diables-rouges, cergy-jokers, gap-rapaces, grenoble-bruleurs-de-loups, marseille-spartiates), trouvés automatiquement selon le champ `sport` de la fiche. Les adversaires hors Ligue 1 s'affichent avec leurs initiales tant que leur logo n'est pas ajouté.

## Vidéos TikTok (`video.py`)

`python3 outils/video.py fiche.json sortie.mp4` : vidéo verticale 1080x1920 dans le style de la vidéo de présentation Angers Direct (photos plein cadre avec léger zoom, logo blanc en haut à gauche, étiquette de rubrique puis titre qui monte, fondus enchaînés). Voir l'en-tête du fichier pour la fiche.
Chaque vidéo se termine automatiquement par la carte de fin : bandes de couleur animées, logo, « Le média d'Angers et de sa région », « Suivez-nous » avec Instagram, Facebook, TikTok, YouTube et LinkedIn, @angersdirect et angersdirect.fr.
Les photos doivent être assez grandes pour du plein cadre 9:16 (au moins 1080 px de haut sur la partie gardée) ; une affiche paysage trop petite rend flou. Musique : `musique.py` compose une boucle pop originale (synthétisée, sans échantillon, donc libre de droits), ajoutée automatiquement ; `"musique": false` dans la fiche pour une vidéo muette.

Modèle de fiche vidéo : `outils/exemples/video.json` (scène d'accroche sans rubrique, scènes photo avec rubrique, scène « texte » sans photo, mode « haut » pour une image peu haute). Copier la fiche dans le dossier daté, remplacer textes et photos, puis lancer `video.py`. Accroche en question ou chiffre, 4 à 6 scènes de 3,2 s, une idée par scène, titres de 6 mots maximum si possible ; la carte de fin est ajoutée automatiquement.

## Story « points clés » (`story_points.py`)

`python3 outils/story_points.py fiche.json story.png` (lancer depuis la racine du dépôt) : story 1080x1920 native avec photo en haut, titre, 3 à 5 chiffres clés et un encart final. Exemple : `2026-10-27/mobilisation-lyceenne-story.json`.
