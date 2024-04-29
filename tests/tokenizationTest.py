import sys
sys.path.append('.')
from util import *
from tokenization import Tokenization


test_cases = [
    # Basic sentence
    {
        'input_text': ["This is sent1", "this is sent2"],
        'expected': [["This", "is", "sent1"], ["this", "is", "sent2"]],
        'weight': 1
    },

    # Sentence with punctuation
    {
        'input_text': ["Hello, world!"],
        'expected': [["Hello", ",", "world", "!",]],
        'weight': 1
    },

    # Sentence with numbers
    {
        'input_text': ["I have 2 apples and 5 oranges."],
        'expected': [["I", "have", "2", "apples", "and", "5", "oranges", "."]],
        'weight': 1
    },

    # Sentence with contractions
    {
        'input_text': ["I'm going to the store.", "He'll be back soon."],
        'expected': [["I", "'m", "going", "to", "the", "store", "."], ["He", "'ll", "be", "back", "soon", "."]],
        'weight': 0.8
    },

    # Sentence with possessive nouns
    {
        'input_text': ["John's car is red.", "The cat's toy is missing."],
        'expected': [["John", "'s", "car", "is", "red", "."], ["The", "cat", "'s", "toy", "is", "missing", "."]],
        'weight': 0.8
    },

    # Sentence with abbreviations
    {
        'input_text': ["I live in the U.S.A.", "She works at C.I.A."],
        'expected': [["I", "live", "in", "the", "U.S.A", "."], ["She", "works", "at", "C.I.A", "."]],
        'weight': 0.7
    },

    # Sentence with hyphenated words
    {
        'input_text': ["The man-made bridge is strong.", "We need to re-evaluate the plan."],
        'expected': [["The", "man-made", "bridge", "is", "strong", "."], ["We", "need", "to", "re-evaluate", "the", "plan", "."]],
        'weight': 0.8
    },

    # Sentence with URLs
    {
        'input_text': ["Visit https://www.example.com for more information."],
        'expected': [["Visit", "https://www.example.com", "for", "more", "information", "."]],
        'weight': 0.6
    },

    # Sentence with emojis
    {
        'input_text': ["I love pizza 🍕!", "That movie was 🔥."],
        'expected': [["I", "love", "pizza", "🍕", "!"], ["That", "movie", "was", "🔥", "."]],
        'weight': 0.5
    },

    # Empty string
    {
        'input_text': [""],
        'expected': [[]],
        'weight': 0.3
    },
 
    # Long sentence
    {
        'input_text': ["This is a very long sentence with multiple clauses, and it includes various punctuation marks, such as commas, semicolons; colons: and even parentheses (like this one)."],
        'expected': [["This", "is", "a", "very", "long", "sentence", "with", "multiple", "clauses", ",", "and", "it", "includes", "various", "punctuation", "marks", ",", "such", "as", "commas", ",", "semicolons", ";", "colons", ":", "and", "even", "parentheses", "(", "like", "this", "one", ")", "."]],
        'weight': 0.9
    },

    # Sentence with HTML tags
    {
        'input_text': ["<p>This is a <b>bold</b> sentence.</p>"],
        'expected': [["<p>", "This", "is", "a", "<b>", "bold", "</b>", "sentence", ".", "</p>"]],
        'weight': 0.4
    }
]

# Define directories
directories = ['tests/effectiveness', 'tests/efficiency', 'tests/hypothesis']

# Create directories if they don't exist
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Create an instance of the Tokenization class
tokenization = Tokenization()

# Run the effectiveness test
effectiveness_metrics = tokenization.effectiveness(test_cases)

# Save test cases and effectiveness metrics
with open('tests/effectiveness/tokenization.txt', 'w', encoding='utf-8') as file:
    # Write precision, recall, and F1 scores
    file.write(f"Naive: Precision - {effectiveness_metrics['naive']['precision']}, Recall - {effectiveness_metrics['naive']['recall']}, F1 Score - {effectiveness_metrics['naive']['f1_score']}\n")
    file.write(f"PennTreeBank: Precision - {effectiveness_metrics['pennTreeBank']['precision']}, Recall - {effectiveness_metrics['pennTreeBank']['recall']}, F1 Score - {effectiveness_metrics['pennTreeBank']['f1_score']}\n\n")
    for case in effectiveness_metrics['results']:
        file.write(f"Input Text: {case['input_text']}\n")
        file.write(f"Expected: {case['expected']}\n")
        file.write(f"Naive Output: {case['naive_output']}\n")
        file.write(f"Naive Passed: {case['naive_passed']}\n")
        file.write(f"PennTreeBank Output: {case['pennTreeBank_output']}\n")
        file.write(f"PennTreeBank Passed: {case['pennTreeBank_passed']}\n\n")


# Print effectiveness metrics
print(f"Naive: Precision - {effectiveness_metrics['naive']['precision']}, Recall - {effectiveness_metrics['naive']['recall']}, F1 Score - {effectiveness_metrics['naive']['f1_score']}")
print(f"PennTreeBank: Precision - {effectiveness_metrics['pennTreeBank']['precision']}, Recall - {effectiveness_metrics['pennTreeBank']['recall']}, F1 Score - {effectiveness_metrics['pennTreeBank']['f1_score']}")

# Efficiency testing
input_sizes = [100, 1000, 10000, 100000]  # input sizes
naive_times, pennTreeBank_times = [], []

for num_sentences in input_sizes:
    words_per_sentence = 10
    efficiency_result = tokenization.efficiency(num_sentences, words_per_sentence)
    naive_times.append(efficiency_result['naive'])
    pennTreeBank_times.append(efficiency_result['pennTreeBank'])

# Save test cases and efficiency metrics
with open('tests/efficiency/tokenization.txt', 'w', encoding='utf-8') as file:
    for i in range(len(input_sizes)):
        file.write(f"Input Size: {input_sizes[i]}\n")
        file.write(f"Naive Approach Time: {naive_times[i]}\n")
        file.write(f"PennTreeBank Approach Time: {pennTreeBank_times[i]}\n\n")
# Hypothesis testing
alpha = 0.5
with open('tests/hypothesis/tokenization.txt', 'w', encoding='utf-8') as file:

    # Precision scores for the Naive approach and the Penn Tree Bank tokenizer
    naive_precision_scores = [case['weight'] * effectiveness_metrics['naive']['precision'] for case in test_cases if 'weight' in case]
    pennTreeBank_precision_scores = [case['weight'] * effectiveness_metrics['pennTreeBank']['precision'] for case in test_cases if 'weight' in case]

    # Perform a two-sided t-test for the null hypothesis that the means of the two approaches are equal
    t_statistic_precision, p_value_precision = stats.ttest_rel(naive_precision_scores, pennTreeBank_precision_scores, nan_policy='omit')

    file.write("T-statistic for precision scores: {}\n".format(t_statistic_precision))
    file.write("P-value for precision scores: {}\n\n".format(p_value_precision))
    if p_value_precision < alpha:
        file.write("Reject the null hypothesis. There is a significant difference between the precision scores of the two approaches.\n")
    else:
        file.write("Fail to reject the null hypothesis. There is no significant difference between the precision scores of the two approaches.\n")
    # Compare p-value to alpha
    if t_statistic_precision > 0:
        file.write("Approach 'naive' performs better than approach 'pennTreeBank'.")
    else:
        file.write("Approach 'pennTreeBank' performs better than approach 'naive'.")



# Print hypothesis testing results
print("Hypothesis Testing Results:")
with open('tests/hypothesis/tokenization.txt', 'r', encoding='utf-8') as file:
    print(file.read())