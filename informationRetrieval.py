from util import *

# Add your import statements here

from sklearn.feature_extraction.text import TfidfVectorizer

class InformationRetrieval:
    def __init__(self):
        self.index = None
        # Create a TfidfVectorizer instance
        self.vectorizer = TfidfVectorizer()

    def buildIndex(self, docs, docIDs):
        """
        Builds the document index in terms of the document
        IDs and stores it in the 'index' class variable

        Parameters
        ----------
        docs : list
            A list of lists of lists where each sub-list is
            a document and each sub-sub-list is a sentence of the document
        docIDs : list
            A list of integers denoting IDs of the documents
        Returns
        -------
        None
        """
        # Flatten the list of lists of lists into a list of strings
        documents = [' '.join([' '.join(sentence) for sentence in doc]) for doc in docs]
        
        
        # Compute TF-IDF scores for the documents
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        
        # Store the TF-IDF matrix and document IDs
        self.index = {
            'tfidf_matrix': tfidf_matrix,
            'docIDs': docIDs,
        }

    def rank(self, queries):
        """
        Rank the documents according to relevance for each query

        Parameters
        ----------
        queries : list
            A list of lists of lists where each sub-list is a query and
            each sub-sub-list is a sentence of the query
        

        Returns
        -------
        list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        """
        if self.index is None:
            raise ValueError("Index has not been built. Call buildIndex method first.")
        
        
        # Flatten the list of lists of lists into a list of strings
        query_strings = [' '.join([' '.join(sentence) for sentence in query]) for query in queries]
        
        # Compute TF-IDF scores for the queries
        query_tfidf = self.vectorizer.transform(query_strings)
        
        # Compute cosine similarity between query TF-IDF vectors and document TF-IDF vectors
        cosine_similarities = query_tfidf.dot(self.index['tfidf_matrix'].T)
        
        # Convert sparse matrix to dense array and then rank documents based on cosine similarities
        doc_indices_ordered = (-cosine_similarities.toarray()).argsort(axis=1)
        
        # Map document indices to document IDs
        docIDs = self.index['docIDs']
        doc_IDs_ordered = [[docIDs[idx] for idx in indices] for indices in doc_indices_ordered]
        
        return doc_IDs_ordered


# # Example Implementation

# # Sample documents
# docs = [
#     [["apple", "is", "a", "fruit"], ["banana", "is", "also", "a", "fruit"], ["apple", "is", "red"]],
#     [['apple', 'is', 'not', 'a', 'vegetable'], ["carrot", "is", "a", "vegetable"], ["potato", "is", "also", "a", "vegetable"]],
#     [["apple", "and", "banana", "are", "fruits"], ["carrot", "and", "potato", "are", "vegetables"], ['apple', 'is', 'also', 'green' 'in', 'some', 'cases']]
# ]

# # Corresponding document IDs
# docIDs = [1, 2, 3]

# # Sample queries
# queries = [
#     [["is", "apple", "fruit", "or", "vegetable", "?"]],
#     [["vegetable", "is", "good", "for", "health"]],
#     [["banana", "and", "potato"]],
#     [["which", "color", "is", "apple", "?"]]
# ]

# # Create an instance of InformationRetrieval
# ir_system = InformationRetrieval()

# # Build the index
# ir_system.buildIndex(docs, docIDs)

# # Rank documents for each query
# doc_IDs_ordered = ir_system.rank(queries)

# # Print the ranked document IDs for each query
# for i, query in enumerate(queries):
#     print(f"Query {i+1}: {query}")
#     print("Ranked Document IDs:", doc_IDs_ordered[i])
#     print()
