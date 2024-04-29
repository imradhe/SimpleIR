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

        naive_metrics = calculate_metrics(results, 'naive')
        pennTreeBank_metrics = calculate_metrics(results, 'pennTreeBank')

        return {
            'results': results,
            'naive': naive_metrics,
            'pennTreeBank': pennTreeBank_metrics,
            'total_weight': total_weight
        }
    

    def efficiency(self, num_sentences, words_per_sentence):
        """
        Measure the running time of the tokenization methods for different input sizes

        Parameters
        ----------
        num_sentences : int
            The number of sentences to generate
        words_per_sentence : int
            The number of words in each sentence

        Returns
        -------
        dict
            A dictionary containing the running times for each tokenization method
        """
        # Generate random text
        random_text = []
        for _ in range(num_sentences):
            sentence = ' '.join(''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, words_per_sentence))) for _ in range(words_per_sentence))
            random_text.append(sentence)

        # Measure running time for naive tokenization
        start_time = time.time()
        self.tokenize(random_text, 'naive')
        naive_time = time.time() - start_time

        # Measure running time for Penn Treebank tokenization
        start_time = time.time()
        self.tokenize(random_text, 'pennTreeBank')
        pennTreeBank_time = time.time() - start_time

        return {
            'naive': naive_time,
            'pennTreeBank': pennTreeBank_time,
            'num_sentences': num_sentences,
            'words_per_sentence': words_per_sentence
        }
