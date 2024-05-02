from util import *

class lsaIR:
    def __init__(self, documents_path, queries_path, output_dir):
        self.documents_path = documents_path
        self.queries_path = queries_path
        self.output_dir = output_dir
        self.documents = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.lsa_model = None
        self.doc_vectors = None
        self.token_vectors = None

        # Load or process data
        self.load_or_process_data()

    def load_or_process_data(self):
        # Check if output directory exists, create if not
        os.makedirs(self.output_dir, exist_ok=True)

        # Load or preprocess documents
        self.load_documents()

        # Perform indexing using LSA
        self.index()

    def load_documents(self):
        with open(self.documents_path) as f:
            self.documents = json.load(f)

    def index(self):
        # Create TF-IDF matrix
        self.tfidf_vectorizer = TfidfVectorizer()
        corpus = [doc['body'] for doc in self.documents]
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus)

        # Perform SVD
        n_components = min(len(self.documents), self.tfidf_matrix.shape[1])
        svd_model = TruncatedSVD(n_components=n_components)
        self.lsa_model = svd_model.fit(self.tfidf_matrix)

        # Compute document vectors
        self.doc_vectors = self.lsa_model.transform(self.tfidf_matrix)

        # Compute token vectors
        tfidf_feature_names = self.tfidf_vectorizer.get_feature_names_out()
        self.token_vectors = self.lsa_model.components_.T

    def retrieve(self, query):
        # Convert query to TF-IDF vector
        query_vector = self.tfidf_vectorizer.transform([query])

        # Project query vector into LSA space
        query_lsa = self.lsa_model.transform(query_vector)

        # Compute cosine similarity between query and document vectors
        similarities = query_lsa @ self.doc_vectors.T

        # Sort documents by similarity score
        sorted_indices = (-similarities[0]).argsort()

        # Return ranked documents
        ranked_documents = [(self.documents[i], similarities[0][i]) for i in sorted_indices]
        return ranked_documents

# Example usage:
documents_path = 'cranfield/cran_docs.json'
queries_path = 'cranfield/cran_queries.json'
output_dir = 'trails/'
ir_system = lsaIR(documents_path, queries_path, output_dir)

# Retrieve documents for a query
query = "material properties of photoelastic materials ."
ranked_documents = ir_system.retrieve(query)

print("LSA Rankings")
for i, (doc, score) in enumerate(ranked_documents[:20]):
    print(f"Doc: {doc['id']}, Similarity Score: {score:.4f}")