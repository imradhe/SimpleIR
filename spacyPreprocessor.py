from util import *

class SpacyPreprocessor:
    def __init__(self, documents_path, queries_path, output_dir):
        self.documents_path = documents_path
        self.queries_path = queries_path
        self.output_dir = output_dir
        self.documents = None
        self.reduced = None
        self.queries = None
        self.nlp = spacy.load("en_core_web_md")

    def process(self, text):
        sentences = self.sentenceSegmentation(text)
        tokens = self.tokenization(text)
        stopwordsRemovedTokens = self.stopwordRemoval(tokens)
        reducedTokens = self.inflectionReduction(stopwordsRemovedTokens)
        processedText = self.detokenize(reducedTokens)
        return {'sentences': sentences, 'tokens' : tokens, 'stopwordRemovedTokens' : stopwordsRemovedTokens,  'reducedTokens' : reducedTokens, 'processedText' : self.nlp(processedText)}

    def sentenceSegmentation(self, text):
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        return sentences

    def tokenization(self, text):
        doc = self.nlp(text)
        tokens = [[token.text for token in sent] for sent in doc.sents]
        return tokens

    def stopwordRemoval(self, tokens):
        stopwords_removed_tokens = [[token for token in sent if not self.nlp.vocab[token].is_stop] for sent in tokens]
        return stopwords_removed_tokens

    def inflectionReduction(self, tokens):
        lemmas = [[token.lemma_ for token in self.nlp(" ".join(sent))] for sent in tokens]
        return lemmas
    
    def detokenize(self, tokens):
        sentences = [' '.join(sent) for sent in tokens]
        text = ' '.join(sentences)
        return text
    
    def calculate_similarity(self, input1, input2):
        doc1 = self.process(input1)
        doc2 = self.process(input2)
        similarity = doc1['processedText'].similarity(doc2['processedText'])

        return similarity
    
    def load_documents(self):
        with open(self.documents_path) as f:
            self.documents = json.load(f)

    def index(self):
        self.load_documents()
        segmented_docs = []
        tokenized_docs = []
        stopword_removed_docs = []
        reduced_docs = []
        detokenized_docs = []

        for doc in tqdm(self.documents, desc="Processing documents"):
            processed_doc = self.process(doc['body'])
            segmented_docs.append((doc['id'], processed_doc['sentences']))
            tokenized_docs.append((doc['id'], processed_doc['tokens']))
            stopword_removed_docs.append((doc['id'], processed_doc['stopwordRemovedTokens']))
            reduced_docs.append((doc['id'], processed_doc['reducedTokens']))
            detokenized_docs.append((doc['id'], processed_doc['processedText']))
        with open(self.output_dir + "spacy_segmented_docs.txt", "w") as f:
            for doc in tqdm(segmented_docs, desc="Indexing segmented docs"):
                f.write(f"Doc ID: {doc[0]}\n")
                f.write('\n'.join(doc[1]) + '\n')

        with open(self.output_dir + "spacy_tokenized_docs.txt", "w") as f:
            for doc in tqdm(tokenized_docs, desc="Indexing tokenized docs"):
                f.write(f"Doc ID: {doc[0]}\n")
                f.write('\n'.join([' '.join(sent) for sent in doc[1]]) + '\n')

        with open(self.output_dir + "spacy_stopword_removed_docs.txt", "w") as f:
            for doc in tqdm(stopword_removed_docs, desc="Indexing stopword removed docs"):
                f.write(f"Doc ID: {doc[0]}\n")
                f.write('\n'.join([' '.join(sent) for sent in doc[1]]) + '\n')

        reduced_docs_json = [{'id': doc[0], 'body': doc[1]} for doc in reduced_docs]
        with open(self.output_dir + "spacy_reduced_docs.json", "w") as f:
            f.write(json.dumps(reduced_docs_json, default=str))

        detokenized_docs_json = [{'id': doc[0], 'body': doc[1]} for doc in detokenized_docs]
        with open(self.output_dir + "spacy_detokenized_docs.json", "w") as f:
            f.write(json.dumps(detokenized_docs_json, default=str))
    
    def load_detokenized_docs(self):
        if self.documents is None:
            self.load_documents()

        detokenized_docs_path = self.output_dir + "spacy_detokenized_docs.json"
        if not os.path.exists(detokenized_docs_path):
            self.index()
            with open(detokenized_docs_path) as f:
                self.documents = json.load(f)
        else:
            with open(detokenized_docs_path) as f:
                self.documents = json.load(f)
        return self.documents

    def load_reduced_docs(self):
        if self.reduced is None:
            self.load_documents()

        reduced_docs_path = self.output_dir + "spacy_reduced_docs.json"
        if not os.path.exists(reduced_docs_path):
            self.index()
            with open(reduced_docs_path) as f:
                self.reduced = json.load(f)
        else:
            with open(reduced_docs_path) as f:
                self.reduced = json.load(f)
        return self.reduced