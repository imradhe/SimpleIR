from util import *

# Add your import statements here


class InflectionReduction:
	def reduce(self, text, approach = "stem"):
		return self.stem(text) if approach == "stem" else self.lemmatize(text) if approach == "lemmatize" else self.hybrid(text)
	
	def stem(self, text):
		reducedText = None
		"""
		Stemming/Lemmatization

		Parameters
		----------
		arg1 : list
			A list of lists where each sub-list a sequence of tokens
			representing a sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of
			stemmed/lemmatized tokens representing a sentence
		"""
		#Fill in code here
		reducedText = [[PorterStemmer().stem(word) for word in sentence]for sentence in text]
		return reducedText
	
	def lemmatize(self, text):
		reducedText = None
		#Fill in code here
		reducedText= [[WordNetLemmatizer().lemmatize(word) for word in sentence]for sentence in text]
		return reducedText
	
	def hybrid(self, text):
		reducedText = None
		#Fill in code here
		reducedText= [[WordNetLemmatizer().lemmatize(word) for word in sentence]for sentence in text]
		reducedText= [[PorterStemmer().stem(word) for word in sentence]for sentence in reducedText]
		return reducedText
