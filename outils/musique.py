"""Compose une musique originale entraînante (libre de droits, générée ici) pour les vidéos.

Usage : python3 outils/musique.py duree_secondes sortie.wav [graine]

Pop légère à 112 BPM : grosse caisse, clap, charleston, basse, nappe d'accords et arpège
en pizzicato sur la grille I - V - vi - IV, fondu à la fin. Aucun échantillon externe :
tout est synthétisé, donc aucune question de droits.
"""
import sys, wave
import numpy as np

SR = 44100
BPM = 112
TEMPS = 60 / BPM


def note(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def env(longueur, a=0.005, d=0.25, s=0.0, r=0.05):
    t = np.arange(longueur) / SR
    e = np.where(t < a, t / a, np.maximum(s, np.exp(-(t - a) / d)))
    rel = int(r * SR)
    if rel and longueur > rel:
        e[-rel:] *= np.linspace(1, 0, rel)
    return e


def ajoute(piste, debut, son):
    i = int(debut * SR)
    if i >= len(piste):
        return
    son = son[:len(piste) - i]
    piste[i:i + len(son)] += son


def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)


def clap(rng):
    n = int(0.25 * SR); t = np.arange(n) / SR
    bruit = rng.standard_normal(n)
    # trois petites attaques rapprochées, comme un clap
    e = sum(np.exp(-np.maximum(t - k, 0) * 60) * (t >= k) for k in (0, 0.012, 0.024)) * np.exp(-t * 10)
    b = np.convolve(bruit, np.ones(3) / 3, mode='same') - np.convolve(bruit, np.ones(30) / 30, mode='same')
    return b * e * 0.45


def hat(rng, ouvert=False):
    n = int((0.18 if ouvert else 0.05) * SR)
    b = rng.standard_normal(n)
    b = b - np.convolve(b, np.ones(8) / 8, mode='same')
    return b * env(n, 0.001, 0.06 if ouvert else 0.015) * 0.2


def basse(n_midi, duree):
    n = int(duree * SR); t = np.arange(n) / SR
    f = note(n_midi)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sign(np.sin(2 * np.pi * f * t))
    return s * env(n, 0.005, 0.35, 0.55, 0.04) * 0.5


def nappe(notes, duree):
    n = int(duree * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for m in notes:
        for det in (-0.12, 0.12):
            f = note(m + det)
            ph = (f * t) % 1
            saw = 2 * ph - 1
            s += saw
    # filtre passe-bas simple (moyenne glissante) pour adoucir
    k = 18
    s = np.convolve(s, np.ones(k) / k, mode='same')
    att = np.minimum(1, t / 0.25)
    return s * att * env(n, 0.01, 10, 1, 0.2) * 0.05


def pizz(n_midi, duree=0.3):
    n = int(duree * SR); t = np.arange(n) / SR
    f = note(n_midi)
    s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t) * np.exp(-t * 12) + 0.25 * np.sin(6 * np.pi * f * t) * np.exp(-t * 20)
    return s * env(n, 0.002, 0.16) * 0.22


def compose(duree, graine=7):
    rng = np.random.default_rng(graine)
    L = int((duree + 1) * SR)
    batt, mel = np.zeros(L), np.zeros(L)
    # grille I - V - vi - IV en do majeur (un accord par mesure de 4 temps)
    grille = [(48, [60, 64, 67, 72]), (43, [59, 62, 67, 71]), (45, [57, 60, 64, 69]), (41, [57, 60, 65, 69])]
    arp = [0, 1, 2, 3, 2, 1, 2, 3]
    mesure = 4 * TEMPS
    nb = int(np.ceil(duree / mesure)) + 1
    for m in range(nb):
        t0 = m * mesure
        racine, acc = grille[m % 4]
        intro = m == 0
        ajoute(mel, t0, nappe(acc, mesure))
        for b in range(4):
            tb = t0 + b * TEMPS
            if not intro:
                ajoute(batt, tb, kick())
                if b in (1, 3):
                    ajoute(batt, tb, clap(rng))
            ajoute(batt, tb + TEMPS / 2, hat(rng, ouvert=(b == 3)))
            ajoute(batt, tb, hat(rng) * 0.6)
            if not intro:
                ajoute(mel, tb, basse(racine, TEMPS * 0.48))
                ajoute(mel, tb + TEMPS / 2, basse(racine + (12 if b % 2 else 0), TEMPS * 0.4))
        for i, k in enumerate(arp):
            ajoute(mel, t0 + i * TEMPS / 2, pizz(acc[k] + 12))
    # pompage léger de la musique sur la grosse caisse
    t = np.arange(L) / SR
    phase = (t % TEMPS) / TEMPS
    pompe = 1 - 0.35 * np.exp(-phase * 8) * (t > mesure)
    mix = batt * 0.9 + mel * pompe
    mix = mix[:int(duree * SR)]
    fin = int(1.6 * SR)
    mix[-fin:] *= np.linspace(1, 0, fin) ** 1.5
    mix[:int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
    mix /= np.max(np.abs(mix)) + 1e-9
    mix = np.tanh(mix * 1.4) / np.tanh(1.4) * 0.89
    return mix


def main():
    duree = float(sys.argv[1]); sortie = sys.argv[2]
    graine = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    m = compose(duree, graine)
    st = np.stack([m, np.roll(m, 90) * 0.97], axis=1)  # léger élargissement stéréo
    data = (st * 32767).astype('<i2')
    with wave.open(sortie, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
    print('ok', sortie, duree, 's')


if __name__ == '__main__':
    main()
