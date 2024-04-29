import numpy as np
import spacy
import json

# Load the English language model from spaCy
nlp = spacy.load("en_core_web_md")

# Opening JSON file
f = open('cranfield/cran_docs.json')

# returns JSON object as 
# a dictionary
data = json.load(f)

documents=[]
for i in range(len(data)):
    documents.append(data[i]["body"])

documents = documents[:10]

# documents = [
#     "The quick brown fox jumps over the lazy dog.",
#     "A stitch in time saves nine.",
#     "All that glitters is not gold.",
#     "Rome wasn't built in a day. it is a huge town",
#     "Beauty is in the eye of the beholder.",
#     "Actions speak louder than words.",
#     "An apple a day keeps the doctor away.",
#     "Birds of a feather flock together.",
#     "Curiosity killed the cat.",
#     "Don't count your chickens before they hatch."
# ]

# Query
query = "what problems of heat conduction in composite slabs have been solved so far ."

# Preprocess query and documents
query_tokens = nlp(query)
document_tokens = [nlp(doc) for doc in documents]

# Calculate word similarity matrix
word_similarity_matrix = np.zeros((len(document_tokens), len(query_tokens)))
for i, doc_tokens in enumerate(document_tokens):
    for j, query_token in enumerate(query_tokens):
        max_similarity = max([token.similarity(query_token) for token in doc_tokens])
        word_similarity_matrix[i, j] = max_similarity

# Calculate document scores
document_scores = np.mean(word_similarity_matrix, axis=1)
documents_with_scores = list(zip(documents, document_scores))
# Sort documents by relevance
sorted_indices = np.argsort(document_scores)[::-1]

# Retrieve relevant documents
relevant_documents = [documents_with_scores[idx] for idx in sorted_indices]

print("Relevant Documents:")
for idx, doc in enumerate(relevant_documents, start=1):
    print(f"doc: {doc[0][:20]}, score: {doc[1]}")

