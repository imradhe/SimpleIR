import sys
sys.path.append('.')
from util import *
from inflectionReduction import InflectionReduction

test_cases = [
    {
        'input_text': [["cycling"]],
        'expected': [["cycle"]],
        'weight': .5,
        # Regular verb ending with 'ing'
    },
    {
        'input_text': [["bouncing"]],
        'expected': [["bounce"]],
        'weight': .6,
        # Another regular verb ending with 'ing'
    },
    {
        'input_text': [["running"]],
        'expected': [["run"]],
        'weight': .9,
        # A commonly mistaken case, where people may overlook irregularities and assume the regular inflection reduction
    },
    {
        'input_text': [["dying"]],
        'expected': [["die"]],
        'weight': .5,
        # Edge case: irregular verb ending with 'ing'
    },
    {
        'input_text': [["gently"]],
        'expected': [["gentle"]],
        'weight': .9,
        # Adverb ending with 'ly'
    },
    {
        'input_text': [["children"]],
        'expected': [["child"]],
        'weight': .3,
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
    {
        'input_text': [[]],
        'expected': [[]],
        'weight': 1,
        # Empty
    },
    {
        'input_text': [[" "]],
        'expected': [[" "]],
        'weight': 1,
        # Empty
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


inflection_reduction = InflectionReduction()
input_sizes = [100, 1000, 10000, 100000]  # input sizes

stem_times = inflection_reduction.efficiency(input_sizes)['stem_times']
lemmatize_times = inflection_reduction.efficiency(input_sizes)['lemmatize_times']
hybrid_times = inflection_reduction.efficiency(input_sizes)['hybrid_times']


# Save test cases and efficiency metrics as a text file
with open('tests/efficiency/inflectionReduction.txt', 'w', encoding='utf-8') as file:
    for i in range(len(input_sizes)):
        file.write(f"Input Size: {input_sizes[i]}\n")
        file.write(f"Stemming Approach Time: {stem_times[i]}\n")
        file.write(f"Lemmatization Approach Time: {lemmatize_times[i]}\n")
        file.write(f"Hybrid Approach Time: {hybrid_times[i]}\n\n")


alpha = 0.05  # Significance level

# Save and print hypothesis testing results
with open('tests/hypothesis/inflectionReduction.txt', 'w', encoding='utf-8') as file:
    for approach1, approach2 in [('stem', 'lemmatize'), ('stem', 'hybrid'), ('lemmatize', 'hybrid')]:
        approach1_precision_scores = [case['weight'] * effectiveness_metrics[approach1]['precision'] for case in test_cases if 'weight' in case]
        approach2_precision_scores = [case['weight'] * effectiveness_metrics[approach2]['precision'] for case in test_cases if 'weight' in case]
        # Perform a two-sided t-test for the null hypothesis that the means of the two approaches are equal
        t_statistic, p_value = stats.ttest_rel(approach1_precision_scores, approach2_precision_scores, nan_policy='omit')
        # Write the results of the hypothesis test
        file.write(f"T-statistic for precision scores ({approach1} vs {approach2}): {t_statistic}\n")
        file.write(f"P-value for precision scores ({approach1} vs {approach2}): {p_value}\n\n")
        if p_value < alpha:
            file.write(f"Reject the null hypothesis. There is a significant difference between the precision scores of {approach1} and {approach2}.\n\n")
        else:
            file.write(f"Fail to reject the null hypothesis. There is no significant difference between the precision scores of {approach1} and {approach2}.\n\n")

        # Compare p-value to alpha
        if p_value < alpha:
            if t_statistic > 0:
                file.write(f"Approach '{approach1}' performs better than approach '{approach2}'.\n\n")
            else:
                file.write(f"Approach '{approach2}' performs better than approach '{approach1}'.\n\n")
        else:
            file.write(f"There is no significant difference in effectiveness between {approach1} and {approach2}.\n\n")

# Print hypothesis testing results
print("Hypothesis Testing Results:")
with open('tests/hypothesis/inflectionReduction.txt', 'r', encoding='utf-8') as file:
    print(file.read())