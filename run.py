from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, BertTokenizerFast
from pathlib import Path
import textract
import mysql.connector
import os
from dotenv import load_dotenv
import re

#Load variables from .env
load_dotenv()

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

def deduplicate_entities(entities):
    seen = set()
    unique = []
    for e in entities:
        key = (e['word'].lower().strip(), e['entity_group'])
        if key not in seen:
            seen.add(key)
            unique.append(e)
    return unique

#-----------------start SQL connect----------------------
try:
    connection = mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user= os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_DATABASE")
    )

    if connection.is_connected():
        print("succses")


except mysql.connector.Error as e:
    print( e) 

finally:
    if 'connection' in locals() and connection.is_connected():
        #cursor.close()
        connection.close()
        print("MySQL connection closed.")

#-------------------end SQL connect ------------------------

# Directory path
base_dir_path = Path('D:/Projekteringsuppdrag/avslutade projekt/1408 Fisksätra Centrum')


project_pattern = re.compile(r"(\d+)\s([\w\s-]+)") # regex first group(1) = one+ numbers for id, group(2) = one+ any word or space for name
counter = 0
for project_dir in base_dir_path.iterdir(): #Iterate through base dir
    if project_dir.is_dir(): # If it is a directory 
        isMatching = project_pattern.match(project_dir.name)
        if isMatching:
            counter += 1
            projectId = int(isMatching.group(1))    #get the regex group 1 (id)
            projectName = isMatching.group(2)   #get regex group 2 

            print(projectId, projectName)

            # Search for the specific file
            files = project_dir.rglob('SP-BSK Fisksätra Centrum- GHSH.docx')
            # files = []
            # for path in project_dir.rglob("*.docx"):
            #     try:
            #         # Skip if any part of the path is a ZIP file
            #         if any(part.suffix == '.zip' for part in path.parents):
            #             continue
            #         files.append(path)
            #     except Exception as e:
            #         print(f"Skipped {path} due to error: {e}")


            #For each file the rglob() finds we apply the ner model
            for file in files:
                if file.suffix.lower != '.zip':
                    try:
                        #print(file)
                        text = textract.process(str(file))  # Using textraxt to extract text
                        decoded_text = text.decode("utf-8", errors="ignore").strip() # Decode it to utf-8
                    except:
                        print("bad file")

                    chunks = []

                    chunk_text(decoded_text)    # call chunk_text function
                    count = 0
                    allEntities = []
                    for chunk in chunks:
                        #print(chunk)
                        #print("processing...")
                        count += 1
                        results = ner(chunk)    # Apply ner model to the chunk
                        results = [e for e in results if e["score"] >= 0.6] # threshold for entities, change the value, maybe?
                        allEntities += results
                            
                    new = deduplicate_entities(allEntities)
                    for entity in new:
                        print(f"{entity['entity_group']:15} | {entity['word']:30} | score: {entity['score']:.2f}")  # Print entities
                    
                    #Load into SQL
                    if connection.is_connected():
                        cursor = connection.cursor()



                        sql = "INSERT INTO verk (projectId, verk) VALUES (%s, %s)"
                        values = [(projectId, item["verk"]) for item in new] 

                        cursor.execute(sql, values)
                        connection.commit()

                        print("wow")

                        cursor.close()
                        connection.close()


