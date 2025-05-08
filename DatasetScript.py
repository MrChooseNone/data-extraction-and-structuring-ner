
import json

all_text = [
    "Anläggningen har utförts enligt SBF 120:5 och SBF 120:6.",
    "Anläggning skall också utföras som en personskyddsanläggning, enligt SBF 120:6/EN 12845 bilaga F i tillämpliga delar. Dock med normal sektionsindelning istället för zonindelning.",
    "Regler för automatisk brandlarmanläggning SBF 110:6.",
    "Projektering, inkoppling och avprovning av anläggningen enligt SBF 110:6",
    "Anläggningen utförs enligt SBF 120:6 i riskklass OH 2 med en vattentäthet på 5 mm/min.",
    "Enligt SBF 120:6 reglerna och VVS AMA 09 ",
    "Märkning skall göras på svenska och även uppfylla gällande sprinklerregler SBF 120:6.  ",
    "Anläggningen utförs enligt SBF 120:6 i riskklass OH 2.",
    "Entreprenaden omfattar etablering, demontering, leverans, installation, inkoppling, driftsättning och dokumentation av en komplett sprinkleranläggning enligt SS EN 12845/SBF 120:8.",
    "Rör, kopplingar och rördelar skall levereras skyddsmålade och uppfylla SBF 120:8.",
    "Tillverkningsstandard: EN10217-1:2004  material PR235 TR-1 eller TR-2. Rören ska vara FM godkända enligt Class Number 1630 eller SBSC certifierade.",
    "Installationen utgör en nyinstallation och utförs enligt SBF120:8/SSEN12845:2015 och enligt Etableringsmanual Brand MAXI.",

    "Samtliga förekommande kopplingar skall vara godkänt av SBSC eller vara UL/FM listat. ",
    "Allt sprinklermateriel skall vara godkänt av SBSC eller vara UL/FM listat. ",

    "Anläggningen utförs enligt SBF 120:6 med vissa tillämpningar från NFPA 13.",
    "Inom lagret utförs ESFR-sprinklersystemet vad gäller dimensionering, hinder, placering, täckningsyta mm enligt NFPA13, 2013.",
    "Anläggningen utförs enligt SBF 120:7 med vissa tillämpningar från NFPA 13 gällande EC-sprinkler",
    "Anläggningen utförs enligt SBF 120:7 med vissa tillämpningar från NFPA13 gällande EC-sprinkler.",

]


with open("TrainDataset.jsonl", "a", encoding="utf-8") as f:
    for text in all_text:
        words = text.strip().split()
        
        entry = {
            "tokens": words,
            "ner_tags": [0] * len(words)  # default NER tag, e.g., "O"
        }

        json.dump(entry, f, ensure_ascii=False)
        f.write("\n")


