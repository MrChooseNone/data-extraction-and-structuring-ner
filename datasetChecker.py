import json
for split, path in [("train","TrainDataset.jsonl"),("val","val.jsonl")]:
    with open(path, encoding="utf-8") as f:
        for i,line in enumerate(f,1):
            if not line.strip(): continue
            obj = json.loads(line)    # kommer kasta om mismatch eller fel
            assert len(obj["tokens"]) == len(obj["ner_tags"]), \
                   f"Rad {i} i {split} har {len(obj['tokens'])} tokens men {len(obj['ner_tags'])} tags"
print("Rådata ser konsistent ut!")

            


