from util import *

# Add your import statements here




class InflectionReduction:
    def reduce(self, text):
        """
        Stemming/Lemmatization

        Parameters
        ----------
        text : list
            A list of lists where each sub-list is a sequence of tokens
            representing a sentence

        Returns
        -------
        list
            A list of lists where each sub-list is a sequence of
            stemmed/lemmatized tokens representing a sentence
        """
        reducedText = []

        lemmatizer = WordNetLemmatizer()
        stemmer = PorterStemmer()

        for sentence_tokens in text:
            # Lemmatize each token
            lemmatized_tokens = [lemmatizer.lemmatize(token) for token in sentence_tokens]
            # Stem each token
            stemmed_tokens = [stemmer.stem(token) for token in sentence_tokens]
            reducedText.append((lemmatized_tokens, stemmed_tokens))
            
        return reducedText

# # Example usage
# inflection_reducer = InflectionReduction()
# tokenized_sentences = [["running", "walked"], ["dogs", "cats"], ['singer', 'liar'], ['locating' , 'laying']]
# reduced_sentences = inflection_reducer.reduce(tokenized_sentences)
# print(reduced_sentences)