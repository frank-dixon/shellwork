"""Builds shellwork/data/seed.json from hand-curated facts + scraped vendor stats.
Every factual field below is tied to a citation key; see CITES."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # the shellwork app dir
SEL = json.loads((ROOT / "tools/commons_selection.json").read_text())
ACC = "2026-10-15"
MM = "McMurray Hatchery"; KC = "Koops Coops"; LC = "The Livestock Conservancy"
mm = lambda p: f"https://www.mcmurrayhatchery.com/{p}.html"
kc = lambda p: f"https://www.koopscoops.com/product/{p}/"
lc = lambda p: f"https://livestockconservancy.org/heritage-breeds/heritage-breeds-list/{p}/"

# breed -> list of (publisher, title, url, kind, supports, excerpt)
B = []
def breed(**kw): B.append(kw)

breed(slug="leghorn", name="White Leghorn", egg_color_name="White", egg_color_category="white", egg_hex="#F3F0E8", shell_finish="gloss",
      egg_size="L", egg_size_note="Large (McMurray, Koops); large to extra-large (Livestock Conservancy)", lay_rate_min=250, lay_rate_max=300,
      temperament="Very active. McMurray: disposition 'poor'", broodiness="Rarely goes broody (seldom sits on eggs to hatch them)", autosexing="unknown",
      genetics_notes="White shell: almost no pigment is deposited.",
      breeding_notes="Adds no brown pigment, so daughters of a Leghorn × blue-layer cross that carry the blue allele should lay blue (inferred from genetics).",
      cites=[(LC,"Leghorn - Non Industrial - Chicken",lc("leghorn-chicken"),"conservancy","egg_color_name,egg_size,temperament","Egg Color: White; Egg Size: Large to Extra-Large; Temperament: Very Active"),
             (MM,"Pearl White Leghorns",mm("pearl_white_leghorn"),"hatchery","egg_color_name,egg_size,broodiness,temperament","Egg Color: white; Egg Size: large; Disposition: poor; Broody: not at all likely"),
             (KC,"White Leghorns",kc("white-leghorns"),"hatchery","egg_size,lay_rate","Egg Size: Large; Eggs per year: 250-300; Not very broody")])
breed(slug="ameraucana", name="Ameraucana", origin="United States", egg_color_name="Blue", egg_color_category="blue", egg_hex="#A8CCD3", shell_finish="satin",
      egg_size="L", egg_size_note="Large (McMurray)", temperament="Docile and friendly", broodiness="Rarely goes broody (seldom sits on eggs to hatch them)", autosexing="unknown",
      genetics_notes="Blue shell from the oocyan (O) allele: an EAV-HP retroviral insertion upstream of SLCO1B3 makes the shell gland deposit biliverdin through the whole shell, so the inside is blue too. Dominant.",
      breeding_notes="One copy of the blue allele is enough; crossed onto a brown layer, daughters that inherit it lay green/olive.",
      cites=[(MM,"Ameraucanas",mm("ameraucanas"),"hatchery","egg_color_name,egg_size,broodiness,temperament","Egg Color: blue; Egg Size: large; Disposition: good; Broody: not very likely; docile, friendly, quiet"),
             (KC,"Blue Ameraucana",kc("blue-ameraucana"),"hatchery","origin,temperament","Temperament: docile and friendly. History: originated in the United States.")])
breed(slug="araucana", name="Araucana", egg_color_name="Blue", egg_color_category="blue", egg_hex="#9CC8C9", shell_finish="satin",
      egg_size="M", egg_size_note="Medium to large (Livestock Conservancy)", temperament="Docile", autosexing="unknown",
      genetics_notes="Same oocyan/EAV-HP mechanism as other blue layers; the insertion was traced in South American (Mapuche) fowl.",
      breeding_notes="Rumpless and tufted traits are separate from egg color. Livestock Conservancy lists the breed as Critical.",
      cites=[(LC,"Araucana Chicken",lc("araucana-chicken"),"conservancy","egg_color_name,egg_size,temperament","Status: Critical; Egg Color: Blue; Egg Size: Medium to Large; Temperament: Docile")])
breed(slug="cream-legbar", name="Cream Legbar", egg_color_name="Blue", egg_color_category="blue", egg_hex="#B2D4C8", shell_finish="satin",
      egg_size="M", egg_size_note="Medium (McMurray, Koops)", lay_rate_min=150, lay_rate_max=200, temperament="Friendly and calm",
      broodiness="Rarely goes broody (seldom sits on eggs to hatch them)", autosexing="yes",
      genetics_notes="Blue via the oocyan allele. Autosexing: chicks can be sexed by down pattern at hatch.",
      breeding_notes="Koops Coops has crossed Cream Legbar with French Cuckoo Marans and on Welsummer to make green-egg layers.",
      cites=[(MM,"Cream Legbars",mm("cream_legbars"),"hatchery","egg_color_name,egg_size,broodiness,autosexing","Egg Color: blue; Egg Size: medium; Broody: not very likely; 'one of the most popular auto-sexing breeds'"),
             (KC,"Cream Legbars",kc("cream-legbars"),"hatchery","egg_size,lay_rate,temperament","Blue egg; Medium; 150-200 per year; friendly and calm")])
breed(slug="easter-egger", name="Easter Egger", is_cross=True, egg_color_name="Blue, green or other (varies by hen)", egg_color_category="variable",
      egg_hex="#B7CBA6", shell_finish="satin", egg_size="M", egg_size_note="Medium (Koops)", lay_rate_min=200, lay_rate_max=250,
      temperament="Not sourced; Koops calls it very beginner-friendly", broodiness="Sometimes goes broody (may sit on eggs to hatch them)", autosexing="no",
      genetics_notes="Not a breed: a cross of a regular brown layer with a blue layer, so egg color depends on which alleles each hen carries.",
      breeding_notes="Hens from one hatch can lay blue, green or, occasionally, tinted eggs.",
      cites=[(KC,"Easter Eggers",kc("easter-eggers"),"hatchery","egg_color_name,egg_size,lay_rate,temperament,broodiness","Blue egg; Medium; 200-250 per year; occasionally broody; very beginner-friendly"),
             (KC,"Olive Egger (Easter Egger definition)",kc("olive-egger"),"hatchery","genetics_notes","Easter Eggers are produced by crossing a regular brown egg layer with a blue egg layer.")])
breed(slug="olive-egger", name="Olive Egger", is_cross=True, egg_color_name="Olive / sage green (can vary)", egg_color_category="green",
      egg_hex="#8E9A5C", speckle_density=0.15, speckle_hex="#4E4A26", shell_finish="matte", egg_size="XL", egg_size_note="Extra large (Koops)",
      lay_rate_min=250, lay_rate_max=300, temperament="Friendly and adaptable", broodiness="Rarely goes broody (seldom sits on eggs to hatch them)", autosexing="no",
      genetics_notes="Olive shell: a blue shell (oocyan) with a layer of brown protoporphyrin on top.",
      breeding_notes="Produced from a dark-brown layer × blue layer. Hens can still lay blue or brown, because egg color genes segregate.",
      cites=[(KC,"Olive Egger",kc("olive-egger"),"hatchery","egg_color_name,egg_size,lay_rate,temperament,broodiness,genetics_notes,breeding_notes","Egg Color: Olive; XLarge; 250-300 per year; 'blue eggs have brown pigment over the top, creating the shade of olive green'")])
breed(slug="marans", name="Black Copper Marans", egg_color_name="Dark brown", egg_color_category="dark-brown", egg_hex="#6A3A26",
      speckle_density=0.35, speckle_hex="#3A190E", shell_finish="matte", egg_size="L", egg_size_note="Large (McMurray, Koops)",
      lay_rate_min=150, lay_rate_max=200, temperament="Not sourced. McMurray: disposition 'excellent'", broodiness="Sometimes goes broody (may sit on eggs to hatch them)", autosexing="unknown",
      genetics_notes="Dark color is protoporphyrin IX deposited late, mostly in the outer shell and cuticle, so it can partly rub off. Color usually fades over a laying season.",
      breeding_notes="Common brown parent for olive eggers.",
      cites=[(MM,"Black Copper Marans",mm("black_copper_marans"),"hatchery","egg_color_name,egg_size,broodiness,temperament","Egg Color: dark brown; Egg Size: large; Disposition: excellent; Broody: somewhat likely"),
             (KC,"Black Copper Maran",kc("black-copper-maran"),"hatchery","lay_rate,egg_size","Dark brown egg; Large; 150-200 per year")])
breed(slug="welsummer", name="Welsummer", origin="Netherlands", egg_color_name="Dark brown, often speckled", egg_color_category="dark-brown",
      egg_hex="#9A5536", speckle_density=0.8, speckle_hex="#4A1F0F", shell_finish="matte", egg_size="L", egg_size_note="Large (McMurray)",
      lay_rate_min=220, lay_rate_max=280, temperament="Docile", broodiness="Sometimes goes broody (may sit on eggs to hatch them)", autosexing="no",
      genetics_notes="Brown pigment (protoporphyrin IX) applied in the shell gland; speckling is extra pigment laid on near the end.",
      breeding_notes="Koops Coops has crossed Welsummer with Cream Legbar to try for speckled green eggs.",
      cites=[(MM,"Welsummer",mm("welsummer"),"hatchery","origin,egg_color_name,egg_size,lay_rate,temperament,broodiness,autosexing","Originated in Holland; docile; dark brown eggs; large; 220-280 eggs per year; somewhat likely broody; not auto sexing")])
breed(slug="barnevelder", name="Barnevelder", egg_color_name="Dark brown", egg_color_category="dark-brown", egg_hex="#8A5A3F",
      speckle_density=0.12, speckle_hex="#4A2618", shell_finish="matte", egg_size="L", egg_size_note="Large (Koops)", lay_rate_min=150, lay_rate_max=200,
      temperament="Calm and friendly", broodiness="Sometimes goes broody (may sit on eggs to hatch them)", autosexing="unknown",
      genetics_notes="Brown shell from protoporphyrin IX (see glossary).", breeding_notes="",
      cites=[(KC,"Barnevelder",kc("barnevelder"),"hatchery","egg_color_name,egg_size,lay_rate,temperament,broodiness","Dark brown egg; Large; 150-200 per year; occasionally broody; calm and friendly")])
breed(slug="penedesenca", name="Penedesenca", egg_color_name="Very dark brown", egg_color_category="dark-brown", egg_hex="#5E3022",
      speckle_density=0.2, speckle_hex="#2E140B", shell_finish="matte", egg_size="XL", egg_size_note="Extra large (Koops)", lay_rate_min=200, lay_rate_max=250,
      temperament="Not sourced; Koops calls it good for beginners", broodiness="Sometimes goes broody (may sit on eggs to hatch them)", autosexing="unknown",
      genetics_notes="Brown shell from protoporphyrin IX (see glossary).", breeding_notes="Figures come from one hatchery and haven't been confirmed elsewhere.",
      cites=[(KC,"Crele Penedesenca",kc("crele-pendesenca"),"hatchery","egg_color_name,egg_size,lay_rate,temperament,broodiness","Dark brown egg; XLarge; 200-250 per year; occasionally broody; good for beginners")])
breed(slug="orpington", name="Buff Orpington", egg_color_name="Light brown to brown", egg_color_category="light-brown", egg_hex="#D6AE86",
      shell_finish="satin", egg_size="L", egg_size_note="Large (McMurray); large to XL (Conservancy); XL (Koops)", lay_rate_min=200, lay_rate_max=250,
      temperament="Calm, friendly", broodiness="Very often goes broody (likes to sit on and hatch eggs)", autosexing="unknown",
      genetics_notes="Brown shell from protoporphyrin IX (see glossary).", breeding_notes="Very likely to go broody, so often used to hatch other breeds' eggs.",
      cites=[(LC,"Orpington Chicken",lc("orpington-chicken"),"conservancy","egg_color_name,egg_size,temperament","Egg Color: Brown; Egg Size: Large to Extra Large; Temperament: Calm, friendly disposition"),
             (MM,"Buff Orpingtons",mm("buff_orpingtons"),"hatchery","egg_color_name,egg_size,broodiness","brown; large; Broody: extremely likely"),
             (KC,"Buff Orpington",kc("buff-orpington"),"hatchery","egg_color_name,lay_rate","Light brown egg; XLarge; 200-250 per year")])
breed(slug="plymouth-rock", name="Barred Plymouth Rock", origin="United States (exhibited in Boston, 1849)", egg_color_name="Brown", egg_color_category="brown",
      egg_hex="#C08C63", shell_finish="satin", egg_size="L", egg_size_note="Sources differ: medium (McMurray), large (Conservancy), XL (Koops)",
      lay_rate_min=200, lay_rate_max=280, temperament="Calm, docile", broodiness="Sources differ: rarely goes broody (McMurray) or often broody (Koops)", autosexing="unknown",
      genetics_notes="Brown shell from protoporphyrin IX (see glossary).", breeding_notes="",
      cites=[(LC,"Plymouth Rock Chicken",lc("plymouth-rock-chicken"),"conservancy","origin,egg_color_name,egg_size,temperament","Developed in America in the mid-19th century, first exhibited in Boston in 1849; Brown; Large; Calm, Docile"),
             (MM,"Barred Rocks",mm("barred_rocks"),"hatchery","egg_size,lay_rate,broodiness","brown; medium; average 225 per year; 'about 220-280 eggs a year'; not very likely broody"),
             (KC,"Barred Rock",kc("barred-rock-2"),"hatchery","lay_rate,egg_size,broodiness","Brown egg; XLarge; 200-250 per year; broody")])
breed(slug="rhode-island-red", name="Rhode Island Red", egg_color_name="Brown", egg_color_category="brown", egg_hex="#B37B52", shell_finish="satin",
      egg_size="L", egg_size_note="Large (McMurray, Conservancy); XL (Koops)", lay_rate_min=238, lay_rate_max=300,
      temperament="Calm", broodiness="Rarely goes broody (production strain; seldom sits on eggs to hatch them)", autosexing="unknown",
      genetics_notes="Brown shell from protoporphyrin IX (see glossary).", breeding_notes="McMurray's flock is a production strain selected for lay and less broodiness; heritage lines may differ.",
      cites=[(LC,"Rhode Island Red Chicken",lc("rhode-island-red-chicken"),"conservancy","egg_color_name,egg_size,temperament","Brown; Large; Temperament: Calm"),
             (MM,"Rhode Island Reds",mm("rhode_island_reds"),"hatchery","lay_rate,broodiness,breeding_notes","Average eggs per year: 238; Broody: not at all likely; production strain"),
             (KC,"RI Red",kc("ri-red"),"hatchery","lay_rate","Brown; XLarge; 250-300 per year")])
breed(slug="sussex", name="Sussex", egg_color_name="Tan to brown", egg_color_category="light-brown", egg_hex="#D3B08A", shell_finish="satin",
      egg_size="L", egg_size_note="Large (all three sources)", lay_rate_min=150, lay_rate_max=250, temperament="Calm and curious",
      broodiness="Often goes broody per McMurray (likes to sit on and hatch eggs); sometimes per Koops", autosexing="unknown",
      genetics_notes="Brown shell from protoporphyrin IX (see glossary).", breeding_notes="Photo shows a Light Sussex. Figures are for the Speckled Sussex.",
      cites=[(LC,"Sussex Chicken",lc("sussex-chicken"),"conservancy","egg_color_name,egg_size,temperament","Tan to Brown; Large; Calm and Curious"),
             (MM,"Speckled Sussex",mm("speckled_sussex"),"hatchery","lay_rate,broodiness","151-220 eggs per year; very likely broody"),
             (KC,"Speckled Sussex",kc("speckled-sussex"),"hatchery","lay_rate","Brown; Large; 200-250 per year")])
breed(slug="silkie", name="Silkie", egg_color_name="White (McMurray)", egg_color_category="white", egg_hex="#F0E9DA",
      shell_finish="satin", egg_size="S", egg_size_note="Small", lay_rate_min=150, lay_rate_max=200, temperament="Not sourced. McMurray: disposition 'best'",
      broodiness="Very often goes broody (likes to sit on and hatch eggs)", autosexing="unknown",
      genetics_notes="", breeding_notes="Very likely to go broody; often used to hatch other birds' eggs.",
      cites=[(MM,"Bantam White Silkies",mm("bantam_white_silkies"),"hatchery","egg_color_name,egg_size,temperament,broodiness","Egg Color: white; small; Disposition: best; Broody: extremely likely"),
             (KC,"Assorted Silkies",kc("assorted-silkies"),"hatchery","lay_rate","Small; 150-200 per year; broody")])
breed(slug="australorp", name="Black Australorp", origin="Australia (from English Black Orpingtons)", egg_color_name="Light brown to brown",
      egg_color_category="light-brown", egg_hex="#CDA07B", shell_finish="satin", egg_size="L", egg_size_note="Large (McMurray, Koops); medium to large (Conservancy)",
      lay_rate_min=226, lay_rate_max=300, temperament="Active, yet gentle", broodiness="Sources differ: rarely goes broody (McMurray) or often broody (Koops)", autosexing="unknown",
      genetics_notes="Brown shell from protoporphyrin IX (see glossary).", breeding_notes="",
      cites=[(LC,"Australorp Chicken",lc("australorp-chicken"),"conservancy","egg_color_name,egg_size,temperament","Tinted to Light Brown; Medium to Large; Active, yet gentle"),
             (MM,"Black Australorps",mm("black_australorps"),"hatchery","origin,egg_color_name,lay_rate,broodiness","Developed from Black Orpingtons imported from England; brown; large; average 226 per year"),
             (KC,"Black Australorp",kc("black-australorp"),"hatchery","lay_rate","Brown; Large; 250-300 per year")])
breed(slug="faverolles", name="Salmon Faverolles", egg_color_name="Cream / tinted to light brown", egg_color_category="cream", egg_hex="#E1C8A6",
      shell_finish="satin", egg_size="M", egg_size_note="Medium (McMurray, Koops); medium to large (Conservancy)", lay_rate_min=150, lay_rate_max=200,
      temperament="Docile, gentle, friendly", broodiness="Very often goes broody (likes to sit on and hatch eggs)", autosexing="unknown",
      genetics_notes="Light shell: little protoporphyrin is deposited.", breeding_notes="Conservancy status: Watch.",
      cites=[(LC,"Faverolles Chicken",lc("faverolles-chicken"),"conservancy","egg_color_name,egg_size,temperament","Status: Watch; Tinted to Light Brown; Medium to Large; Active, yet gentle"),
             (MM,"Salmon Faverolles",mm("salmon_faverolles"),"hatchery","egg_color_name,egg_size,broodiness","cream; medium; Broody: extremely likely"),
             (KC,"Salmon Faverolles",kc("salmon-faverolles"),"hatchery","lay_rate,temperament","Light brown; Medium; 150-200 per year; docile, gentle, friendly")])

GEN = {
 "wang2013": dict(publisher="PLOS Genetics", title="Wang Z. et al. (2013) An EAV-HP insertion in 5′ flanking region of SLCO1B3 causes blue eggshell in the chicken",
                  url="https://doi.org/10.1371/journal.pgen.1003183", kind="peer-reviewed", supports="genetics_notes", excerpt="Blue eggshell (oocyan) is caused by an EAV-HP insertion that up-regulates SLCO1B3 in the shell gland, increasing biliverdin uptake."),
 "wragg2013": dict(publisher="PLOS ONE", title="Wragg D. et al. (2013) Endogenous retrovirus EAV-HP linked to blue egg phenotype in Mapuche fowl",
                   url="https://doi.org/10.1371/journal.pone.0071393", kind="peer-reviewed", supports="genetics_notes", excerpt="Independent confirmation of the EAV-HP insertion in South American blue-egg fowl."),
 "samiullah2015": dict(publisher="Poultry Science", title="Samiullah S., Roberts J.R., Chousalkar K. (2015) Eggshell color in brown-egg laying hens — a review",
                       url="https://doi.org/10.3382/ps/pev202", kind="peer-reviewed", supports="genetics_notes", excerpt="Brown color is protoporphyrin IX, concentrated in the outer shell and cuticle; color intensity tends to decline with hen age."),
 "lc-heritage": dict(publisher=LC, title="Heritage chicken definition", url="https://livestockconservancy.org/heritage-breeds/heritage-breeds-list/", kind="conservancy", supports="glossary", excerpt="Conservation priority list and heritage breed definitions."),
}
BLUE = {"ameraucana", "araucana", "cream-legbar", "easter-egger", "olive-egger"}
BROWN = {"marans", "welsummer", "barnevelder", "penedesenca", "orpington", "plymouth-rock", "rhode-island-red", "sussex", "australorp", "faverolles", "olive-egger"}

GLOSS = [
 ("Oocyan (O) allele", "The dominant blue-eggshell allele. One copy makes the whole shell blue, inside and out.", "wang2013"),
 ("SLCO1B3", "A transporter gene. The blue-shell insertion switches it on in the shell gland so that biliverdin is taken up into the shell.", "wang2013"),
 ("EAV-HP", "An endogenous avian retrovirus. Its insertion near SLCO1B3 is the cause of blue eggs, found in both Chinese and Mapuche fowl.", "wragg2013"),
 ("Biliverdin", "The blue-green pigment in blue eggshells.", "wang2013"),
 ("Protoporphyrin IX", "The brown pigment, laid mainly in the outer shell and cuticle. It usually lightens as a hen ages.", "samiullah2015"),
 ("Cuticle / bloom", "The thin organic coat on a freshly laid egg. On brown eggs it carries much of the pigment.", "samiullah2015"),
 ("Olive egg", "A blue shell with brown pigment over it. Usually from a dark-brown × blue cross.", "kc:olive-egger"),
 ("Easter Egger", "A cross of a regular brown layer and a blue layer, not a recognized breed. Egg color varies from hen to hen.", "kc:olive-egger"),
 ("Autosexing", "A breed whose chicks can be sexed at hatch by down color or pattern, e.g. Cream Legbar.", "mm:cream-legbar"),
 ("Broody", "A broody hen wants to sit on eggs and hatch them. Breeds differ: some rarely go broody, others often do. Hatcheries rate how likely each breed is.", "mm:orpington"),
 ("Heritage breed", "A traditional breed tracked on The Livestock Conservancy priority list (Critical, Watch, Recovering, etc.).", "lc-heritage"),
]
PAIRS = [
 ("ameraucana", "marans", "green", "Olive green", "Purebred Ameraucanas carry two copies of the dominant blue allele, so every first-generation daughter gets one and lays a blue shell under heavy brown pigment: olive. Brown-only layers can appear in later generations.", "sourced", "kc:olive-egger"),
 ("cream-legbar", "marans", "green", "Sage to olive green", "Koops Coops crossed Cream Legbar with French Cuckoo Marans for olive eggers. The shade varies between sage and olive.", "sourced", "kc:olive-egger"),
 ("cream-legbar", "welsummer", "green", "Green, possibly speckled", "Koops Coops crossed these to aim for speckled green eggs. Speckling is not guaranteed.", "sourced", "kc:olive-egger"),
 ("ameraucana", "rhode-island-red", "variable", "Blue/green mix (Easter Egger type)", "Crossing a brown layer with a blue layer produces Easter Eggers. Egg color varies from hen to hen.", "sourced", "kc:olive-egger"),
 ("araucana", "leghorn", "blue", "Blue", "Leghorns add no brown pigment, so daughters carrying the dominant blue allele should lay blue (inferred from genetics, not reported by a breeder).", "inferred", "wang2013"),
]

out = {"breeds": [], "general_citations": [], "glossary": [], "pairings": []}
for i, b in enumerate(B):
    cites = b.pop("cites")
    b["sort_order"] = i
    b["citations"] = [dict(publisher=p, title=t, url=u, kind=k, supports=s, excerpt=e, accessed=ACC) for p, t, u, k, s, e in cites]
    photos = []
    for kind in ("hen", "egg"):
        s = SEL.get(f"{b['slug']}|{kind}")
        if not s:
            continue
        cap = s["desc"] or s["title"][5:]
        import re as _re
        author = s["artist"].replace("No machine-readable author provided. ", "")
        author = _re.sub(r"\s*assumed \(based on copyright claims\)\.?|^Photo:\s*|\s*\(talk\)\s*\(Uploads\)", "", author).strip() or "See source page"
        photos.append(dict(kind=kind, file=Path(s["file"]).name, caption=cap[:300], author=author[:200], source_url=s["page"],
                           license_name=s["license"], license_url=s["license_url"] or "",
                           attribution_text=f"“{s['title'][5:]}” by {author}, {s['license']}, via Wikimedia Commons"))
    b["photos"] = photos
    out["breeds"].append(b)
for key, g in GEN.items():
    out["general_citations"].append(dict(key=key, accessed=ACC, **g))
for t, d, c in GLOSS:
    out["glossary"].append(dict(term=t, definition=d, cite=c))
VARIETY = {("cream-legbar", "marans"): "The source used French Cuckoo Marans, not Black Copper Marans."}
PARENT_B_LABEL = {("cream-legbar", "marans"): "French Cuckoo Marans"}
OFFSPRING = {  # (hex, speckle density, speckle hex, finish): approximate on-screen render of the expected egg
    ("ameraucana", "marans"): ("#7E8A4C", 0.15, "#3E3A1C", "matte"),
    ("cream-legbar", "marans"): ("#93A36C", 0.1, "#4A4424", "satin"),
    ("cream-legbar", "welsummer"): ("#8C9A5E", 0.6, "#463A1A", "matte"),
    ("ameraucana", "rhode-island-red"): ("#B3C6A8", 0, "#4A3A1C", "satin"),
    ("araucana", "leghorn"): ("#A8CDD2", 0, "#4A3A1C", "satin"),
}
for a, bb, cat, col, ex, conf, c in PAIRS:
    h, sd, sc, fin = OFFSPRING[(a, bb)]
    out["pairings"].append(dict(a=a, b=bb, cat=cat, color=col, explanation=ex, confidence=conf, cite=c,
                                variety_note=VARIETY.get((a, bb), ""), parent_b_label=PARENT_B_LABEL.get((a, bb), ""),
                                offspring=dict(offspring_hex=h, offspring_speckle_density=sd, offspring_speckle_hex=sc, offspring_finish=fin)))
out["genetic_links"] = {"blue": sorted(BLUE), "brown": sorted(BROWN)}
(ROOT / "data/seed.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(len(out["breeds"]), "breeds")
