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