
from datasets import load_dataset
from transformers import (
  AutoTokenizer,
  AutoModelForTokenClassification,
  DataCollatorForTokenClassification,
  TrainingArguments,
  Trainer,
)

label2id = {
    "EVN": 13,
    "LOC": 7,
    "LOC/ORG": 11,
    "LOC/PRS": 10,
    "MSR": 12,
    "O": 0,
    "OBJ": 1,
    "OBJ/ORG": 4,
    "ORG": 8,
    "ORG/PRS": 3,
    "PER": 9,
    "PRS/WRK": 5,
    "TME": 2,
    "WRK": 6,
    "B-VERK": 14,
    "I-VERK": 15,
    }
id2label = {
    "0": "O",
    "1": "OBJ",
    "2": "TME",
    "3": "ORG/PRS",
    "4": "OBJ/ORG",
    "5": "PRS/WRK",
    "6": "WRK",
    "7": "LOC",
    "8": "ORG",
    "9": "PER",
    "10": "LOC/PRS",
    "11": "LOC/ORG",
    "12": "MSR",
    "13": "EVN",
    "14": "B-VERK",
    "15": "I-VERK",
    }
label_num = len(label2id)

raw = load_dataset("json", data_files={"train":"TrainDataset.jsonl","validation":"val.jsonl"})

# Initialize QA pipeline only once
model_name = "KB/bert-base-swedish-cased-ner"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(
    model_name,
    num_labels=label_num,
    id2label=id2label, 
    label2id=label2id,
    ignore_mismatched_sizes=True
    )

tokenizer.add_special_tokens({"additional_special_tokens": ["SBF","NFPA"]})
model.resize_token_embeddings(len(tokenizer))

def tokenize_and_align(ex):
    toks = tokenizer(ex["tokens"], is_split_into_words=True, truncation=True)
    wids = toks.word_ids()
    labs = ex["ner_tags"]
    aligned = [(labs[w] if w is not None and w!=prev else -100)
               for prev, w in zip([-1]+wids[:-1], wids)]
    toks["labels"] = aligned
    return toks

tokenized = raw.map(tokenize_and_align, batched=False, remove_columns=["tokens","ner_tags"])

data_collator = DataCollatorForTokenClassification(tokenizer)

args = TrainingArguments(
  "swedish-ner", eval_strategy="epoch",
  per_device_train_batch_size=16, per_device_eval_batch_size=16,
  num_train_epochs=3, learning_rate=3e-5
)
trainer = Trainer(
  model, args,
  train_dataset=tokenized["train"],
  eval_dataset=tokenized["validation"],
  tokenizer=tokenizer,
  data_collator=data_collator
)
trainer.train()
trainer.save_model("C:/Users/alexo/OneDrive/Dokument/Data extraction/my‐swedish‐ner")

# Directory path
# dir_path = Path('D:/Projekteringsuppdrag/avslutade projekt/1355 Åby Ängar/8. Beskrivningar_PM_Handl-fört')

# # Search for the specific file
# files = dir_path.rglob('SH Ram-SPRINKLER Åby Ängar.docx')

# # Output path
# output_path = Path('C:/Users/alexo/Documents/out12.txt')
# ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# decoded_text = """
# text, Alexander Ohlsson
# """

# chunks = []
# def chunk_text(text, max_length=64):
#     tokens = tokenizer(text, return_offsets_mapping=True, truncation=False)
#     input_ids = tokens["input_ids"]

#     for i in range(0, len(input_ids), max_length - 2):  # leave room for [CLS] and [SEP]
#         chunk_ids = input_ids[i:i + max_length - 2]
#         chunk = tokenizer.decode(chunk_ids)
#         chunks.append(chunk)
#     return chunks

# chunk_text(decoded_text)
# count = 0
# for chunk in chunks:
#     print(chunk)
#     print(count)
#     count += 1
#     results = ner(chunk)
#     for entity in results:
#         print(f"{entity['entity_group']:15} | {entity['word']:30} | score: {entity['score']:.2f}")

# Print results


# l = []
# for token in outputs:
#     if token['word'].startswith('##'):
#         l[-1]['word'] += token['word'][2:]
#     else:
#         l += [ token ]

# print(l)

# for file in files:
#     try:
#         print(f"Processing: {file}")
        
#         # Extract text
#         text = textract.process(str(file))
#         decoded_text = text.decode("utf-8", errors="ignore").strip()

#         if not decoded_text:
#             raise ValueError("Text extraction returned empty content.")

#         # Save extracted text
#         with open(output_path, 'w', encoding='utf-8') as f:
#             f.write(decoded_text)
#         print("Text extraction complete.")

       

#         
#         # Ask questions
#         # for question in questions:
#         #     result = qa_pipeline(question=question, context=decoded_text)
#         #     print(f"Q: {question}")
#         #     print(f"A: {result['answer']}\n")

#     except Exception as e:
#         print(f"Failed to process {file}: {e}")
