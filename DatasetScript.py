
import json

all_text = [
    "Rörväggtjocklekar enligt SS - EN 10255 : 2004 + A1 : 2007 Table B.",
    "Samtliga trimsats rör DN 15 - 50 för sprinklercentral,",
    "sprinkler monterade lägre än 2, 4 m.",
    

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


