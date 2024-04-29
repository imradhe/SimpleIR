import sys
sys.path.append('.')
from util import *
from sentenceSegmentation import SentenceSegmentation


test_cases = [
    # Simple text with common punctuation
    {
        'input_text': "This is a simple sentence. Another sentence follows!",
        'expected': ["This is a simple sentence.", "Another sentence follows!"],
        'weight': 1
    },
    # Text with abbreviations and nested quotes
    {
        'input_text': "Dr. Smith said, 'Hello, Mr. Jones.' Is that correct?",
        'expected': ["Dr. Smith said, 'Hello, Mr. Jones.'", "Is that correct?"],
        'weight': 1
    },
    # Edge case: empty input
    {
        'input_text': "",
        'expected': [],
        'weight': 0.6
    },
    # Edge case: input with only punctuation
    {
        'input_text': "?!;:",
        'expected': ["?!;:"],
        'weight': 0.5
    },
    # Edge case: single word input
    {
        'input_text': "Hello",
        'expected': ["Hello"],
        'weight': 1
    },
    # Text with special characters
    {
        'input_text': "Sentence 1 ends with '.', Sentence 2 ends with '?', Sentence 3 ends with '!'",
        'expected': ["Sentence 1 ends with '.', Sentence 2 ends with '?', Sentence 3 ends with '!'"],
        'weight': 0.6
    },
    # Text with numbers
    {
        'input_text': "1. First point. 2. Second point. 3. Third point.",
        'expected': ["1. First point.", "2. Second point.", "3. Third point."],
        'weight': 0.8
    },
    # Text with ellipsis
    {
        'input_text': "This is a sentence... And here's another...",
        'expected': ["This is a sentence...", "And here's another..."],
        'weight': 0.8
    },
    # Text with parentheses and brackets
    {
        'input_text': "This (is) a [test].",
        'expected': ["This (is) a [test]."],
        'weight': 0.7
    },
    # Text with quotations
    {
        'input_text': '"This is a quote," he said.',
        'expected': ['"This is a quote," he said.'],
        'weight': 0.8
    },
    # Text with multiple exceptions
    {
        'input_text': "We'll meet at 6 p.m. at 123 Main St. (across the street).",
        'expected': ["We'll meet at 6 p.m. at 123 Main St. (across the street)."],
        'weight': 0.7
    },
    # Text with multiple exceptions and nested quotes
    {
        'input_text': "She said, 'I'm going to the store (I need eggs).'",
        'expected': ["She said, 'I'm going to the store (I need eggs).'"],
        'weight': 0.9
    },
    # Text with emoticons
    {
        'input_text': "I'm happy :) but she's sad :(.",
        'expected': ["I'm happy :)", "but she's sad :("],
        'weight': 0.5
    },
    # Text with URLs and email addresses
    {
        'input_text': "Visit us at www.example.com or email us at info@example.com.",
        'expected': ["Visit us at www.example.com or email us at info@example.com."],
        'weight': 0.8
    },
    # Text with hyphenated words
    {
        'input_text': "High-level programming is fun.",
        'expected': ["High-level programming is fun."],
        'weight': 1
    },
    # Text with mixed punctuation
    {
        'input_text': "This text ends with an exclamation mark! And this one with a period.",
        'expected': ["This text ends with an exclamation mark!", "And this one with a period."],
        'weight': 0.8
    },
    # Text with multiple spaces
    {
        'input_text': "   This   has   multiple   spaces   between   words.   ",
        'expected': ["   This   has   multiple   spaces   between   words.   "],
        'weight': 0.6
    },
    # Text with mixed case
    {
        'input_text': "This is a SENTENCE in mixed CASE.",
        'expected': ["This is a SENTENCE in mixed CASE."],
        'weight': 0.7
    },
    # Text with newline characters
    {
        'input_text': "This sentence\nspans multiple\nlines.",
        'expected': ["This sentence", "spans multiple", "lines."],
        'weight': 0.9
    },
    # Text with decimal numbers
    {
        'input_text': "This sentence with decimal numbers: 3.14, 2.71828, 1.61803398875. This is another sentence with decimal numbers: 6.12, 33.21, 433.132",
        'expected': ["This sentence with decimal numbers: 3.14, 2.71828, 1.61803398875.", "This is another sentence with decimal numbers: 6.12, 33.21, 433.132",],
        'weight': 1
    },
    # Text with mathematical expressions
    {
        'input_text': "The equation for the area of a circle is: A = π * r^2, where r is the radius.",
        'expected': ["The equation for the area of a circle is: A = π * r^2, where r is the radius."],
        'weight': 0.7
    },
    # Text with code snippets
    {
        'input_text': "To print 'Hello, World!' in Python, you can use: print('Hello, World!')",
        'expected': ["To print 'Hello, World!' in Python, you can use: print('Hello, World!')"],
        'weight': 0.8
    },
    # Text with chemical formulas
    {
        'input_text': "The chemical formula for water is H2O. The formula for carbon dioxide is CO2.",
        'expected': ["The chemical formula for water is H2O.", "The formula for carbon dioxide is CO2."],
        'weight': 0.6
    },
    # Text with long sentences
    {
        'input_text': "This is a very long sentence with multiple clauses and phrases, and it is meant to test the ability of the sentence segmentation algorithms to handle long and complex sentences, as well as to ensure that they do not incorrectly split the sentence into multiple parts, which could potentially lead to incorrect or incomplete information being extracted or processed.",
        'expected': ["This is a very long sentence with multiple clauses and phrases, and it is meant to test the ability of the sentence segmentation algorithms to handle long and complex sentences, as well as to ensure that they do not incorrectly split the sentence into multiple parts, which could potentially lead to incorrect or incomplete information being extracted or processed."],
        'weight': 0.9
    },
    # Text with mixed languages and scripts
    {
        'input_text': "Hola, ¿cómo estás? Hello, how are you? नमस्ते, आप कैसे हैं?",
        'expected': ["Hola, ¿cómo estás?", "Hello, how are you?", "नमस्ते, आप कैसे हैं?"],
        'weight': 0.8
    },
    # Text with XML/HTML tags
    {
        'input_text': "This is a <bold>bold</bold> text. <p>This is a new paragraph.</p>",
        'expected': ["This is a <bold>bold</bold> text.", "<p>This is a new paragraph.</p>"],
        'weight': 0.7
    },
    # Text with emoji
    {
        'input_text': "I'm feeling great today! 😊 Let's celebrate! 🎉",
        'expected': ["I'm feeling great today! 😊", "Let's celebrate! 🎉"],
        'weight': 0.5
    },
    # Text with contractions
    {
        'input_text': "She's going to the store. He'll be there soon.",
        'expected': ["She's going to the store.", "He'll be there soon."],
        'weight': 0.8
    },
    # Text with possessives
    {
        'input_text': "This is John's book. That is Mary's pen.",
        'expected': ["This is John's book.", "That is Mary's pen."],
        'weight': 0.8
    },
    # Text with abbreviations
    {
        'input_text': "We live on Main St. He works at the U.S. Dept. of Defense.",
        'expected': ["We live on Main St.", "He works at the U.S. Dept. of Defense."],
        'weight': 0.9
    },
    # Text with dates
    {
        'input_text': "The meeting is scheduled for June 15th, 2023. The deadline is 31/12/2023.",
        'expected': ["The meeting is scheduled for June 15th, 2023.", "The deadline is 31/12/2023."],
        'weight': 0.7
    },
    # Text with currency
    {
        'input_text': "The book costs $19.99. The shirt is €29.95.",
        'expected': ["The book costs $19.99.", "The shirt is €29.95."],
        'weight': 0.8
    },
    # Text with fractions
    {
        'input_text': "I ate 3/4 of the pizza. She drank 1/2 of the milk.",
        'expected': ["I ate 3/4 of the pizza.", "She drank 1/2 of the milk."],
        'weight': 0.7
    },
    # Text with measurements
    {
        'input_text': "The room is 10 meters long. The temperature is 25°C.",
        'expected': ["The room is 10 meters long.", "The temperature is 25°C."],
        'weight': 0.6
    },
    # Add more test cases as needed
]

# Define directories
directories = ['tests/effectiveness', 'tests/efficiency', 'tests/hypothesis']

# Create directories if they don't exist
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Create an instance of the SentenceSegmentation class
sentence_segmentation = SentenceSegmentation()

# Run the effectiveness test
effectiveness_metrics = sentence_segmentation.effectiveness(test_cases)

# Save test cases and effectiveness metrics
with open('tests/effectiveness/sentenceSegmentation.txt', 'w', encoding='utf-8') as file:
    # Write precision, recall, and F1 scores for both approaches
    file.write(f"Naive: Precision - {effectiveness_metrics['naive']['precision']}, Recall - {effectiveness_metrics['naive']['recall']}, F1 Score - {effectiveness_metrics['naive']['f1_score']}\n")
    file.write(f"Punkt: Precision - {effectiveness_metrics['punkt']['precision']}, Recall - {effectiveness_metrics['punkt']['recall']}, F1 Score - {effectiveness_metrics['punkt']['f1_score']}\n\n")
    for case in effectiveness_metrics['results']:
        file.write(f"Input Text: {case['input_text']}\n")
        file.write(f"Expected: {case['expected']}\n")
        file.write(f"Naive Output: {case['naive_output']}\n")
        file.write(f"Naive Passed: {case['naive_passed']}\n")
        file.write(f"Punkt Output: {case['punkt_output']}\n")
        file.write(f"Punkt Passed: {case['punkt_passed']}\n\n")


# Print effectiveness metrics
print(f"Naive: Precision - {effectiveness_metrics['naive']['precision']}, Recall - {effectiveness_metrics['naive']['recall']}, F1 Score - {effectiveness_metrics['naive']['f1_score']}")
print(f"Punkt: Precision - {effectiveness_metrics['punkt']['precision']}, Recall - {effectiveness_metrics['punkt']['recall']}, F1 Score - {effectiveness_metrics['punkt']['f1_score']}")


sentence_segmentation = SentenceSegmentation()
input_sizes = [100, 1000, 10000, 100000]  # input sizes

naive_times, punkt_times = sentence_segmentation.efficiency(input_sizes)

# Save test cases and efficiency metrics as a text file
with open('tests/efficiency/sentenceSegmentation.txt', 'w', encoding='utf-8') as file:
    for i in range(len(input_sizes)):
        file.write(f"Input Size: {input_sizes[i]}\n")
        file.write(f"Naive Approach Time: {naive_times[i]}\n")
        file.write(f"Punkt Approach Time: {punkt_times[i]}\n\n")


alpha = 0.5
# Save and print hypothesis testing results
with open('tests/hypothesis/sentenceSegmentation.txt', 'w', encoding='utf-8') as file:

    # Precision scores for the Naive approach and the Punkt tokenizer
    naive_precision_scores = [case['weight'] * effectiveness_metrics['naive']['precision'] for case in test_cases if 'weight' in case]
    punkt_precision_scores = [case['weight'] * effectiveness_metrics['punkt']['precision'] for case in test_cases if 'weight' in case]

    # Perform a two-sided t-test for the null hypothesis that the means of the two approaches are equal
    t_statistic_precision, p_value_precision = stats.ttest_rel(naive_precision_scores, punkt_precision_scores, nan_policy='omit')
    # Write the results of the hypothesis test
    file.write("T-statistic for precision scores: {}\n".format(t_statistic_precision))
    file.write("P-value for precision scores: {}\n\n".format(p_value_precision))
    if p_value_precision < alpha:
        file.write("Reject the null hypothesis. There is a significant difference between the precision scores of the two approaches.\n")
    else:
        file.write("Fail to reject the null hypothesis. There is no significant difference between the precision scores of the two approaches.\n")

    # Compare p-value to alpha
    if p_value_precision < alpha:
        print("Reject the null hypothesis.")
        if t_statistic_precision > 0:
            file.write("Approach 'Naive' performs better than approach 'Punkt'.")
        else:
            file.write("Approach 'Punkt' performs better than approach 'Naive'.")
    else:
        file.write("Fail to reject the null hypothesis. There is no significant difference in effectiveness between the two approaches.")


# Print hypothesis testing results
print("Hypothesis Testing Results:")
with open('tests/hypothesis/sentenceSegmentation.txt', 'r', encoding='utf-8') as file:
    print(file.read())