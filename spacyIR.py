import os
import json
import spacy
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

class SpacyIR:
    def __init__(self, documents_path, queries_path, output_dir):
        self.documents_path = documents_path
        self.queries_path = queries_path
        self.output_dir = output_dir
        self.documents = None
        self.queries = None
        self.word_embeddings = None
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self.cosine_similarities = None
        self.nlp = spacy.load("en_core_web_md")

        # Load or process data
        self.load_or_process_data()

    def load_or_process_data(self):
        # Check if output directory exists, create if not
        os.makedirs(self.output_dir, exist_ok=True)

        # Load or preprocess documents
        self.load_documents()

        # Load or preprocess queries
        self.load_queries()

        # Check if necessary files exist, else preprocess
        embeddings_path = os.path.join(self.output_dir, 'word_embeddings.npy')
        tfidf_matrix_path = os.path.join(self.output_dir, 'tfidf_matrix.npz')
        cosine_similarities_path = os.path.join(self.output_dir, 'cosine_similarities.npy')

        if os.path.exists(embeddings_path) and os.path.exists(tfidf_matrix_path) and os.path.exists(cosine_similarities_path):
            # Load word embeddings, TF-IDF matrix, and cosine similarities
            self.word_embeddings = np.load(embeddings_path, allow_pickle=True).item()
            self.tfidf_matrix = sparse.load_npz(tfidf_matrix_path)
            self.cosine_similarities = np.load(cosine_similarities_path)
        else:
            # Preprocess documents
            documents_text = self.preprocess_documents()

            # Extract word embeddings
            self.calculate_word_embeddings(documents_text)
            np.save(embeddings_path, self.word_embeddings)

            # Calculate TF-IDF matrix
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(documents_text)
            sparse.save_npz(tfidf_matrix_path, self.tfidf_matrix)

            # Calculate cosine similarities
            self.cosine_similarities = cosine_similarity(self.tfidf_matrix)
            np.save(cosine_similarities_path, self.cosine_similarities)

    def load_documents(self):
        with open(self.documents_path) as f:
            self.documents = json.load(f)

    def load_queries(self):
        with open(self.queries_path) as f:
            self.queries = json.load(f)

    def preprocess_documents(self):
        return [doc["body"] for doc in self.documents]

    def run_queries(self):
        query_results = {}
        # Check if TF-IDF vectorizer is fitted, if not, fit it
        if not self.tfidf_vectorizer.vocabulary:
            documents_text = self.preprocess_documents()
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(documents_text)
        for query_data in tqdm(self.queries, desc="Processing queries"):
            query_id = query_data["query number"]
            query_text = query_data["query"]
            query_vector = self.tfidf_vectorizer.transform([query_text])

            # Calculate cosine similarity for the query
            query_similarities = cosine_similarity(query_vector, self.tfidf_matrix)

            # Rank documents based on cosine similarity
            sorted_indices = np.argsort(query_similarities.flatten())[::-1]

            # Collect results
            results = []
            for rank, index in enumerate(sorted_indices, start=1):
                document_id = self.documents[index]["id"]
                score = query_similarities[0][index]
                results.append({"id": document_id, "score": score, "rank": rank})

            # Save query results
            query_results[query_id] = {"query": query_text, "results": results}

        # Save all query results in a single file
        output_file_path = os.path.join(self.output_dir, 'query_results.json')
        with open(output_file_path, "w") as output_file:
            json.dump(query_results, output_file, indent=2)


    def calculate_word_embeddings(self, documents_text):
        chunk_size = 100000  # Define the chunk size
        full_text = ' '.join(documents_text)
        tokens = []
        for chunk in tqdm(range(0, len(full_text), chunk_size), desc="Processing Documents"):
            chunk_text = full_text[chunk:chunk+chunk_size]
            chunk_tokens = self.nlp(chunk_text)
            tokens.extend(chunk_tokens)
        self.word_embeddings = {}
        for token in tokens:
            if token.has_vector:
                self.word_embeddings[token.text] = token.vector

    def process_single_query(self, query_text):
        # Check if TF-IDF vectorizer is fitted, if not, fit it
        if not self.tfidf_vectorizer.vocabulary:
            documents_text = self.preprocess_documents()
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(documents_text)

        # Transform the query text into a TF-IDF vector
        query_vector = self.tfidf_vectorizer.transform([query_text])

        # Calculate cosine similarity for the query
        query_similarities = cosine_similarity(query_vector, self.tfidf_matrix)

        # Rank documents based on cosine similarity
        sorted_indices = np.argsort(query_similarities.flatten())[::-1]

        # Collect results
        results = []
        for rank, index in enumerate(sorted_indices, start=1):
            document_id = self.documents[index]["id"]
            score = query_similarities[0][index]
            results.append({"id": document_id, "score": score, "rank": rank})

        # Save results to a file
        output_file_path = os.path.join(self.output_dir, 'custom_query.json')
        with open(output_file_path, "w") as output_file:
            json.dump(results, output_file, indent=2)

        return results

# Example usage:
documents_path = 'cranfield/cran_docs.json'
queries_path = 'cranfield/cran_queries.json'
output_dir = 'trails/'
ground_truth_file = 'cranfield/cran_qrels.json'

ir_system = SpacyIR(documents_path, queries_path, output_dir)
ir_system.run_queries()
