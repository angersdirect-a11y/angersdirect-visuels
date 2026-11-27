"""Garde-fou de la charte graphique Angers Direct.

Règle de Valentin (27/11/2026) : un visuel ne sort jamais avec une police de remplacement.
Si les polices Barlow / Barlow Condensed ne sont pas installées, le générateur s'arrête
au lieu de produire un visuel hors charte (police à empattements par défaut).
Réparer : cd outils && npm i --silent
"""
import pathlib, sys

POLICES = [('barlow', [400, 500, 600]), ('barlow-condensed', [600, 700])]


def verifier_polices(fonts: pathlib.Path):
    manquantes = [f"{d}-{w}" for d, ws in POLICES for w in ws
                  if not (fonts / d / 'files' / f'{d}-latin-{w}-normal.woff2').is_file()]
    if manquantes:
        sys.exit("CHARTE NON RESPECTÉE : polices absentes (" + ", ".join(manquantes) + "). "
                 "Aucun visuel produit. Installer : cd outils && npm i --silent")
