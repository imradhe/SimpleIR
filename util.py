# Add your import statements here

import time
import random
import string
import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.stem import PorterStemmer, WordNetLemmatizer
import numpy as np
from scipy import stats
import os
import spacy
import json
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import torch

def calculate_metrics(results, approach):
    true_positives = sum(case['weight'] for case in results if case[f'{approach}_passed'])
    false_positives = sum(case['weight'] for case in results if not case[f'{approach}_passed'] and case[f'{approach}_output'])
    false_negatives = 0

    precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    return {'precision': precision, 'recall': recall, 'f1_score': f1_score, 'true_positives': true_positives, 'false_positives': false_positives, 'false_negatives': false_negatives}