# Outils de production des visuels

- `visuel.py` : génère un visuel PNG 1080x1350 à partir d'une fiche JSON : `meteo`, `article` (carte blanche avec photo, style principal), `fiche` (carte de carrousel avec gros chiffre, pour la rubrique pratique), `sombre` (infos urgentes). Voir l'en-tête du fichier.
- `chercher_photo.py` et `telecharger_photo.py` : recherche de photos sur Wikimedia Commons et Unsplash, avec auteur et licence.
- `photos/stade-tribunes.jpg` (football), `photos/patinoire.jpg` (hockey, vidéo de la rédaction) et `photos/basket.jpg` (Unsplash) : fonds dégradés des visuels sport, choisis avec le champ `sport` de la fiche.
- `photos/` : photos déjà validées, réutilisables sans crédit sur le visuel (laisser `credit` vide) :
  - `stade-nuit.jpg` : Alex Simpson / Unsplash
  - `stade-raymond-kopa.jpg` : M. Mouchoir / Wikimedia Commons, domaine public
  - `patinage.jpg` : Kelli McClintock / Unsplash
  - `cinema-fantastique.jpg` : illustration originale générée par `outils/cinema.py` (salle de cinéma, film fantastique), libre de droits
  - `ballon-basket.jpg` : illustration originale générée par `outils/ballon.py` (aucun droit tiers), pour le basket quand aucune photo libre n'est disponible

## Visuels Facebook : photo plutôt que bandeau (consigne de la rédaction, 11 novembre 2026)

Sur Facebook, le visuel doit être beau avant tout. Le bandeau de couleur avec un gros chiffre (type `fiche`) est réservé aux sujets dont l'information principale est un chiffre ou une statistique. Pour tous les autres sujets, on met une photo en haut à la place du bandeau (type `article`, ou `sombre` pour un sujet grave).
- En session avec la rédaction : demander d'abord à la rédaction si elle a des photos du sujet, avant de produire le visuel.
- Sans photo de la rédaction (ou en tâche automatique, sans personne à qui demander) : chercher une photo libre et utilisable sans crédit (voir la règle sur les crédits photo) ; si aucune ne convient, publier quand même avec le bandeau.

## Règle du bandeau : une photo par défaut (règle de la rédaction, 12 novembre 2026)

Le haut de chaque visuel (post et story) porte une **photo**, sauf quand le sujet repose sur un chiffre ou une statistique : seulement dans ce cas, le bandeau de couleur avec le gros chiffre (type `fiche`, `story_fiche.py`) est autorisé.
- Post : type `article` (photo en haut) ou `sombre` ; story : `story_points.py` avec la même photo.
- Concert, spectacle, sortie, sport, vie locale : toujours une photo (photo de la rédaction, `outils/photos/`, ou photo libre Unsplash/Pexels/Pixabay/domaine public, jamais de crédit affiché).
- Sans photo libre adaptée : chercher une photo d'ambiance cohérente (instrument, salle, lieu, objet) avant de se rabattre sur le bandeau ; signaler dans le résumé tout visuel publié sans photo.

## Alertes : bon modèle selon le sujet (règle de la rédaction, 13 novembre 2026)

`outils/alerte.py` a deux modèles, choisis avec le champ `modele` de la fiche :
- `"modele": "trafic"` (par défaut, bandes jaunes et noires « chantier ») : **uniquement** pour les problèmes de circulation, accidents de la route, travaux.
- `"modele": "info"` (en-tête « ALERTE INFO » avec point rouge, étiquette et filets rouges, sans bandes) : toutes les autres alertes, notamment les alertes nationales et internationales (catastrophe, attentat, décès, décision majeure, rapport, chiffre national...).
Jamais les bandes de chantier sur un sujet qui n'est pas trafic, accident ou travaux. Un sujet qui repose sur un chiffre (rapport, statistique) peut aussi prendre la carte `fiche` / `story_fiche.py`.
Exemple : `2026-11-13/exemple-alerte-info-post.json`.

## Règle sur les sources (règle générale de la rédaction)

Jamais de source affichée : ni sur un visuel (pas de bloc « SOURCE »), ni dans un texte de post, de story ou d'article (pas de ligne « Source : »).
On ne nomme jamais un média comme source de l'information, et **jamais Angers Info / My Angers**, concurrent direct.
Seules les attributions officielles utiles à l'exactitude restent possibles dans le texte (« selon la préfecture », « indique la mairie »).

## Règle anti-doublon (obligatoire, pour toutes les tâches)

Avant de choisir un sujet, puis de nouveau juste avant le premier createScheduledPost (une autre tâche a pu programmer le même sujet entre-temps), vérifie qu'il n'a pas déjà été traité. Un doublon, c'est le même événement, la même décision, la même exposition, le même match ou la même alerte, quelle que soit la formulation. Vérifie, sur les 15 derniers jours et jusqu'à J+15 :
1. Metricool `getScheduledPosts` (marque 7574505, fuseau Europe/Paris), par tranches d'1 ou 2 jours : posts, stories, X, LinkedIn, publiés, programmés ou en brouillon. Les stories n'ont pas de texte : lis leur `mediaAltText`.
2. Les posts publiés hors Metricool : `getAnalyticsDataByMetrics` avec FBPO02 + FBPO03 (Facebook) et IGPO02 + IGPO03 (Instagram) sur la même période.
3. Ce dépôt : les fiches JSON des dossiers datés des 15 derniers jours (titres et textes des visuels, y compris des stories).
4. Le dépôt privé angersdirect-auto : `veille/sujets.json`, `alertes/vues.json`, `reseaux/traites.json` et `reseaux/a-faire/`, et, après l'ouverture du site (lundi 9 novembre 2026 à 19h), les articles déjà publiés sur angersdirect.fr.
Si le sujet existe déjà : ne publie rien. Exception seulement pour un vrai fait nouveau (bilan officiel, date changée, ouverture effective, résultat après une annonce, rappel « ce soir » d'un événement annoncé plusieurs jours avant), et alors sous un angle nouveau, en le signalant dans le résumé. Un même sujet n'a jamais deux posts Facebook ou deux posts Instagram le même jour. En cas de doute, abstiens-toi et signale-le.

## Règle sur les crédits photo

Règle absolue d'Angers Direct : **jamais de source ni de crédit affiché sur une photo**, quelle que soit son origine (Unsplash, Wikimedia, domaine public, rédaction). Laisser `credit` vide ; les scripts ignorent ce champ de toute façon.
La provenance de la photo est notée seulement dans `sel/credits.json`, jamais sur le visuel. Comme une photo sous CC BY ou CC BY-SA impose un crédit, ne pas utiliser ces photos : préférer Unsplash, Pexels, Pixabay, le domaine public ou les photos de la rédaction.

## Jamais de mention « contenu généré par IA » (règle de la rédaction, 13 novembre 2026)

Ne jamais cocher la mention IA dans Metricool, sur aucun réseau ni format : `isAiGenerated: false` (Instagram, Pinterest), `isAigc: false` (TikTok), `isAiGeneratedContent: false` (YouTube), y compris pour les illustrations.

## Jamais « lien en bio »

Aucun texte de post, de story ou de visuel ne contient « lien en bio » : on écrit « Tous les détails sur angersdirect.fr ».

Les images publiées vont dans un dossier daté (`AAAA-MM-JJ/`). Lien public : `https://raw.githubusercontent.com/angersdirect-a11y/angersdirect-visuels/main/<dossier>/<fichier>.png`.

## Visuels sport (`sport.py`)

Cinq modèles, sur le style des maquettes Angers Direct : `score` (score final avec buteurs et statistiques), `classement` (Ligue 1, ligne d'Angers surlignée), `calendrier` (matchs du mois), `jdm_story` (jour de match 1080x1920) et `jdm_paysage` (jour de match 1920x1080).
Exemples de fiches dans `outils/exemples/`. Champs `sport` (football, hockey, basket) et `competition` (« Ligue 1 » par défaut, « Ligue Magnus », « Nationale 1 ») : `journee` ne contient que la journée (« 8e journée »). Logos des 18 clubs de Ligue 1 dans `outils/logos/<slug>.png`, trouvés automatiquement à partir du nom du club (laisser `logo` vide). Un club sans fichier (promu, coupe) s'affiche avec ses initiales.
Pour un résultat : publier `score` + `classement` en carrousel (Facebook et fil Instagram), en validation (autoPublish false).
Ne jamais remplir une statistique, un buteur ou une ligne de classement sans l'avoir vérifié sur deux sources.

## Stories : toujours en 1080x1920

Instagram et Facebook recadrent une story qui n'est pas au format 9:16 : le haut, le bas et les côtés d'un visuel 1080x1350 sont coupés.

**Règle de la rédaction, pour toutes les stories : une story occupe toute la page.** Le visuel est conçu nativement en 1080x1920 (fond, photo ou graphique jusqu'aux bords, jamais de bandes floutées en haut et en bas), avec le texte utile entre 250 et 1670 px.
- Article avec photo : `outils/story_points.py` (photo en haut, 3 à 5 chiffres ou mots clés, encart).
- Carte sans photo (gros chiffre) : `outils/story_fiche.py`.
- Météo : `outils/visuel.py` avec la même fiche en type `meteo_story`.
- Score : `outils/sport.py` avec la même fiche en type `score_story` ; jour de match : `jdm_story`.
- Alerte : `outils/alerte.py` au format « story » (même `modele` que le post).
- Courbe, carrousel ou cas particulier : un script dédié qui compose la page en 1080x1920 (exemple : `2026-11-09/smic_story.py`).
- `outils/story.py` (visuel 1080x1350 au centre, fond flouté autour) est interdit pour une publication.
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

## Visuels X (`paysage.py`)

`python3 outils/paysage.py fiche.json sortie.png` : visuel 1200x675 (16:9) pour X, photo à gauche, titre sur panneau bleu nuit à droite. Fiche : `photo`, `rubrique`, `titre` (mots entre crochets dans la teinte de la rubrique), `date` et `cadrage` facultatifs. Exemple : `2026-10-29/pepina-x.json`. Instagram, Facebook et LinkedIn gardent le 1080x1350, les stories le 1080x1920.
