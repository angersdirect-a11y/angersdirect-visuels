import { createFileRoute } from "@tanstack/react-router";
import { ARTICLES } from "@/lib/site";
import { ArticleCard, Container } from "@/components/site/ui";
import { meta } from "@/components/site/Page";

/** Page Vidéos : vignettes des derniers reportages + comptes Instagram, TikTok et Facebook.
 *  Simples liens et images légères (webp 540x960, chargement différé) : aucun script tiers, aucun cookie. */
const IMG = "https://raw.githubusercontent.com/angersdirect-a11y/angersdirect-visuels/main/site/videos";
const TIKTOK = "https://www.tiktok.com/@angersdirect";
const INSTAGRAM = "https://www.instagram.com/angersdirect/";
const FACEBOOK = "https://www.facebook.com/angersdirect";

const VIDEOS = [
  { img: "manif-musique", titre: "Manifestation à Angers : l'après-midi commence en musique" },
  { img: "manif-place-leclerc", titre: "14h, place Leclerc : la manifestation démarre en musique" },
  { img: "manif-voies-berges", titre: "15h30 : le cortège s'engage sur les voies sur berges" },
  { img: "manif-cale-savatte", titre: "Cale de la Savatte, les gendarmes repoussent les manifestants" },
  { img: "manif-rue-beaurepaire", titre: "Rue Beaurepaire, les forces de l'ordre bloquent l'accès" },
  { img: "salon-du-cheval", titre: "Salon du Cheval : dernier jour" },
];

const RESEAUX = [
  {
    nom: "Instagram", compte: "@angersdirect", url: INSTAGRAM, site: "instagram.com", photo: "carte-instagram", sigle: "IG", action: "S'abonner",
    titre: "Nos Reels au cœur de l'actu angevine",
    texte: "Manifestations, matchs, sorties : la rédaction filme Angers au plus près.",
    pastille: { background: "linear-gradient(135deg,#F58529,#DD2A7B 55%,#8134AF)" },
    etiquette: { background: "linear-gradient(90deg,#DD2A7B,#8134AF)" },
    couleur: "#DD2A7B", remplissage: "linear-gradient(90deg,#F58529,#DD2A7B 60%,#8134AF)",
  },
  {
    nom: "TikTok", compte: "@angersdirect", url: TIKTOK, site: "tiktok.com", photo: "carte-tiktok", sigle: "TT", action: "S'abonner",
    titre: "L'actu d'Angers en vidéos courtes",
    texte: "Chaque jour, l'essentiel de l'info locale en moins d'une minute.",
    pastille: { background: "#000", boxShadow: "-2px -2px 0 #25F4EE, 2px 2px 0 #FE2C55" },
    etiquette: { background: "#111111", boxShadow: "-3px 0 0 #25F4EE, 3px 0 0 #FE2C55" },
    couleur: "#111111", remplissage: "#111111",
  },
  {
    nom: "Facebook", compte: "Angers Direct", url: FACEBOOK, site: "facebook.com", photo: "carte-facebook", sigle: "FB", action: "Suivre la page",
    titre: "Vidéos, directs et débats",
    texte: "Toute l'actu de la rédaction, et vos réactions en commentaires.",
    pastille: { background: "#1877F2" },
    etiquette: { background: "#1877F2" },
    couleur: "#1877F2", remplissage: "#1877F2",
  },
];

function Vignette({ v }: { v: (typeof VIDEOS)[number] }) {
  return (
    <a
      href={TIKTOK}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={`${v.titre} (vidéo sur TikTok)`}
      className="relative block aspect-[9/16] w-[140px] shrink-0 snap-start overflow-hidden rounded-[14px] shadow-[0_6px_14px_rgba(15,27,45,0.22)] transition-transform hover:-translate-y-1 md:w-[160px]"
    >
      <img src={`${IMG}/${v.img}.webp`} alt="" loading="lazy" decoding="async" width={540} height={960} className="h-full w-full object-cover" />
      <span aria-hidden="true" className="absolute bottom-3 right-3 flex h-10 w-10 items-center justify-center rounded-full bg-white/95">
        <span className="ml-[3px] border-y-[8px] border-l-[13px] border-y-transparent border-l-[#0F1B2D]" />
      </span>
    </a>
  );
}

/** Carte au style des visuels Angers Direct : photo, bandeau bleu incliné, étiquette framboise, titre bleu nuit, bouton incliné. */
/** Carte au style des visuels Angers Direct : photo, bandeau bleu incliné, étiquette aux couleurs du réseau,
 *  titre bleu nuit, bouton contour incliné qui se remplit de la couleur du réseau au survol. */
function CarteReseau({ r }: { r: (typeof RESEAUX)[number] }) {
  return (
    <a
      href={r.url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex flex-col overflow-hidden rounded-md border border-[#EEF1F5] bg-white shadow-[0_10px_26px_rgba(15,27,45,0.10)] transition-transform hover:-translate-y-1 motion-reduce:transition-none"
    >
      <span className="relative block h-[190px] bg-[#0F1B2D]">
        <img src={`${IMG}/${r.photo}.webp`} alt="" loading="lazy" decoding="async" width={800} height={524} className="h-full w-full object-cover" />
        <span aria-hidden="true" className="absolute inset-0 bg-gradient-to-b from-transparent from-40% to-[rgba(15,27,45,0.45)]" />
        <span aria-hidden="true" className="absolute right-3.5 top-3.5 flex h-[42px] w-[42px] items-center justify-center rounded-xl font-display text-xl text-white" style={r.pastille}>{r.sigle}</span>
      </span>
      <span className="relative z-10 -ml-1.5 -mt-6 self-start -skew-x-12 bg-gradient-to-r from-[#4FA8FF] to-[#1D5FD0] py-2 pl-[22px] pr-[26px]">
        <span className="inline-block skew-x-12 font-display text-[26px] uppercase tracking-wide text-white">{r.nom}</span>
      </span>
      <span className="flex flex-1 flex-col px-6 pb-[22px] pt-4">
        <span className="mt-1 self-start -skew-x-12 px-3 py-0.5" style={r.etiquette}>
          <span className="inline-block skew-x-12 font-display text-sm uppercase tracking-[0.12em] text-white">{r.compte}</span>
        </span>
        <span className="mt-3 font-display text-[28px] leading-[1.05] text-[#0F1B2D]">{r.titre}</span>
        <span className="mt-2 flex-1 text-[16.5px] leading-relaxed text-[#5A6472]">{r.texte}</span>
        <span className="mt-[18px] flex items-center justify-between border-t border-[#ECE6DA] pt-3.5">
          <span
            className="group/btn relative inline-block -skew-x-12 overflow-hidden border-2 bg-white px-[18px] py-[7px]"
            style={{ borderColor: r.couleur, color: r.couleur }}
          >
            <span
              aria-hidden="true"
              className="absolute inset-0 origin-left scale-x-0 transition-transform duration-300 ease-out group-hover/btn:scale-x-100 motion-reduce:transition-none"
              style={{ background: r.remplissage }}
            />
            <span className="relative inline-block skew-x-12 font-display text-[17px] uppercase tracking-wider transition-colors duration-300 group-hover/btn:text-white motion-reduce:transition-none">
              {r.action}{" "}
              <span aria-hidden="true" className="inline-block transition-transform duration-300 group-hover/btn:translate-x-1 motion-reduce:transition-none">→</span>
            </span>
          </span>
          <span className="text-sm tracking-wide text-[#8A8F99]">{r.site}</span>
        </span>
      </span>
    </a>
  );
}

function TitreSection({ titre, intro }: { titre: string; intro: string }) {
  return (
    <div className="mb-5">
      <h2 className="flex items-center gap-3 font-display text-[34px] uppercase leading-none text-[#0F1B2D]">
        <span aria-hidden="true" className="inline-block h-[26px] w-1.5 -skew-x-12 bg-[#1C8FE3]" />
        {titre}
      </h2>
      <p className="mt-1.5 text-base text-[#5A6472]">{intro}</p>
    </div>
  );
}

export const Route = createFileRoute("/videos")({
  head: () => meta("Vidéos", "Les vidéos de l'actualité d'Angers : manifestations, matchs, sorties. Sur Instagram, TikTok et Facebook.", undefined, "/videos"),
  component: () => {
    const articles = ARTICLES.filter((a) => a.video);
    return (
      <>
        <section className="relative isolate overflow-hidden bg-[#0F1B2D] pb-28 pt-10 text-[#F6F1E7] md:pb-32">
          <div aria-hidden="true" className="pointer-events-none absolute -right-32 -top-20 h-[520px] w-[520px] rounded-full" style={{ background: "radial-gradient(circle, rgba(28,143,227,0.35), transparent 65%)" }} />
          <Container className="relative">
            <span className="inline-block -skew-x-12 bg-gradient-to-r from-[#4FA8FF] to-[#1D5FD0] px-3.5 py-1">
              <span className="inline-block skew-x-12 font-display text-sm uppercase tracking-[0.2em] text-white">Vidéos</span>
            </span>
            <h1 className="mt-3.5 font-display text-5xl uppercase leading-[0.95] md:text-[64px]">
              L'actu d'Angers <span className="text-[#5AB6F1]">en images</span>
            </h1>
            <p className="mt-3 max-w-[520px] text-lg opacity-85">
              Manifestations, matchs, sorties : nos reportages vidéo sont sur Instagram, TikTok et Facebook.
            </p>
          </Container>
        </section>
        <Container className="pb-14">
          <section aria-label="Nos dernières vidéos" className="relative -mt-24 md:-mt-[104px]">
            <div className="flex snap-x snap-mandatory gap-4 overflow-x-auto px-1 pb-6 pt-1">
              {VIDEOS.map((v) => <Vignette key={v.img} v={v} />)}
            </div>
          </section>
          <section className="mt-9">
            <TitreSection titre="Suivez-nous en vidéo" intro="Instagram, TikTok et Facebook : toute l'actu d'Angers en images." />
            <div className="grid gap-5 lg:grid-cols-3">
              {RESEAUX.map((r) => <CarteReseau key={r.nom} r={r} />)}
            </div>
          </section>
          {articles.length > 0 && (
            <section className="mt-12 grid gap-8 md:grid-cols-3">
              {articles.map((a) => <ArticleCard key={a.slug} a={a} />)}
            </section>
          )}
        </Container>
      </>
    );
  },
});
