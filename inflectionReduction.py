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

	def effectiveness(self, test_cases):
		results = []
		total_weight = 0

		for case in test_cases:
			input_text = case['input_text']
			expected = case['expected']
			weight = case.get('weight', 1)  # Default weight is 1 if not provided

			total_weight += weight

			stem_output = self.reduce(input_text, 'stem')
			lemmatize_output = self.reduce(input_text, 'lemmatize')
			hybrid_output = self.reduce(input_text, 'hybrid')

			stem_passed = stem_output == expected
			lemmatize_passed = lemmatize_output == expected
			hybrid_passed = hybrid_output == expected

			results.append({
                'input_text': input_text,
                'expected': expected,
                'stem_output': stem_output,
                'stem_passed': stem_passed,
                'lemmatize_output': lemmatize_output,
                'lemmatize_passed': lemmatize_passed,
                'hybrid_output': hybrid_output,
                'hybrid_passed': hybrid_passed,
                'weight': weight
            })

		metrics = {
			'results': results,
            'stem': calculate_metrics(results, 'stem'),
            'lemmatize': calculate_metrics(results, 'lemmatize'),
            'hybrid': calculate_metrics(results, 'hybrid'),
            'total_weight': total_weight
        }

		return metrics

def calculate_metrics(results, approach):
    true_positives = sum(case['weight'] for case in results if case[f'{approach}_passed'])
    false_positives = sum(case['weight'] for case in results if not case[f'{approach}_passed'] and case[f'{approach}_output'])
    false_negatives = sum(case['weight'] * len(case['expected']) for case in results if not case[f'{approach}_passed'])
	


    precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    return {'precision': precision, 'recall': recall, 'f1_score': f1_score, 'true_positives': true_positives, 'false_positives': false_positives, 'false_negatives': false_negatives}