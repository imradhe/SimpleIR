from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Documents
documents = [
    "The quick brown fox jumps over the lazy dog.",
    "A stitch in time saves nine.",
    "All that glitters is not gold.",
    "Rome wasn't built in a day. it is a huge town",
    "Beauty is in the eye of the beholder.",
    "Actions speak louder than words.",
    "An apple a day keeps the doctor away.",
    "Birds of a feather flock together.",
    "Curiosity killed the cat.",
    "Don't count your chickens before they hatch."
]

# Query
query = "animal"

# Combine documents and query
documents.append(query)

# Calculate TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

# Calculate cosine similarity
cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
# Get indices of most similar documents
indices = cosine_similarities.argsort()[0][::-1]

print(cosine_similarities)
# Print most relevant documents
print("Most relevant documents for query '{}':".format(query))
for idx in indices:
    print("- Document {}: {}".format(idx+1, documents[idx]))
