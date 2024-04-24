from util import *

# Add your import statements here
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')



class StopwordRemoval():
	def fromList(self, text):
		stopwordRemovedText = None
		"""
		Sentence Segmentation using the Punkt Tokenizer

		Parameters
		----------
		arg1 : list
			A list of lists where each sub-list is a sequence of tokens
			representing a sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of tokens
			representing a sentence with stopwords removed
		"""
		#Fill in code here
		stop_words = stopwords.words('english')
		stopwordRemovedText=[[word for word in sentence if word not in stop_words] for sentence in text]
		return stopwordRemovedText


# # Example usage
# stopword_remover = StopwordRemoval()
# tokenized_sentences = [["This", "is", "a", "sample", "sentence"], ["Another", "sample", "sentence"]]
# stopword_removed_sentences = stopword_remover.fromList(tokenized_sentences)
# print(stopword_removed_sentences)
