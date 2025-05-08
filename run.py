from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, BertTokenizerFast
from pathlib import Path
# import textract
# Directory path
# dir_path = Path('D:/Projekteringsuppdrag/avslutade projekt/1355 Åby Ängar/8. Beskrivningar_PM_Handl-fört')

# # Search for the specific file
# files = dir_path.rglob('SH Ram-SPRINKLER Åby Ängar.docx')

# # Output path
# output_path = Path('C:/Users/alexo/Documents/out12.txt')

# 2a. Point to the folder or Hub repo where you saved your fine‑tuned model
model_path = "C:/Users/alexo/OneDrive/Dokument/Data extraction/my‐swedish‐ner"            # or "your‑username/swedish‐ner‐model" if on Hub

# 2b. Load
#tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer = BertTokenizerFast.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

tokenizer.add_special_tokens({"additional_special_tokens": ["SBF","NFPA"]})
model.resize_token_embeddings(len(tokenizer))
                              
print(tokenizer.tokenize("NFPA 13 120:7/SS-EN 12845"))


ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

decoded_text = """
Regelverk och riskklasser 
 
Anläggningen utförs enligt SBF 120:7. 
Entreprenaden omfattar etablering, demontering, leverans, installation, inkoppling, driftsättning och dokumentation av en komplett sprinkleranläggning enligt SS EN 12845/ SBF 120:8.
Anläggningen utförs enligt SBF 120:7 med vissa tillämpningar från NFPA 13 gällande EC-sprinkler
"""

chunks = []
def chunk_text(text, max_length=128):
    tokens = tokenizer(text, return_offsets_mapping=True, truncation=False)
    input_ids = tokens["input_ids"]

    for i in range(0, len(input_ids), max_length - 2):  # leave room for [CLS] and [SEP]
        chunk_ids = input_ids[i:i + max_length - 2]
        chunk = tokenizer.decode(chunk_ids)
        chunks.append(chunk)
    return chunks

chunk_text(decoded_text)
count = 0
for chunk in chunks:
    print(chunk)
    print(count)
    count += 1
    results = ner(chunk)
    print(results)
    for entity in results:
        print(f"{entity['entity_group']:15} | {entity['word']:30} | score: {entity['score']:.2f}")