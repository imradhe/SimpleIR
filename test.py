from util import *
from spacyPreprocessor import SpacyPreprocessor
class SpacyIR:
    def __init__(self, documents_path, queries_path, output_dir):
        self.documents_path = documents_path
        self.queries_path = queries_path
        self.output_dir = output_dir
        self.documents = None
        self.reduced = None
        self.queries = None
        self.frequencies = None
        self.reduced = None
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

    def load_documents(self):
        with open(self.documents_path) as f:
            self.documents = json.load(f)

    def load_queries(self):
        with open(self.queries_path) as f:
            self.queries = json.load(f)
    
    def load_frequencies(self):        
        preprocessor = SpacyPreprocessor(self.documents_path, self.queries_path, self.output_dir)
        self.documents = preprocessor.load_detokenized_docs()
        self.reduced = preprocessor.load_reduced_docs()
        # Build token document matrix
        if os.path.exists(os.path.join(self.output_dir, 'frequencies.json')):
            frequencies_path = os.path.join(self.output_dir, 'frequencies.json')
            with open(frequencies_path) as f:
                self.frequencies = json.load(f)
        else:
            docs = [[token.lower() for sentence in doc['body'] for token in sentence] for doc in self.reduced]
            self.frequencies = {}
            for doc in tqdm(docs, "Indexing documents (token-document frequency)"):
                for token in doc:
                    if token not in self.frequencies:
                        self.frequencies[token] = []
                        for i in docs:
                                self.frequencies[token].append(i.count(token))
                                                
            # Store token document matrix
            output_file = os.path.join(self.output_dir, 'frequencies.json')
            with open(output_file, 'w') as f:
                json.dump(self.frequencies, f, indent=4)
        return self.frequencies

    def load_similarities(self):
        if os.path.exists(os.path.join(self.output_dir, 'similarities.json')):
            similarities_path = os.path.join(self.output_dir, 'similarities.json')
            with open(similarities_path) as f:
                self.similarities = json.load(f)
        else:
            self.similarities = {}
            docs = [[token for sentence in doc['body'] for token in sentence] for doc in self.reduced]
            for token in tqdm(self.frequencies, "Indexing documents (token-document similarity)"):
                if token not in self.similarities:
                    self.similarities[token] = []
                for i in tqdm(range(len(docs)), "Calculating similarities"):
                    doc_similarity = 0
                    for doc_token in docs[i]:
                        doc_similarity += (self.frequencies.get(token)[i] + 0.1) * self.nlp(token).similarity(self.nlp(doc_token))
                    self.similarities[token].append(doc_similarity/len(docs[i]))

                # Store token document matrix for similarities
                output_file = os.path.join(self.output_dir, 'similarities.json')
                with open(output_file, 'w') as f:
                    json.dump(self.similarities, f, indent=4)
        return self.similarities
    
    def query_doc_similarity(self, query):
        self.preprocessor = SpacyPreprocessor(self.documents_path, self.queries_path, self.output_dir)
        query = self.preprocessor.process(query)
        queryTokens = query['reducedTokens']
        tokens = [token.lower() for sentence in queryTokens for token in sentence]
        similarities = []
        for token in tokens:
            if token in self.similarities:
                similarities.append(self.similarities.get(token))
            elif token in self.frequencies:
                similarities.append(self.frequencies.get(token))
            else:
                similarities = []
                for doc in self.documents:
                    similarity = self.nlp(token).similarity(self.nlp(doc['body']))
                    similarities.append(similarity)

        return [sum(sim) for sim in zip(*similarities)]

        
        
    

    def retrieve(self, query):
        similarity_scores = self.query_doc_similarity(query)
        sorted_results = sorted(enumerate(similarity_scores), key=lambda x: x[1], reverse=True)
        return sorted_results
    


# Example usage:
documents_path = 'cranfield/test_docs.json'
queries_path = 'cranfield/cran_queries.json'
output_dir = 'trails/'

ir_system = SpacyIR(documents_path, queries_path, output_dir)

ir_system.load_frequencies()
ir_system.load_similarities()

query = "italy"
for doc_index, score in ir_system.retrieve(query):
    print(ir_system.documents[doc_index])