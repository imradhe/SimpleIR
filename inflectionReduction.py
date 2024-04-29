from util import *


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
	def efficiency(self, num_sentences):
		results = {
			'stem_times': [],
			'lemmatize_times': [],
			'hybrid_times': []
		}
		for num in num_sentences:
			exec_time_stem = self.exec_time(num, "stem")
			exec_time_lemmatize = self.exec_time(num, "lemmatize")
			exec_time_hybrid = self.exec_time(num, "hybrid")
			results['stem_times'].append(exec_time_stem)
			results['lemmatize_times'].append(exec_time_lemmatize)
			results['hybrid_times'].append(exec_time_hybrid)
		return results


	def exec_time(self, num_sentences, approach = 'stem'):
		text = []
		for _ in range(num_sentences):
			num_tokens = random.randint(10 - 2, 10 + 2)  # Vary tokens per sentence
			sentence = [random.choice(string.ascii_lowercase) for _ in range(num_tokens)]
			text.append(sentence)
		startTime = time.time()
		self.reduce(text, approach)
		endTime = time.time()
		return endTime - startTime
	