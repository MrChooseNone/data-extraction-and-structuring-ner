from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, BertTokenizerFast
from pathlib import Path
import textract

# Directory path
dir_path = Path('D:/Projekteringsuppdrag/avslutade projekt/1408 Fisksätra Centrum/8. Beskrivningar_PM_Handl-fört')

# # Search for the specific file
files = dir_path.rglob('SP-BSK Fisksätra Centrum- SH.docx')

# # Output path
output_path = Path('C:/Users/alexo/Documents/out12.txt')

# Point to the folder of our fine‑tuned model
model_path = "C:/Users/alexo/OneDrive/Dokument/Data extraction/my‐swedish‐ner" 

# Load model and tokenizer
#tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer = BertTokenizerFast.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

tokenizer.add_special_tokens({"additional_special_tokens": ["SBF","NFPA"]}) # Add special token, This it so it wont split these words
model.resize_token_embeddings(len(tokenizer))
                              
print(tokenizer.tokenize("NFPA 13 120:7/SS-EN 12845")) # test the tokenizer

ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple") #Use Pipeline to prepere the ner model

# decoded_text = """
# Regelverk och riskklasser 
 
# Anläggningen utförs enligt SBF 120:7. 
# Entreprenaden omfattar etablering, demontering, leverans, installation, inkoppling, driftsättning och dokumentation av en komplett sprinkleranläggning enligt SS EN 12845/ SBF 120:8.
# Anläggningen utförs enligt SBF 120:7 med vissa tillämpningar från NFPA 13 gällande EC-sprinkler

# """

# Function for chunking text to accomedate to the ner model max length, devide the text into smaller chunks
def chunk_text(text, max_length=128):
    tokens = tokenizer(text, return_offsets_mapping=True, truncation=False)
    input_ids = tokens["input_ids"]

    for i in range(0, len(input_ids), max_length - 2):  # leave room for [CLS] and [SEP]
        chunk_ids = input_ids[i:i + max_length - 2]
        chunk = tokenizer.decode(chunk_ids)
        chunks.append(chunk)
    return chunks


#For each file the rglob() finds we apply the ner model
for file in files:
    print(file)
    text = textract.process(str(file))  # Using textraxt to extract text
    decoded_text = text.decode("utf-8", errors="ignore").strip() # Decode it to utf-8

    chunks = []

    chunk_text(decoded_text)    # call chunk_text function
    count = 0
    for chunk in chunks:
        print(chunk)
        print(count)
        count += 1
        results = ner(chunk)    # Apply ner model to the chunk
        results = [e for e in results if e["score"] >= 0.6] # threshold for entities, change the value, maybe?
        print(results)
        for entity in results:
            print(f"{entity['entity_group']:15} | {entity['word']:30} | score: {entity['score']:.2f}")  # Print entities