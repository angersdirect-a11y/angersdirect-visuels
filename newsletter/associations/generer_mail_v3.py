# Mail associations : coquille identique au « Brief » (newsletter-modele-defaut.ts), contenu adapté.
import html
SITE="https://angersdirect.fr"
A="/__l5e/assets-v1/"
IMG_ENTETE=SITE+A+"aa903383-7640-483b-9e47-50058fce5cb2/angers-vue-aerienne-cadree.jpg"
LOGO=SITE+A+"6c530f47-7bf1-4333-880c-2d99391318cc/logo-email-lisible.png"
LOGO_PIED=SITE+A+"9abb44e8-6aed-44fb-bcb2-be9a4a7b538a/logo-email-pied.png"
IC={"WhatsApp":A+"0a77b55c-3444-4f2f-822c-0e79e5fb083e/newsletter-icone-whatsapp.png","Enveloppe":A+"4b0fed52-1863-4f44-9bb5-8c6f798eb0db/newsletter-icone-enveloppe.png",
"Instagram":A+"10bdcf31-25c9-4b0e-80b8-92197ed8d730/newsletter-icone-instagram.png","Facebook":A+"1612d740-b0e1-429f-ad71-c496e5afcc4b/newsletter-icone-facebook.png",
"TikTok":A+"32e3cbc8-1ecf-45ec-bec9-c6342d3b812c/newsletter-icone-tiktok.png","X":A+"f4e325b8-915a-419a-9939-c592cf5df382/newsletter-icone-x.png"}
FC="'Barlow Condensed','Arial Narrow',Arial,sans-serif"; FT="Barlow,Arial,sans-serif"
NUIT,BLEU,LIEN,GRIS="#0F1B2D","#1C8FE3","#1665D8","#6B7685"
AG={"fond":"#F4EFE6","framboise":"#D6336C","debut":"#B0204F","fin":"#F0628F"}
VERT=("#3DCB6E","#16834A")
MAIL="associations@angersdirect.fr"
WA=("07 56 93 23 13","https://wa.me/33756932313")
RS=[("Instagram","@angersdirect","https://www.instagram.com/angersdirect/"),("Facebook","Angers Direct","https://www.facebook.com/angersdirect"),
    ("TikTok","@angersdirect","https://www.tiktok.com/@angersdirect"),("X","@angersdirect_","https://x.com/angersdirect_"),
    ("YouTube","Angers Direct","https://www.youtube.com/channel/UC6TexEBeBWaKCb_irMoV90A"),("LinkedIn","Angers Direct","https://www.linkedin.com/company/146675680/")]
e=html.escape
def etiquette(t,c,degrade=None,angle=90,taille=15,pad="7px 14px"):
    t_=max(14,taille); fin=degrade[1] if degrade else c
    fond=f"background-color:{c};background-image:linear-gradient({angle}deg,{degrade[0]},{degrade[1]});" if degrade else f"background-color:{c};"
    h=round(t_*1.2)+2*int(pad.split("px")[0])
    return f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse"><tr><td bgcolor="{c}" style="{fond}padding:{pad};font-family:{FC};font-weight:700;font-size:{t_}px;line-height:{round(t_*1.2)}px;letter-spacing:1.5px;text-transform:uppercase;color:#ffffff;mso-line-height-rule:exactly">{e(t)}</td><!--[if !mso]><!--><td width="12" valign="top" style="width:12px;padding:0;font-size:0;line-height:0"><div style="width:0;height:0;border-top:{h}px solid {fin};border-right:12px solid transparent"></div></td><!--<![endif]--></tr></table>'
SEP='<tr><td style="padding:0 20px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td height="1" style="height:1px;line-height:1px;font-size:0;background:#E3E8EF">&nbsp;</td></tr></table></td></tr>'
def ligne(c,pad="36px 20px"): return f'<tr><td{"" if pad=="0" else " class=\"ad-p\""} style="padding:{pad}">{c}</td></tr>'
def entete(g,d=None): return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td valign="middle">{g}</td>{f"<td align=\"right\" valign=\"middle\" style=\"font-family:{FT};font-size:14px\">{d}</td>" if d else ""}</tr></table>'
P=lambda t,mb="0 0 14px": f'<p style="margin:{mb};font-family:{FT};font-size:16px;line-height:26px;color:#3A4656">{t}</p>'
def badge(t,deg): return etiquette(t,deg[0],degrade=deg,angle=110,taille=14,pad="4px 10px")
def liste(items):
    out=[]
    for i,(rub,deg,titre,txt) in enumerate(items):
        out.append(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-bottom:{"1px solid #E3E8EF" if i<len(items)-1 else "0"}"><tr><td width="42" valign="middle" style="padding:16px 0;font-family:{FC};font-weight:700;font-size:28px;color:{BLEU}">{i+1:02d}</td><td valign="middle" style="padding:16px 12px 16px 0">{badge(rub,deg)}<div style="height:8px;line-height:8px;font-size:0">&nbsp;</div><span style="font-family:{FC};font-weight:700;font-size:20px;line-height:24px;color:{NUIT}">{titre}</span><div style="margin-top:6px;font-family:{FT};font-size:14px;line-height:21px;color:#5A6575">{txt}</div></td></tr></table>')
    return "".join(out)
def bouton(icone,l,h,alt,fond,coul,texte,href):
    return f'<a href="{e(href)}" style="display:block;background:{fond};text-decoration:none;padding:13px 6px;text-align:center;height:26px;line-height:26px"><table role="presentation" cellpadding="0" cellspacing="0" align="center" style="margin:0 auto"><tr><td valign="middle" height="26" style="padding-right:8px;height:26px"><img src="{SITE}{icone}" width="{l}" height="{h}" alt="{e(alt)}" style="display:block;width:{l}px;height:auto;border:0"></td><td valign="middle" style="font-family:{FC};font-weight:700;font-size:15px;line-height:18px;letter-spacing:1px;text-transform:uppercase;color:{coul};white-space:nowrap">{e(texte)}</td></tr></table></a>'

def carte_rs(nom,poignee,href):
    ic=IC.get(nom)
    img=f'<img src="{SITE}{ic}" width="40" height="40" alt="{nom}" style="display:block;width:40px;height:auto;border:0">' if ic else f'<div style="width:40px;height:40px;line-height:40px;border-radius:20px;background:#0F1B2D;color:#ffffff;text-align:center;font-family:{FC};font-weight:700;font-size:{15 if nom=='YouTube' else 17}px">{"▶" if nom=="YouTube" else "in"}</div>'
    return f'<!--[if mso]><td width="170" valign="top"><![endif]--><div class="ad-rs" style="display:inline-block;width:100%;max-width:170px;vertical-align:top;text-align:left"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="padding:0 4px 10px"><a href="{e(href)}" style="display:block;background:#1A2B44;text-decoration:none;padding:12px"><table role="presentation" cellpadding="0" cellspacing="0"><tr><td valign="middle">{img}</td><td valign="middle" style="padding-left:10px"><div style="font-family:{FC};font-weight:700;font-size:16px;line-height:18px;text-transform:uppercase;color:#ffffff">{nom}</div><div style="font-family:{FT};font-size:13px;line-height:18px;color:#B7C3D3">{e(poignee)}</div></td></tr></table></a></td></tr></table></div><!--[if mso]></td><![endif]-->'

def pied():
    icones="".join(f'<td style="padding:0 2px"><a href="{e(h)}" style="display:inline-block;padding:2px 0"><img src="{SITE}{IC[n]}" width="40" height="40" alt="{n}" style="display:block;width:40px;height:auto;border:0"></a></td>' for n,_,h in RS if n in ("Instagram","Facebook","TikTok","X"))
    return f'''<tr><td align="center" style="padding:36px 20px 40px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td class="ad-footer-logo" width="110" valign="middle" align="left"><a href="{SITE}/" style="display:inline-block;padding:4px 0"><img src="{LOGO_PIED}" width="110" height="36" alt="Angers Direct" style="display:block;width:110px;height:36px;border:0"></a></td>
<td class="ad-footer-social" align="right" valign="middle"><table class="ad-footer-reseaux" role="presentation" cellpadding="0" cellspacing="0" align="right"><tr><td style="font-family:{FC};font-weight:600;font-size:13px;line-height:16px;letter-spacing:1.5px;color:{GRIS};padding-right:12px;white-space:nowrap">SUIVEZ-NOUS</td>{icones}</tr></table></td>
</tr><tr><td colspan="2" style="padding:20px 0 16px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td height="1" style="height:1px;font-size:0;line-height:1px;background:#E3E8EF">&nbsp;</td></tr></table></td></tr></table>
<div style="font-family:{FT};font-size:14px;line-height:21px;color:{GRIS}"><a href="{SITE}/" style="color:{LIEN};text-decoration:none">angersdirect.fr</a> · <a href="mailto:{MAIL}" style="color:{GRIS};text-decoration:none">{MAIL}</a><br>Vous recevez ce message car l’adresse de votre association figure dans un annuaire public des associations de votre commune.<br><a href="{{{{ unsubscribe }}}}" style="color:{GRIS};text-decoration:underline;display:inline-block;line-height:44px">Ne plus recevoir nos messages</a></div>
</td></tr>'''



CULT=("#B0204F","#F0628F"); SPORT=VERT; SOL=("#E07A1F","#F2A63A"); VIE=("#1665D8","#3AA3F5")
ESPACE=SITE+"/associations"
def gros_bouton(texte,href,fond=LIEN,coul="#ffffff"):
    return f'<table role="presentation" cellpadding="0" cellspacing="0"><tr><td bgcolor="{fond}" style="background:{fond}"><a href="{e(href)}" style="display:inline-block;padding:15px 26px;font-family:{FC};font-weight:700;font-size:17px;line-height:20px;letter-spacing:1px;text-transform:uppercase;color:{coul};text-decoration:none">{texte}</a></td></tr></table>'

une = f"""{entete(etiquette("À LA UNE",BLEU))}<div style="height:16px"></div>
<h1 style="margin:0 0 14px;font-family:{FC};font-weight:700;font-size:30px;line-height:34px;color:{NUIT}">Votre association a une actu&nbsp;?<br>Angers Direct la&nbsp;relaie.</h1>
{P("Bonjour,")}
{P("Angers Direct raconte chaque jour la vie d’Angers et du Maine-et-Loire, avec une conviction&nbsp;: ce qui nous rassemble compte plus que ce qui nous divise. Et les associations font vivre nos quartiers et nos communes.")}
{P("Nous vous proposons deux choses, gratuitement&nbsp;:","0 0 8px")}
{liste([("Agenda",CULT,"Déposez vos actus","Événements, communiqués, résultats, initiatives : nous les relayons sur le site, l’agenda, la newsletter et nos réseaux."),
("Partage",VIE,"Faites connaître angersdirect.fr à vos adhérents","Pour qu’ils suivent l’actu de leur ville, et celle de votre association.")])}"""

espace = f"""<table role="presentation" class="ad-agenda" width="100%" cellpadding="0" cellspacing="0" bgcolor="{AG["fond"]}" style="background:{AG["fond"]}"><tr><td class="ad-p" style="padding:36px 20px">
{etiquette("NOUVEAU · VOTRE ESPACE EST OUVERT",AG["debut"],degrade=(AG["debut"],AG["fin"]),angle=110)}<div style="height:18px"></div>
<h2 style="margin:0 0 12px;font-family:{FC};font-weight:700;font-size:24px;line-height:28px;color:{NUIT}">Déposez vos actus en quelques minutes</h2>
<p style="margin:0 0 14px;font-family:{FT};font-size:16px;line-height:26px;color:{NUIT}">Sur <strong style="font-weight:500">angersdirect.fr/associations</strong>, un formulaire pas à pas vous guide&nbsp;:</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
{"".join(f'<tr><td width="26" valign="top" style="padding:4px 0;font-family:{FC};font-weight:700;font-size:18px;color:{AG["framboise"]}">✓</td><td style="padding:4px 0;font-family:{FT};font-size:15px;line-height:23px;color:{NUIT}">{t}</td></tr>' for t in ["un événement ou un communiqué, avec une photo (1&nbsp;200&nbsp;px de large minimum, que vous avez le droit de diffuser)&nbsp;;","un clic dans l’e-mail de confirmation, et c’est envoyé&nbsp;;","la rédaction relit, met en forme et publie, gratuitement."])}
</table><div style="height:22px"></div>
{gros_bouton("Déposer une actu&nbsp;→",ESPACE)}
</td></tr></table>"""

contact = f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="{LIEN}" style="background-color:{LIEN};background-image:linear-gradient(110deg,{LIEN},#3AA3F5)"><tr><td style="padding:34px 20px 8px">
<div style="font-family:{FC};font-weight:600;font-size:14px;line-height:18px;letter-spacing:2.5px;text-transform:uppercase;color:#D6E8FF">Vous préférez écrire&nbsp;?</div>
<h2 class="ad-info-titre" style="margin:12px 0;font-family:{FC};font-weight:700;font-size:21px;line-height:1.15;color:#ffffff">Une date, un projet, une réussite à partager&nbsp;?</h2>
<p style="margin:0 0 24px;font-family:{FT};font-size:16px;line-height:26px;color:#EAF3FF">Répondez simplement à ce message, avec votre texte et <strong style="font-weight:500;color:#ffffff">une photo que vous avez le droit de diffuser</strong> (horizontale, avec le nom du photographe).</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td class="ad-contact-cell" width="50%" valign="top" style="padding:0 6px 12px 0">{bouton(IC["WhatsApp"],26,26,"WhatsApp","#ffffff",NUIT,WA[0],WA[1])}</td><td class="ad-contact-cell" width="50%" valign="top" style="padding:0 0 12px 6px">{bouton(IC["Enveloppe"],26,18,"E-mail",NUIT,"#ffffff","Écrire à la rédaction",f"mailto:{MAIL}")}</td></tr></table>
<p style="margin:8px 0 0;font-family:{FT};font-size:14px;line-height:20px;color:#D6E8FF">Chaque information est relue par la rédaction avant publication.</p>
</td></tr><!--[if !mso]><!--><tr><td align="right" style="padding:0;font-size:0;line-height:0"><div style="width:0;height:0;border-bottom:30px solid #ffffff;border-left:30px solid transparent"></div></td></tr><!--<![endif]--><!--[if mso]><tr><td style="padding:0 0 22px;font-size:0;line-height:0">&nbsp;</td></tr><![endif]--></table>"""

MSG_ADH = ("Bonjour à toutes et à tous,\n\nAngers Direct (angersdirect.fr) relaie la vie des associations d’Angers et du Maine-et-Loire, dont la nôtre : "
"vous pourrez y retrouver nos événements et nos actualités, aux côtés de l’actu locale, du sport, de la culture, des sorties et des infos pratiques.\n\n"
"Pour suivre l’actu :\n- le site : angersdirect.fr\n- la newsletter gratuite du samedi matin, à recevoir via le site\n"
"- Instagram, TikTok et Facebook : @angersdirect\n\nBonne lecture !")
import urllib.parse
MAILTO_ADH = "mailto:?subject=" + urllib.parse.quote("Retrouvez nos actus sur Angers Direct") + "&body=" + urllib.parse.quote(MSG_ADH)
partage = f"""{entete(etiquette("FAITES CONNAÎTRE ANGERS DIRECT",BLEU))}<div style="height:16px"></div>
{P("Plus vos adhérents suivent Angers Direct, plus vos actus touchent de monde. Glissez ce message dans votre prochaine newsletter&nbsp;:","0 0 16px")}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#EEF2F6" style="background:#EEF2F6;border-left:4px solid {BLEU}"><tr><td style="padding:18px 18px 16px">
<div style="font-family:{FC};font-weight:600;font-size:14px;letter-spacing:2px;text-transform:uppercase;color:{GRIS};margin-bottom:10px">Message prêt à transmettre</div>
<div style="font-family:{FT};font-size:15px;line-height:24px;color:{NUIT}">{e(MSG_ADH).replace(chr(10),"<br>")}</div>
</td></tr></table>
<a href="{e(MAILTO_ADH)}" style="font-family:{FC};font-weight:700;font-size:15px;line-height:20px;color:{LIEN};letter-spacing:1px;text-decoration:none;display:inline-block;padding:14px 0 0">TRANSMETTRE CE MESSAGE À NOS ADHÉRENTS&nbsp;→</a>
<p style="margin:14px 0 0;font-family:{FT};font-size:14px;line-height:21px;color:{GRIS}">Un visuel à partager sur vos réseaux, en format publication et story, vous attend sur <a href="{ESPACE}" style="color:{LIEN}">angersdirect.fr/associations</a>.</p>"""

reseaux = f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="{NUIT}" style="background:{NUIT}"><tr><td style="padding:26px 12px 14px">
<div style="padding:0 4px">{etiquette("SUIVEZ ANGERS DIRECT",VERT[0],degrade=VERT)}</div><div style="height:18px"></div>
<div style="font-size:0;text-align:center"><!--[if mso]><table role="presentation" width="528" cellpadding="0" cellspacing="0"><tr><![endif]-->{"".join(carte_rs(*r) for r in RS[:3])}<!--[if mso]></tr><tr><![endif]-->{"".join(carte_rs(*r) for r in RS[3:])}<!--[if mso]></tr></table><![endif]--></div>
</td></tr></table>"""

bientot = f"""<p style="margin:0;font-family:{FT};font-size:16px;line-height:26px;color:{NUIT}">À très bientôt,<br><strong style="font-weight:500">La rédaction d’Angers Direct</strong></p>"""

corps="".join((SEP if i else "")+ligne(h,"0" if h.startswith("<table role=\"presentation\" class=\"ad-agenda\"") or h.startswith("<table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" bgcolor=\"#0F1B2D\"") else "36px 20px") for i,h in enumerate([une,espace,contact,partage,reseaux,bientot]))
TITRE="SPÉCIAL ASSOCIATIONS"
doc=f'''<!doctype html><html lang="fr" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting"><meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark"><title>{TITRE}</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500&display=swap" rel="stylesheet">
<!--[if mso]><style>table,td,div,p{{font-family:Arial,sans-serif!important}}h1,h2,a{{font-family:"Arial Narrow",Arial,sans-serif!important}}</style><![endif]-->
<style>@media (min-width:600px){{.ad-info-titre{{white-space:nowrap}}.ad-p{{padding-left:44px!important;padding-right:44px!important}}}}
@media (max-width:599px){{.ad-footer-logo,.ad-footer-social{{display:block!important;width:100%!important;text-align:center!important}}.ad-footer-social{{padding-top:12px!important}}.ad-footer-reseaux{{float:none!important;margin:0 auto!important}}.ad-p{{padding-left:20px!important;padding-right:20px!important}}.ad-rs{{max-width:50%!important}}}}
@media (max-width:479px){{.ad-contact-cell{{display:block!important;width:100%!important;padding:0 0 12px!important}}.ad-rs{{max-width:100%!important}}}}
@media (prefers-color-scheme:dark){{.ad-c{{background:#ffffff!important;color:#0F1B2D!important}}}}[data-ogsc] .ad-c{{background:#ffffff!important;color:#0F1B2D!important}}</style></head>
<body style="margin:0;padding:0;background:#ffffff;font-family:{FT};color:{NUIT}">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all">Votre espace est ouvert : déposez vos actus en quelques minutes, nous les relayons gratuitement.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#EEF2F6" style="background:#EEF2F6"><tr><td align="center">
<!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0"><tr><td><![endif]--><table role="presentation" class="ad-c" width="100%" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="width:100%;max-width:600px;background:#ffffff;table-layout:fixed">
<tr><td style="padding:26px 20px">{entete(f'<a href="{SITE}/"><img src="{LOGO}" width="110" height="46" alt="Angers Direct" style="display:block;width:110px;height:auto;border:0"></a>', f'<span style="color:{GRIS};font-size:14px;line-height:20px">Angers et Maine-et-Loire</span><br><span style="color:{NUIT};font-weight:500;font-size:14px">Associations</span>')}</td></tr>
<tr><td background="{IMG_ENTETE}" bgcolor="{NUIT}" height="190" valign="middle" style="background-color:{NUIT};background-image:url('{IMG_ENTETE}');background-size:cover;background-position:center;height:190px">
<!--[if gte mso 9]><v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px;height:190px"><v:fill type="frame" src="{IMG_ENTETE}" color="{NUIT}"/><v:textbox inset="0,0,0,0"><![endif]-->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td height="190" valign="middle" style="height:190px;padding:0 20px;background-color:transparent;background-image:linear-gradient(90deg,rgba(15,27,45,0.92) 0%,rgba(15,27,45,0.7) 50%,rgba(15,27,45,0.1) 100%)">
{etiquette(TITRE,BLEU,degrade=("#1665D8",BLEU),taille=24,pad="8px 16px")}
<div style="margin-top:16px;font-family:{FT};font-size:15px;color:#ffffff">L’actualité d’Angers et du Maine-et-Loire, au plus près de chez vous.</div>
</td></tr></table>
<!--[if gte mso 9]></v:textbox></v:rect><![endif]--></td></tr>
{corps}
{SEP}
{pied()}
</table><!--[if mso]></td></tr></table><![endif]--></td></tr></table></body></html>'''
doc=doc.replace("’","&rsquo;")
open("/home/claude/assos/mail-associations-v3.html","w").write(doc)
print(len(doc))
