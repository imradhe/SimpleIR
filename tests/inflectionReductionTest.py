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
        'input_text': [["cats"]],
        'expected': [["cat"]],
        'weight': 1,
        # Plural noun ending with 's'
    },
    {
        'input_text': [["discussed"]],
        'expected': [["discuss"]],
        'weight': 1,
        # Regular verb in past tense ending with 'ed'
    },
    {
        'input_text': [["running"]],
        'expected': [["run"]],
        'weight': 1,
        # Regular verb ending with 'ing'
    },
    {
        'input_text': [["better"]],
        'expected': [["good"]],
        'weight': 1,
        # Word with no inflection
    },
    {
        'input_text': [["leaves"]],
        'expected': [["leaf"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["carried"]],
        'expected': [["carry"]],
        'weight': 1,
        # Regular verb in past tense ending with 'ed'
    },
    {
        'input_text': [["studying"]],
        'expected': [["study"]],
        'weight': 1,
        # Regular verb ending with 'ing'
    },
    {
        'input_text': [["mice"]],
        'expected': [["mouse"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["boxes"]],
        'expected': [["box"]],
        'weight': 1,
        # Regular plural noun ending with 'es'
    },
    {
        'input_text': [["calves"]],
        'expected': [["calf"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["pennies"]],
        'expected': [["penny"]],
        'weight': 1,
        # Regular plural noun ending with 'ies'
    },
    {
        'input_text': [["radii"]],
        'expected': [["radius"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["analyses"]],
        'expected': [["analysis"]],
        'weight': 1,
        # Regular plural noun ending with 'es'
    },
    {
        'input_text': [["criteria"]],
        'expected': [["criterion"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["phenomena"]],
        'expected': [["phenomenon"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["matrices"]],
        'expected': [["matrix"]],
        'weight': 1,
        # Regular plural noun ending with 'es'
    },
    {
        'input_text': [["vertices"]],
        'expected': [["vertex"]],
        'weight': 1,
        # Regular plural noun ending with 'es'
    },
    {
        'input_text': [["indices"]],
        'expected': [["index"]],
        'weight': 1,
        # Regular plural noun ending with 'es'
    },
    {
        'input_text': [["appendices"]],
        'expected': [["appendix"]],
        'weight': 1,
        # Regular plural noun ending with 'es'
    },
    {
        'input_text': [["bacteria"]],
        'expected': [["bacterium"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["data"]],
        'expected': [["datum"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["media"]],
        'expected': [["medium"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["loaves"]],
        'expected': [["loaf"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["hooves"]],
        'expected': [["hoof"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["lives"]],
        'expected': [["life"]],
        'weight': 1,
        # Regular plural noun ending with 's'
    },
    {
        'input_text': [["wives"]],
        'expected': [["wife"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["knives"]],
        'expected': [["knife"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["shelves"]],
        'expected': [["shelf"]],
        'weight': 1,
        # Regular plural noun ending with 's'
    },
    {
        'input_text': [["thieves"]],
        'expected': [["thief"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["potatoes"]],
        'expected': [["potato"]],
        'weight': 1,
        # Regular plural noun ending with 'es'
    },
    {
        'input_text': [["tomatoes"]],
        'expected': [["tomato"]],
        'weight': 1,
        # Regular plural noun ending with 'es'
    },
    {
        'input_text': [["volcanoes"]],
        'expected': [["volcano"]],
        'weight': 1,
        # Regular plural noun ending with 'es'
    },
    {
        'input_text': [["heroes"]],
        'expected': [["hero"]],
        'weight': 1,
        # Regular plural noun ending with 'es'
    },
    {
        'input_text': [["zeroes"]],
        'expected': [["zero"]],
        'weight': 1,
        # Regular plural noun ending with 'es'
    },
    {
        'input_text': [["zoos"]],
        'expected': [["zoo"]],
        'weight': 1,
        # Regular plural noun ending with 's'
    },
    {
        'input_text': [["boys"]],
        'expected': [["boy"]],
        'weight': 1,
        # Regular plural noun ending with 's'
    },
    {
        'input_text': [["girls"]],
        'expected': [["girl"]],
        'weight': 1,
        # Regular plural noun ending with 's'
    },
    {
        'input_text': [["children"]],
        'expected': [["child"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["men"]],
        'expected': [["man"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["women"]],
        'expected': [["woman"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["feet"]],
        'expected': [["foot"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["teeth"]],
        'expected': [["tooth"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["geese"]],
        'expected': [["goose"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["mice"]],
        'expected': [["mouse"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["lice"]],
        'expected': [["louse"]],
        'weight': 1,
        # Irregular plural noun
    },
    {
        'input_text': [["were"]],
        'expected': [["be"]],
        'weight': 1,
        # Irregular verb form
    },
    {
        'input_text': [["would"]],
        'expected': [["will"]],
        'weight': 1,
        # Irregular verb form
    },
    {
        'input_text': [["could"]],
        'expected': [["can"]],
        'weight': 1,
        # Irregular verb form
    },
    {
        'input_text': [["should"]],
        'expected': [["shall"]],
        'weight': 1,
        # Irregular verb form
    },
    {
        'input_text': [["might"]],
        'expected': [["may"]],
        'weight': 1,
        # Irregular verb form
    },
    {
        'input_text': [["am"]],
        'expected': [["be"]],
        'weight': 1,
        # Irregular verb form
    },
    {
        'input_text': [["is"]],
        'expected': [["be"]],
        'weight': 1,
        # Irregular verb form
    },
    {
        'input_text': [["are"]],
        'expected': [["be"]],
        'weight': 1,
        # Irregular verb form
    },
    {
        'input_text': [["was"]],
        'expected': [["be"]],
        'weight': 1,
        # Irregular verb form
    },
    {
        'input_text': [["been"]],
        'expected': [["be"]],
        'weight': 1,
        # Irregular verb form
    },
    {
        'input_text': [["being"]],
        'expected': [["be"]],
        'weight': 1,
        # Regular verb ending with 'ing'
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