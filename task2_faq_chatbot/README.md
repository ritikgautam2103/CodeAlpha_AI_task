# Task 2 — FAQ Chatbot

This project implements an FAQ chatbot using NLP preprocessing, TF-IDF vectorization, and cosine similarity.

## How it works

1. Load FAQ questions and answers from `faqs.json`.
2. Normalize/tokenize text using a simple regex tokenizer.
3. Convert questions to TF-IDF vectors.
4. Convert the user's question to the same vector space.
5. Calculate cosine similarity.
6. Return the most similar FAQ answer when the score passes the confidence threshold.

## Run

```bash
streamlit run app.py
```

You can edit `faqs.json` to change the topic/product.
