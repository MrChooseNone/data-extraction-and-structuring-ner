
import json

all_text = [
    "Brandförsvarsföreningen utgivna ”Regler för Gassläcksystem”, SBF 500 : 4 . ",
    "Integritetstest av lokalen skall i enlighet med krav i SBF 500 : 4 genomföras . ",
    "Anläggningen utförs som våtrörssystem och i tillämpliga delar enligt SS-EN 16925:2018 och SBF 501 : 2 .",
    "Allt sprinklermateriel ska vara typgodkänt av SBSC, FM eller UL. ",
    
    

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


