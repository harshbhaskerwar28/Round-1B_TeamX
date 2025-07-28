from transformers import pipeline
from transformers import AutoTokenizer

def get_summarizer():
    model_name = "t5-small"
    summarizer = pipeline("summarization", model=model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return summarizer, tokenizer

def summarize_subsections(top_sections, max_length=300):
    summarizer, tokenizer = get_summarizer()
    summaries = []
    for section in top_sections:
        input_text = "summarize: " + section['text']
        # Tokenize and truncate to 512 tokens
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
        input_text_trunc = tokenizer.decode(inputs['input_ids'][0], skip_special_tokens=True)
        effective_max = min(max_length, len(input_text_trunc.split()) // 2 + 1)
        refined = summarizer(input_text_trunc, max_length=effective_max, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append({
            'document': section['document'],
            'refined_text': refined,
            'page_number': section['page_number']
        })
    return summaries 