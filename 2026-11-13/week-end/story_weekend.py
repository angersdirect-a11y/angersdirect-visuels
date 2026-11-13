"""Story 1080x1920 du carrousel week-end : story_fiche.py avec un gros chiffre réduit (150 px) pour que « CE WEEK-END » tienne sur une ligne.
Usage (depuis la racine du dépôt) : python3 2026-11-13/week-end/story_weekend.py 2026-11-13/week-end/carte-1-story.json 2026-11-13/week-end/carte-1-story.png
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'outils'))
import story_fiche
_corps = story_fiche.corps
story_fiche.corps = lambda f: _corps(f).replace('font-size:200px;line-height:1', 'font-size:150px;line-height:1;white-space:nowrap').replace('top:360px', 'top:385px')
story_fiche.main()
