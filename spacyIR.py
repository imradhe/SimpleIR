from util import *
from spacyPreprocessor import SpacyPreprocessor
class SpacyIR:
    def __init__(self, documents_path, queries_path, output_dir):
        self.documents_path = documents_path
        self.queries_path = queries_path
        self.output_dir = output_dir
        self.documents = None
        self.queries = None
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
    
    def index(self, documents_path, output_dir):
        pass

    def calculate_similarity(self, query):
        similarities = []
        preprocessor = SpacyPreprocessor(self.documents_path, self.queries_path, self.output_dir)
        query_vector = preprocessor.process(query)['processedText']
        print(query_vector)
        for doc in tqdm(self.documents, "Retrieving documents"):
            doc_vector = self.nlp(doc['body'])
            similarity = query_vector.similarity(doc_vector)
            similarities.append({'id': doc['id'], 'similarity': similarity})
        return similarities

    def retrieve(self, query):        
        preprocessor = SpacyPreprocessor(self.documents_path, self.queries_path, self.output_dir)
        self.documents = preprocessor.load_detokenized_docs()
        query_results = self.calculate_similarity(query)
        query_results_sorted = sorted(query_results, key=lambda x: x['similarity'], reverse=True)
        output_file = os.path.join(self.output_dir, 'query_results.json')
        with open(output_file, 'w') as f:
            json.dump(query_results_sorted, f, indent=4)
        return query_results_sorted
    
    def run_queries(self):
        query_results = {}
        for query in tqdm(self.queries, "Running queries"):
            query_results[query['query number']] = self.retrieve(query['query'])
        output_file = os.path.join(self.output_dir, 'queries_results.json')
        with open(output_file, 'w') as f:
            json.dump(query_results, f, indent=4)
        return query_results


# Example usage:
documents_path = 'cranfield/cran_docs.json'
queries_path = 'cranfield/cran_queries.json'
output_dir = 'trails/'

ir_system = SpacyIR(documents_path, queries_path, output_dir)

# Example retrieve method usage
ir_system.run_queries()