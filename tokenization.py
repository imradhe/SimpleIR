from util import *

class Tokenization():
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
            for char in sentence:
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

# w