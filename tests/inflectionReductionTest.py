import sys
sys.path.append('.')
from util import *
from inflectionReduction import InflectionReduction

test_cases = [
    {
        'input_text': [["cycling"]],
        'expected': [["cycle"]],
        'weight': 1,
        # Regular verb ending with 'ing'
    },
    {
        'input_text': [["bouncing"]],
        'expected': [["bounce"]],
        'weight': 1,
        # Another regular verb ending with 'ing'
    },
    {
        'input_text': [["running"]],
        'expected': [["run"]],
        'weight': 1,
        # A commonly mistaken case, where people may overlook irregularities and assume the regular inflection reduction
    },
    {
        'input_text': [["dying"]],
        'expected': [["die"]],
        'weight': 1,
        # Edge case: irregular verb ending with 'ing'
    },
    {
        'input_text': [["gently"]],
        'expected': [["gentle"]],
        'weight': 1,
        # Adverb ending with 'ly'
    },
    {
        'input_text': [["children"]],
        'expected': [["child"]],
        'weight': 1,
        # Exceptional case: plural noun with irregular singular form
    },
    {
        'input_text': [["happier"]],
        'expected': [["happy"]],
        'weight': 1,
        # Adjective with comparative inflection ending in 'er'
    },
    {
        'input_text': [["best"]],
        'expected': [["good"]],
        'weight': 1,
        # Superlative adjective
    },
    {
        'input_text': [["bigger"]],
        'expected': [["big"]],
        'weight': 1,
        # Comparative adjective ending in 'er'
    },
    {
        'input_text': [["more interesting"]],
        'expected': [["interesting"]],
        'weight': 1,
        # Comparative adverb with 'more' preceding it
    },
    {
        'input_text': [["most interesting"]],
        'expected': [["interesting"]],
        'weight': 1,
        # Superlative adverb with 'most' preceding it
    },
]

# Define directories
directories = ['tests/effectiveness', 'tests/efficiency', 'tests/hypothesis']

# Create directories if they don't exist
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Create an instance of the InflectionReduction class
inflection_reduction = InflectionReduction()

# Run the effectiveness test
effectiveness_metrics = inflection_reduction.effectiveness(test_cases)

# Save test cases and effectiveness metrics
with open('tests/effectiveness/inflectionReduction.txt', 'w', encoding='utf-8') as file:
    # Write precision, recall, and F1 scores for all approaches
    file.write(f"Stemming: Precision - {effectiveness_metrics['stem']['precision']}, Recall - {effectiveness_metrics['stem']['recall']}, F1 Score - {effectiveness_metrics['stem']['f1_score']}\n")
    file.write(f"Lemmatization: Precision - {effectiveness_metrics['lemmatize']['precision']}, Recall - {effectiveness_metrics['lemmatize']['recall']}, F1 Score - {effectiveness_metrics['lemmatize']['f1_score']}\n")
    file.write(f"Hybrid: Precision - {effectiveness_metrics['hybrid']['precision']}, Recall - {effectiveness_metrics['hybrid']['recall']}, F1 Score - {effectiveness_metrics['hybrid']['f1_score']}\n\n")
    for case in effectiveness_metrics['results']:
        file.write(f"Input Text: {case['input_text']}\n")
        file.write(f"Expected: {case['expected']}\n")
        file.write(f"Stem Output: {case['stem_output']}\n")
        file.write(f"Stem Passed: {case['stem_passed']}\n")
        file.write(f"Lemmatize Output: {case['lemmatize_output']}\n")
        file.write(f"Lemmatize Passed: {case['lemmatize_passed']}\n")
        file.write(f"Hybrid Output: {case['hybrid_output']}\n")
        file.write(f"Hybrid Passed: {case['hybrid_passed']}\n\n")

# Print effectiveness metrics
print(f"Stem: Precision - {effectiveness_metrics['stem']['precision']}, Recall - {effectiveness_metrics['stem']['recall']}, F1 Score - {effectiveness_metrics['stem']['f1_score']}")
print(f"Lemmatize: Precision - {effectiveness_metrics['lemmatize']['precision']}, Recall - {effectiveness_metrics['lemmatize']['recall']}, F1 Score - {effectiveness_metrics['lemmatize']['f1_score']}")
print(f"Hybrid: Precision - {effectiveness_metrics['hybrid']['precision']}, Recall - {effectiveness_metrics['hybrid']['recall']}, F1 Score - {effectiveness_metrics['hybrid']['f1_score']}")

print(effectiveness_metrics['stem'])
print(effectiveness_metrics['lemmatize'])
print(effectiveness_metrics['hybrid'])