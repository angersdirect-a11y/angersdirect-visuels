# Le Brief de la semaine : même coquille que le modèle du site (newsletter-modele-defaut.ts).
# Photos en JPEG/PNG hébergées sur ce dépôt public (lisibles par Outlook, contrairement au WebP).
import sys, html
src = open(__file__.replace("brief/generer_brief.py", "associations/generer_mail_v3.py")).read()
exec(src.split("CULT=(")[0])  # charte : couleurs, polices, étiquettes, boutons, icônes

DATE = sys.argv[1] if len(sys.argv) > 1 else "2026-11-21"
RAW = f"https://raw.githubusercontent.com/angersdirect-a11y/angersdirect-visuels/main/newsletter/brief/{DATE}/"
VIOLET = ("#6A3FC9", "#9B6BF2"); ECO = ("#C27A12", "#E3A33B"); VILLE = ("#0E8C8C", "#2BB5A8")
CULT = ("#B0204F", "#F0628F")
def lien(t, href, c=LIEN):
    return f'<a href="{e(href)}" style="font-family:{FC};font-weight:700;font-size:15px;line-height:20px;letter-spacing:1px;text-transform:uppercase;color:{c};text-decoration:none">{t}&nbsp;→</a>'
def lien_droite(t, href, c=LIEN):
    return f'<a href="{e(href)}" style="font-family:{FT};font-size:14px;color:{c};text-decoration:none">{t}&nbsp;→</a>'
def rub(t, c):
    return f'<div style="font-family:{FC};font-weight:700;font-size:13px;line-height:16px;letter-spacing:1.5px;text-transform:uppercase;color:{c}">{t}</div>'

# ---------- Contenu de la semaine ----------
UNE = dict(rub="Économie", deg=ECO, img="une-eclim.jpg",
    url=SITE+"/economie/eclim-angers-reprise-salaries-scop-ventilation",
    titre="À Angers, les salariés d’Eclim reprennent leur entreprise en Scop",
    texte="Pour assurer la succession de son fondateur, 20 des 25 salariés de la PME angevine de ventilation ont racheté l’entreprise fin octobre, en réunissant 270&nbsp;000&nbsp;euros. Chacun y a désormais une voix.")
ESSENTIEL = [
    ("Ville", VILLE[0], "Cité scolaire David d’Angers : 864&nbsp;758&nbsp;€ du Département",
     "Rénovation thermique de quinze bâtiments : travaux fin 2027, livraison à la rentrée 2029.",
     "th-cite-scolaire.jpg", SITE+"/ville/renovation-cite-scolaire-david-angers-departement-864-758-euros"),
    ("Société", VIOLET[0], "Violences sexuelles : les plaintes ont doublé en cinq ans",
     "454 plaintes à Angers en 2025. Un débat ouvert à tous est organisé lundi à 19h.",
     "th-violences.jpg", SITE+"/societe/violences-sexuelles-angers-plaintes-doublent-debat-angers-cooperative"),
    ("Ville", VILLE[0], "La résidence Corbeille d’Argent inaugurée après rénovation",
     "La résidence autonomie du CCAS compte désormais 61 logements, contre 58 auparavant.",
     "th-corbeille.jpg", SITE+"/ville/inauguration-residence-autonomie-corbeille-argent-angers"),
    ("Société", VIOLET[0], "Inflation : +3,4&nbsp;% sur un an en octobre",
     "L’énergie tire les prix vers le haut en France.",
     "th-inflation.jpg", SITE+"/societe/inflation-france-octobre-2026-insee"),
]
SPORT = dict(sport="Hockey · Ligue Magnus", club="Ducs d’Angers", logo="logo-ducs-angers.png",
    club_url=SITE+"/sport/hockey",
    dernier="Ven. 20 nov. · 16e journée", dom=("Ducs d’Angers","logo-ducs-angers.png"), score="4 - 0",
    ext=("Marseille","logo-marseille-spartiates.png"),
    prochain="Mar. 24 nov. 20h30 · Coupe de France", p_dom=("Ducs d’Angers","logo-ducs-angers.png"),
    p_ext=("Amiens","logo-amiens-gothiques.png"))
SORTIR = [("25","NOV.","sortir-soleils-hiver.jpg","Soleils d’Hiver : c’est parti","Centre-ville · jusqu’au 3 janvier",
           SITE+"/ville/soleils-hiver-angers-2026-programme"),
          ("27","NOV.","sortir-agirc-arrco.jpg","Rencontres retraite Agirc-Arrco","Entretiens gratuits · jusqu’au 27 nov.",
           SITE+"/societe/rencontres-retraite-agirc-arrco-entretiens-gratuits-2")]
METEO = "☁️&nbsp; 9&nbsp;°C à Angers · nuageux, max 13&nbsp;°C"
DATE_TXT, EDITION = "Samedi 21 novembre 2026", "Édition n°&nbsp;1"
PREHEADER = "Eclim reprise par ses salariés, les Ducs en série, Soleils d’Hiver arrive : l’essentiel de la semaine."

# ---------- Blocs ----------
une = f"""{entete(etiquette("À LA UNE",BLEU,degrade=("#1665D8",BLEU),angle=110))}<div style="height:18px;line-height:18px;font-size:0">&nbsp;</div>
<a href="{UNE['url']}"><img src="{RAW}{UNE['img']}" width="512" alt="" style="display:block;width:100%;max-width:512px;height:auto;border:0"></a>
<div style="margin-top:-14px">{badge(UNE['rub'],UNE['deg'])}</div>
<h1 style="margin:16px 0 12px;font-family:{FC};font-weight:600;font-size:30px;line-height:34px;color:{NUIT}"><a href="{UNE['url']}" style="color:{NUIT};text-decoration:none">{UNE['titre']}</a></h1>
{P(UNE['texte'],"0 0 18px")}{lien("Lire l’article",UNE['url'])}"""

def item(i, r):
    rb, c, titre, txt, img, url = r
    bord = "1px solid #E3E8EF" if i < len(ESSENTIEL)-1 else "0"
    return f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-bottom:{bord}"><tr>
<td width="42" valign="middle" style="padding:20px 0;font-family:{FC};font-weight:700;font-size:28px;color:{BLEU}">{i+1:02d}</td>
<td valign="middle" style="padding:20px 14px 20px 0">{rub(rb,c)}<a href="{url}" style="text-decoration:none"><div style="margin-top:4px;font-family:{FC};font-weight:600;font-size:19px;line-height:23px;color:{NUIT}">{titre}</div></a><div style="margin-top:6px;font-family:{FT};font-size:14px;line-height:21px;color:#5A6575">{txt}</div></td>
<td width="120" valign="middle" style="padding:20px 0"><a href="{url}"><img src="{RAW}{img}" width="120" height="90" alt="" style="display:block;width:120px;height:90px;border:0"></a></td></tr></table>'''
essentiel = f"""{entete(etiquette("L’ESSENTIEL",BLEU,degrade=("#1665D8",BLEU),angle=110), lien_droite("Toute l’actu",SITE+"/actu"))}<div style="height:6px"></div>
{"".join(item(i,r) for i,r in enumerate(ESSENTIEL))}"""

def equipe(nom, logo, droite=False):
    img = f'<img src="{RAW}{logo}" width="40" alt="" style="display:block;width:40px;height:auto;border:0">'
    txt = f'<span style="font-family:{FC};font-weight:700;font-size:16px;line-height:18px;text-transform:uppercase;color:#ffffff">{nom}</span>'
    cells = f'<td valign="middle" style="padding:0 8px">{txt}</td><td valign="middle">{img}</td>' if droite else f'<td valign="middle">{img}</td><td valign="middle" style="padding:0 8px">{txt}</td>'
    return f'<table role="presentation" cellpadding="0" cellspacing="0" align="{"right" if droite else "left"}"><tr>{cells}</tr></table>'
def match(titre, dom, centre, ext):
    return f'''<div style="font-family:{FC};font-weight:600;font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:#B7C3D3;text-align:center;padding:16px 8px 12px">{titre}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td width="40%" valign="middle">{equipe(*dom)}</td>
<td width="20%" align="center" valign="middle" style="font-family:{FC};font-weight:700;font-size:28px;color:#ffffff;white-space:nowrap">{centre}</td>
<td width="40%" valign="middle">{equipe(*ext, droite=True)}</td></tr></table>'''
S = SPORT
sport = f"""{entete(etiquette("SPORT",VERT[0],degrade=VERT,angle=110), lien_droite("Résultats et classements",SITE+"/sport","#16834A"))}<div style="height:18px"></div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="{NUIT}" style="background:{NUIT}"><tr><td style="padding:18px 16px 16px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td width="56" valign="middle"><img src="{RAW}{S['logo']}" width="48" alt="" style="display:block;width:48px;height:auto;border:0"></td>
<td valign="middle" style="padding-left:8px"><div style="font-family:{FC};font-weight:600;font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:#B7C3D3">{S['sport']}</div><div style="font-family:{FC};font-weight:700;font-size:21px;text-transform:uppercase;color:#ffffff">{S['club']}</div></td>
<td align="right" valign="middle">{etiquette("Voir le club","#D9381E",degrade=("#D9381E","#F05A2B"),angle=110,taille=14,pad="6px 12px").replace('<table role="presentation"','<a href="'+S['club_url']+'" style="text-decoration:none"><table role="presentation" align="right"',1).replace('</tr></table>','</tr></table></a>',1)}</td></tr></table>
<div style="height:14px"></div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#1A2B44" style="background:#1A2B44"><tr><td style="padding:0 14px 18px">
{match("Dernier match · "+S['dernier'], S['dom'], S['score'], S['ext'])}
<div style="height:1px;background:#2C4060;margin:18px 0 0;line-height:1px;font-size:0">&nbsp;</div>
{match("Prochain match · "+S['prochain'], S['p_dom'], "VS", S['p_ext'])}
</td></tr></table></td></tr></table>"""

def carte_sortie(j, m, img, titre, lieu, url):
    return f'''<!--[if mso]><td width="250" valign="top"><![endif]--><div class="ad-rs" style="display:inline-block;width:100%;max-width:256px;vertical-align:top;text-align:left"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="padding:0 6px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="background:#ffffff"><tr><td style="position:relative">
<a href="{url}"><img src="{RAW}{img}" width="244" alt="" style="display:block;width:100%;height:auto;border:0"></a></td></tr>
<tr><td style="padding:14px 14px 16px"><table role="presentation" cellpadding="0" cellspacing="0" style="margin-bottom:8px"><tr><td bgcolor="{AG['debut']}" style="background:{AG['debut']};padding:4px 9px;font-family:{FC};font-weight:700;font-size:15px;line-height:17px;color:#ffffff;text-align:center">{j} <span style="font-size:12px">{m}</span></td></tr></table>
<a href="{url}" style="text-decoration:none"><div style="font-family:{FC};font-weight:600;font-size:19px;line-height:23px;color:{NUIT}">{titre}</div></a>
<div style="margin-top:4px;font-family:{FT};font-size:14px;line-height:20px;color:{GRIS}">{lieu}</div></td></tr></table>
</td></tr></table></div><!--[if mso]></td><![endif]-->'''
sortir = f"""<table role="presentation" class="ad-agenda" width="100%" cellpadding="0" cellspacing="0" bgcolor="{AG['fond']}" style="background:{AG['fond']}"><tr><td class="ad-p" style="padding:36px 20px 24px">
{entete(etiquette("SORTIR CETTE SEMAINE",AG['debut'],degrade=(AG['debut'],AG['fin']),angle=110), f'<a href="{SITE}/agenda" style="font-family:{FC};font-weight:700;font-size:14px;letter-spacing:1px;color:{AG["framboise"]};text-decoration:none">TOUT L’AGENDA&nbsp;→</a>')}<div style="height:18px"></div>
<div style="font-size:0;margin:0 -6px"><!--[if mso]><table role="presentation" width="512" cellpadding="0" cellspacing="0"><tr><![endif]-->{"".join(carte_sortie(*c) for c in SORTIR)}<!--[if mso]></tr></table><![endif]--></div>
</td></tr></table>"""

info = f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="{LIEN}" style="background-color:{LIEN};background-image:linear-gradient(110deg,{LIEN},#3AA3F5)"><tr><td style="padding:34px 26px 8px">
<div style="font-family:{FC};font-weight:600;font-size:14px;line-height:18px;letter-spacing:2.5px;text-transform:uppercase;color:#D6E8FF">Votre info compte</div>
<h2 style="margin:12px 0;font-family:{FC};font-weight:700;font-size:22px;line-height:1.15;color:#ffffff">Vous avez vu, vécu ou appris quelque chose à Angers&nbsp;?</h2>
<p style="margin:0 0 24px;font-family:{FT};font-size:16px;line-height:26px;color:#EAF3FF">Un accident, un commerce qui ouvre, un souci dans votre quartier, une belle initiative : envoyez-nous votre info, vos photos ou vos vidéos.</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td class="ad-contact-cell" width="50%" valign="top" style="padding:0 6px 12px 0">{bouton(IC["WhatsApp"],26,26,"WhatsApp","#ffffff",NUIT,WA[0],WA[1])}</td><td class="ad-contact-cell" width="50%" valign="top" style="padding:0 0 12px 6px">{bouton(IC["Enveloppe"],26,18,"E-mail",NUIT,"#ffffff","Écrire à la rédaction","mailto:redaction@angersdirect.fr")}</td></tr></table>
<p style="margin:8px 0 0;font-family:{FT};font-size:14px;line-height:20px;color:#D6E8FF">Chaque info est vérifiée. Votre nom n’est jamais publié sans votre accord.</p>
</td></tr><!--[if !mso]><!--><tr><td align="right" style="padding:0;font-size:0;line-height:0"><div style="width:0;height:0;border-bottom:30px solid #ffffff;border-left:30px solid transparent"></div></td></tr><!--<![endif]--><!--[if mso]><tr><td style="padding:0 0 22px;font-size:0;line-height:0">&nbsp;</td></tr><![endif]--></table>"""

pied_brief = pied().replace("associations@angersdirect.fr", "redaction@angersdirect.fr").replace(
    "Vous recevez ce message car l’adresse de votre association figure dans un annuaire public des associations de votre commune.",
    "Vous recevez ce brief car vous vous êtes inscrit sur angersdirect.fr.").replace("Ne plus recevoir nos messages", "Se désinscrire")

PLEIN = ("<table role=\"presentation\" class=\"ad-agenda\"",)
blocs = [une, essentiel, sport, sortir, info]
corps = ""
for i, h in enumerate(blocs):
    plein = h.startswith(PLEIN)
    if i and not plein and not blocs[i-1].startswith(PLEIN): corps += SEP
    corps += ligne(h, "0" if plein else ("36px 20px" if h is not info else "36px 20px 0"))

TITRE = "LE BRIEF DE LA SEMAINE"
doc = f'''<!doctype html><html lang="fr" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting"><meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark"><title>Le Brief de la semaine</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500&display=swap" rel="stylesheet">
<!--[if mso]><style>table,td,div,p{{font-family:Arial,sans-serif!important}}h1,h2,a{{font-family:"Arial Narrow",Arial,sans-serif!important}}</style><![endif]-->
<style>@media (min-width:600px){{.ad-info-titre{{white-space:nowrap}}.ad-p{{padding-left:44px!important;padding-right:44px!important}}}}
@media (max-width:599px){{.ad-footer-logo,.ad-footer-social{{display:block!important;width:100%!important;text-align:center!important}}.ad-footer-social{{padding-top:12px!important}}.ad-footer-reseaux{{float:none!important;margin:0 auto!important}}.ad-p{{padding-left:20px!important;padding-right:20px!important}}}}
@media (max-width:479px){{.ad-contact-cell{{display:block!important;width:100%!important;padding:0 0 12px!important}}.ad-rs{{max-width:100%!important}}}}
@media (prefers-color-scheme:dark){{.ad-c{{background:#ffffff!important;color:#0F1B2D!important}}}}[data-ogsc] .ad-c{{background:#ffffff!important;color:#0F1B2D!important}}</style></head>
<body style="margin:0;padding:0;background:#ffffff;font-family:{FT};color:{NUIT}">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all">{PREHEADER}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#EEF2F6" style="background:#EEF2F6"><tr><td align="center">
<!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0"><tr><td><![endif]--><table role="presentation" class="ad-c" width="100%" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="width:100%;max-width:600px;background:#ffffff;table-layout:fixed">
<tr><td class="ad-p" style="padding:26px 20px">{entete(f'<a href="{SITE}/"><img src="{LOGO}" width="110" height="46" alt="Angers Direct" style="display:block;width:110px;height:auto;border:0"></a>', f'<span style="color:{GRIS};font-size:14px;line-height:20px">{DATE_TXT}</span><br><span style="color:{NUIT};font-weight:500;font-size:14px">{EDITION}</span>')}</td></tr>
<tr><td background="{IMG_ENTETE}" bgcolor="{NUIT}" height="190" valign="middle" style="background-color:{NUIT};background-image:url('{IMG_ENTETE}');background-size:cover;background-position:center;height:190px">
<!--[if gte mso 9]><v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px;height:190px"><v:fill type="frame" src="{IMG_ENTETE}" color="{NUIT}"/><v:textbox inset="0,0,0,0"><![endif]-->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td class="ad-p" height="190" valign="middle" style="height:190px;padding:0 20px;background-color:transparent;background-image:linear-gradient(90deg,rgba(15,27,45,0.92) 0%,rgba(15,27,45,0.7) 50%,rgba(15,27,45,0.1) 100%)">
{etiquette(TITRE,BLEU,degrade=("#1665D8",BLEU),taille=24,pad="8px 16px")}
<div style="margin-top:16px;font-family:{FT};font-size:15px;color:#ffffff">{METEO}</div>
</td></tr></table>
<!--[if gte mso 9]></v:textbox></v:rect><![endif]--></td></tr>
{corps}
{SEP}
{pied_brief}
</table><!--[if mso]></td></tr></table><![endif]--></td></tr></table></body></html>'''
doc = doc.replace("’", "&rsquo;")
out = f"/home/claude/angersdirect-visuels/newsletter/brief/{DATE}/brief-{DATE}.html"
open(out, "w").write(doc)
print(out, len(doc))
