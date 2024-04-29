import os
import json
import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

class SpacyIR:
    def __init__(self, documents_path, queries_path, embeddings_path):
        self.documents_path = documents_path
        self.queries_path = queries_path
        self.embeddings_path = embeddings_path
        self.documents = None
        self.queries = None
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self.nlp = spacy.load("en_core_web_sm")
        self.word_embeddings = self.load_word_embeddings()

    def load_documents(self):
        with open(self.documents_path) as f:
            self.documents = json.load(f)

    def load_queries(self):
        with open(self.queries_path) as f:
            self.queries = json.load(f)

    def preprocess_documents(self):
        if self.documents is None:
            self.load_documents()
        return [doc["body"] for doc in self.documents]

    def preprocess_queries(self):
        if self.queries is None:
            self.load_queries()
        return [query["query"] for query in self.queries]

    def fit_tfidf_vectorizer(self):
        documents_text = self.preprocess_documents()
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(documents_text)

    def calculate_cosine_similarity(self, query_text):
        query_vector = self.tfidf_vectorizer.transform([query_text])
        cosine_similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        return cosine_similarities.argsort()[::-1]

    def get_word_embeddings(self, text):
        tokens = self.nlp(text)
        embeddings = []
        for token in tokens:
            if token.has_vector:
                embeddings.append((token.text, token.vector))
        return embeddings

    def load_word_embeddings(self):
        if os.path.exists(self.embeddings_path):
            return np.load(self.embeddings_path, allow_pickle=True).item()
        else:
            documents_text = ' '.join(self.preprocess_documents())
            chunk_size = 100000
            chunks = [documents_text[i:i+chunk_size] for i in range(0, len(documents_text), chunk_size)]

            word_embeddings = {}
            for chunk in tqdm(chunks, desc="Processing chunks for word embeddings"):
                for token, vector in self.get_word_embeddings(chunk):
                    if token not in word_embeddings:
                        word_embeddings[token] = vector

            os.makedirs(os.path.dirname(self.embeddings_path), exist_ok=True)
            np.save(self.embeddings_path, word_embeddings)
            print(f"Word embeddings for all unique tokens saved to {self.embeddings_path}")
            return word_embeddings

    def run_queries(self, output_file_path):
        if self.documents is None:
            self.load_documents()
        if self.queries is None:
            self.load_queries()
        if self.tfidf_matrix is None:
            self.fit_tfidf_vectorizer()

        query_results = {}
        for query_data in tqdm(self.queries, desc="Processing queries"):
            query_id = query_data["query number"]
            query_text = query_data["query"]
            doc_indices_sorted = self.calculate_cosine_similarity(query_text)
            all_documents = []
            for rank, doc_index in enumerate(doc_indices_sorted, start=1):
                document_id = self.documents[doc_index]["id"]
                document_score = cosine_similarity(self.tfidf_matrix[doc_index], self.tfidf_vectorizer.transform([query_text]))[0][0]
                all_documents.append({"document_id": document_id, "score": document_score, "rank": rank})
            query_results[query_id] = {"query": query_text, "results": all_documents}

        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, "w") as f:
            json.dump(query_results, f, indent=2)
        print(f"Query results saved to {output_file_path}")

# Example usage:
documents_path = 'cranfield/cran_docs.json'
queries_path = 'cranfield/cran_queries.json'
embeddings_path = 'output/word_embeddings.npy'
output_file_path = 'output/query_results.json'

ir_system = SpacyIR(documents_path, queries_path, embeddings_path)
ir_system.run_queries(output_file_path)