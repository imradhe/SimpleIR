from util import *

class SentenceSegmentation():
    def segment(self, text, approach='naive'):
        """
        Sentence Segmentation

        Parameters
        ----------
        text : str
            A string containing one or more sentences.
        approach : str, optional
            The approach to use for sentence segmentation.
            Possible values are 'naive' (default) or 'punkt'.

        Returns
        -------
        list
            A list of strings where each string is a single sentence.
        """
        if approach == 'naive':
            return self.naive(text)
        elif approach == 'punkt':
            return self.punkt(text)
        else:
            raise ValueError("Invalid approach. Supported values are 'naive' and 'punkt'.")

    def naive(self, text):
        """
        Sentence Segmentation using a Naive Approach

        Parameters
        ----------
        text : str
            A string (a bunch of sentences)

        Returns
        -------
        list
            A list of strings where each string is a single sentence
        """

        punctuation_marks = ['.', '!', '?', ";", "\n"]

        brackets_and_quotes = ['"', "'", '(', ')', '[', ']', '{', '}']

        abbreviations = ['Ms.', 'Mr.', 'Dr.', 'Mrs.', 'Prof.', 'etc.', 'e.g.', 'i.e.']
        abbreviations = [abbr.lower() for abbr in abbreviations]

        segmented_text = []

        sentences = [sentence.strip() for sentence in text.split('\n') if sentence.strip()]

        for sentence in sentences:
            sentence_segment = ''
            is_abbreviation = False
            is_number = False
            inside_quotes_or_brackets = False

            for i, char in enumerate(sentence):
                sentence_segment += char

                if i < len(sentence) - 1 and sentence[i+1].isdigit():
                    is_number = True
                else:
                    is_number = False

                if char in punctuation_marks and not inside_quotes_or_brackets and (i < len(sentence) - 1 and sentence[i+1] in [' '] + brackets_and_quotes):
                    preceding_word = sentence_segment.strip().split()[-1].lower()
                    if preceding_word in abbreviations or is_number:
                        is_abbreviation = True
                    else:
                        segmented_text.append(sentence_segment.strip())
                        sentence_segment = ''
                        is_abbreviation = False

            if sentence_segment:
                segmented_text.append(sentence_segment.strip())

        return segmented_text

    def punkt(self, text):
        """
        Sentence Segmentation using the Punkt Tokenizer

        Parameters
        ----------
        text : str
            A string (a bunch of sentences)

        Returns
        -------
        list
            A list of strings where each string is a single sentence
        """

        segmented_text = sent_tokenize(text)

        return segmented_text

    def effectiveness(self, test_cases):
        results = []
        total_weight = 0

        for case in test_cases:
            input_text = case['input_text']
            expected = case['expected']
            weight = case.get('weight', 1)  # Default weight is 1 if not provided

            total_weight += weight

            naive_output = self.segment(input_text, 'naive')
            punkt_output = self.segment(input_text, 'punkt')

            naive_passed = naive_output == expected
            punkt_passed = punkt_output == expected

            results.append({
                'input_text': input_text,
                'expected': expected,
                'naive_output': naive_output,
                'naive_passed': naive_passed,
                'punkt_output': punkt_output,
                'punkt_passed': punkt_passed,
                'weight': weight
            })

        naive_metrics = calculate_metrics(results, 'naive')
        punkt_metrics = calculate_metrics(results, 'punkt')

        return {
            'results': results,
            'naive': naive_metrics,
            'punkt': punkt_metrics,
            'total_weight': total_weight
        }
       
    def efficiency(self, input_sizes):
        naive_times = []
        punkt_times = []

        for size in input_sizes:
            input_text = ' '.join(['sentence.' for _ in range(size)])  # Generating input text of given size

            start_time = time.time()
            for _ in range(10):  # Repeat 10 times to get average time
                self.segment(input_text, 'naive')
            end_time = time.time()
            naive_times.append((end_time - start_time) / 10)

            start_time = time.time()
            for _ in range(10):  # Repeat 10 times to get average time
                self.segment(input_text, 'punkt')
            end_time = time.time()
            punkt_times.append((end_time - start_time) / 10)

        return naive_times, punkt_times
    
