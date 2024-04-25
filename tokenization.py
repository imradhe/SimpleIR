from util import *

class Tokenization():
    
    def tokenize(self, text, method='naive'):
        """
        Tokenization using the specified method

        Parameters
        ----------
        text : list
            A list of strings where each string is a single sentence
        method : str
            The tokenization method to use. Options are 'naive' and 'pennTreeBank'

        Returns
        -------
        list
            A list of lists where each sub-list is a sequence of tokens
        """
        if method == 'naive':
            return self.naive(text)
        elif method == 'pennTreeBank':
            return self.pennTreeBank(text)
        else:
            raise ValueError('Invalid tokenization method')

    def naive(self, text):
        """
        Tokenization using a Naive Approach

        Parameters
        ----------
        text : list
            A list of strings where each string is a single sentence

        Returns
        -------
        list
            A list of lists where each sub-list is a sequence of tokens
        """
        tokenizedText = []
        for sentence in text:
            tokens = []
            current_token = ''
            for word in sentence.split(" "):  # Split each sentence with space
                for char in word:
                    if char.isalnum() or char == '\'':
                        current_token += char
                    elif char == '.':
                        # Check if the current token is a decimal number
                        if re.match(r'^\d+(\.\d+)?$', current_token):
                            current_token += char
                        else:
                            if current_token:
                                tokens.append(current_token)
                                current_token = ''
                            tokens.append(char)
                    else:
                        if current_token:
                            tokens.append(current_token)
                            current_token = ''
                        tokens.append(char)
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
            tokenizedText.append(tokens)
        return tokenizedText

    def pennTreeBank(self, text):
        """
        Tokenization using the Penn Tree Bank Tokenizer

        Parameters
        ----------
        text : list
            A list of strings where each string is a single sentence

        Returns
        -------
        list
            A list of lists where each sub-list is a sequence of tokens
        """
        tokenizedText = []
        tokenizer = nltk.tokenize.TreebankWordTokenizer()
        for sentence in text:
            tokens = tokenizer.tokenize(sentence)
            tokenizedText.append(tokens)
            
        return tokenizedText
        
    def effectiveness(self, test_cases):
        results = []
        total_weight = 0

        for case in test_cases:
            input_text = case['input_text']
            expected = case['expected']
            weight = case.get('weight', 1)  # Default weight is 1 if not provided

            total_weight += weight

            naive_output = self.tokenize(input_text, 'naive')
            pennTreeBank_output = self.tokenize(input_text, 'pennTreeBank')

            naive_passed = naive_output == expected
            pennTreeBank_passed = pennTreeBank_output == expected

            results.append({
                'input_text': input_text,
                'expected': expected,
                'naive_output': naive_output,
                'naive_passed': naive_passed,
                'pennTreeBank_output': pennTreeBank_output,
                'pennTreeBank_passed': pennTreeBank_passed,
                'weight': weight
            })

        weighted_naive_true_positives = sum(case['weight'] for case in results if case['naive_passed'])
        weighted_naive_false_positives = sum(case['weight'] for case in results if not case['naive_passed'] and case['naive_output'])
        weighted_naive_false_negatives = sum(case['weight'] * len(case['expected']) for case in results if not case['naive_passed'])
        weighted_pennTreeBank_true_positives = sum(case['weight'] for case in results if case['pennTreeBank_passed'])
        weighted_pennTreeBank_false_positives = sum(case['weight'] for case in results if not case['pennTreeBank_passed'] and case['pennTreeBank_output'])
        weighted_pennTreeBank_false_negatives = sum(case['weight'] * len(case['expected']) for case in results if not case['pennTreeBank_passed'])

        weighted_naive_precision = weighted_naive_true_positives / (weighted_naive_true_positives + weighted_naive_false_positives) if weighted_naive_true_positives + weighted_naive_false_positives > 0 else 0
        weighted_naive_recall = weighted_naive_true_positives / (weighted_naive_true_positives + weighted_naive_false_negatives) if weighted_naive_true_positives + weighted_naive_false_negatives > 0 else 0
        weighted_naive_f1_score = 2 * (weighted_naive_precision * weighted_naive_recall) / (weighted_naive_precision + weighted_naive_recall) if weighted_naive_precision + weighted_naive_recall > 0 else 0

        weighted_pennTreeBank_precision = weighted_pennTreeBank_true_positives / (weighted_pennTreeBank_true_positives + weighted_pennTreeBank_false_positives) if weighted_pennTreeBank_true_positives + weighted_pennTreeBank_false_positives > 0 else 0
        weighted_pennTreeBank_recall = weighted_pennTreeBank_true_positives / (weighted_pennTreeBank_true_positives + weighted_pennTreeBank_false_negatives) if weighted_pennTreeBank_true_positives + weighted_pennTreeBank_false_negatives > 0 else 0
        weighted_pennTreeBank_f1_score = 2 * (weighted_pennTreeBank_precision * weighted_pennTreeBank_recall) / (weighted_pennTreeBank_precision + weighted_pennTreeBank_recall) if weighted_pennTreeBank_precision + weighted_pennTreeBank_recall > 0 else 0

        return {
            'results': results,
            'naive': {'precision': weighted_naive_precision, 'recall': weighted_naive_recall, 'f1_score': weighted_naive_f1_score},
            'pennTreeBank': {'precision': weighted_pennTreeBank_precision, 'recall': weighted_pennTreeBank_recall, 'f1_score': weighted_pennTreeBank_f1_score},
            'total_weight': total_weight
        }
    
    def efficiency(self, input_sizes, num_sentences=10, words_per_sentence=10):
        naive_times = []
        pennTreeBank_times = []

        for size in input_sizes:
            input_text = [' '.join(['word' for _ in range(words_per_sentence)]) for _ in range(num_sentences)]

            start_time = time.time()
            for _ in range(10):  # Repeat 10 times to get average time
                self.tokenize(input_text, 'naive')
            end_time = time.time()
            naive_times.append((end_time - start_time) / 10)

            start_time = time.time()
            for _ in range(10):  # Repeat 10 times to get average time
                self.tokenize(input_text, 'pennTreeBank')
            end_time = time.time()
            pennTreeBank_times.append((end_time - start_time) / 10)

        return naive_times, pennTreeBank_times


