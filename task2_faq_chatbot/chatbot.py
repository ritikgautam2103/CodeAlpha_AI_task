import json
import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE = Path(__file__).resolve().parent

def tokenize_and_clean(text: str) -> str:
    # Lightweight NLP preprocessing: lowercase + tokenization + punctuation removal.
    tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
    return " ".join(tokens)

class FAQChatbot:
    def __init__(self, faq_file=BASE / "faqs.json", threshold=0.20):
        with open(faq_file, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)

        self.questions = [item["question"] for item in self.faqs]
        self.answers = [item["answer"] for item in self.faqs]
        self.vectorizer = TfidfVectorizer(
            preprocessor=tokenize_and_clean,
            token_pattern=r"(?u)\b\w+\b",
            ngram_range=(1, 2),
        )
        self.matrix = self.vectorizer.fit_transform(self.questions)
        self.threshold = threshold

    def answer(self, user_question: str):
        if not user_question.strip():
            return "Please type a question.", 0.0, None

        query_vector = self.vectorizer.transform([user_question])
        scores = cosine_similarity(query_vector, self.matrix)[0]
        best_index = int(scores.argmax())
        best_score = float(scores[best_index])

        if best_score < self.threshold:
            return (
                "I couldn't find a sufficiently similar FAQ. Please contact the "
                "support/college office for a specific answer.",
                best_score,
                None,
            )

        return self.answers[best_index], best_score, self.questions[best_index]
