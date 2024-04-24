# spaCy (en_core_web_md)

**spaCy's** `en_core_web_md` model is trained on data collected from news, blogs and comments on the internet.

## Pipeline
The pipeline or the flow of it's process involves the below components 

1. **Sentencizer (Top-down)**:
Implement rule-based sentence boundary detection that doesn’t require the dependency parse.

1. **SentenceRecognizer (Bottom-up)**:
A trainable pipeline component for sentence segmentation. It predicts the boundaries of a sentence as it is trained over a large corpus labeled data. 

1. **Tokenizer**:
Segment raw text and create Doc objects from the words, punctuations marks, etc.

1. **DependencyParser**:
Pipeline component for syntactic dependency parsing. By default, sentence segmentation is performed by the DependencyParser, so the Sentencizer lets you implement a simpler, rule-based strategy that doesn’t require a statistical model to be loaded.

1. **Tagger (Bottom-up)**:
Predict part-of-speech tags.

1. **Lemmatizer**:
Determine the base forms of words using rules and lookups.

1. **EditTreeLemmatizer**:
Predict base forms of words.

1. **AttributeRuler**:
Set token attributes using matcher rules.

1. **EntityRecognizer**:
Predict named entities, e.g. persons or products.

1. **Tok2Vec**:
Apply a “token-to-vector” model and set its outputs.


### POS Tags
Here's a table of all POS tags of tokens in the spaCy `en_core_web_md` model along with their descriptions:

| Tag | Description                                                  |
|-------|--------------------------------------------------------------|
| $     | Dollar sign                                                  |
| ''    | Single quotation mark                                        |
| ,     | Comma                                                        |
| -LRB- | Left round bracket                                           |
| -RRB- | Right round bracket                                          |
| .     | Period (full stop)                                           |
| :     | Colon                                                        |
| ADD   | Email headers, signatures, and other 'added' text           |
| AFX   | Affix                                                        |
| CC    | Coordinating conjunction                                     |
| CD    | Cardinal number                                              |
| DT    | Determiner                                                   |
| EX    | Existential there                                            |
| FW    | Foreign word                                                 |
| HYPH  | Hyphen                                                       |
| IN    | Preposition or subordinating conjunction                     |
| JJ    | Adjective                                                    |
| JJR   | Adjective, comparative                                       |
| JJS   | Adjective, superlative                                       |
| LS    | List item marker                                             |
| MD    | Modal                                                        |
| NFP   | Superfluous punctuation (e.g., hashtags)                     |
| NN    | Noun, singular or mass                                       |
| NNP   | Proper noun, singular                                        |
| NNPS  | Proper noun, plural                                          |
| NNS   | Noun, plural                                                 |
| PDT   | Predeterminer                                                |
| POS   | Possessive ending                                            |
| PRP   | Personal pronoun                                             |
| PRP$  | Possessive pronoun                                           |
| RB    | Adverb                                                       |
| RBR   | Adverb, comparative                                          |
| RBS   | Adverb, superlative                                          |
| RP    | Particle                                                     |
| SYM   | Symbol                                                       |
| TO    | to                                                           |
| UH    | Interjection                                                 |
| VB    | Verb, base form                                              |
| VBD   | Verb, past tense                                             |
| VBG   | Verb, gerund or present participle                           |
| VBN   | Verb, past participle                                        |
| VBP   | Verb, non-3rd person singular present                        |
| VBZ   | Verb, 3rd person singular present                            |
| WDT   | Wh-determiner                                                |
| WP    | Wh-pronoun                                                   |
| WP$   | Possessive wh-pronoun                                        |
| WRB   | Wh-adverb                                                    |
| XX    | Unknown, uncertain, or unclassifiable                        |
| _SP   | Space                                                        |
| ``    | Opening quotation mark                                       |


### Parser Labels
Here's a table listing the dependency labels (classes) used in the spaCy `en_core_web_md` model for parsing, along with their descriptions.

These labels are used to represent the syntactic relationships between words in a sentence, forming the basis of dependency parsing.


| Label     | Description                                                  |
|-----------|--------------------------------------------------------------|
| ROOT      | Root                                                         |
| acl       | Clausal modifier of noun (adjectival clause)                 |
| acomp     | Adjectival complement                                        |
| advcl     | Adverbial clause modifier                                    |
| advmod    | Adverbial modifier                                           |
| agent     | Agent                                                        |
| amod      | Adjectival modifier                                          |
| appos     | Appositional modifier                                        |
| attr      | Attribute                                                    |
| aux       | Auxiliary                                                    |
| auxpass   | Auxiliary (passive)                                          |
| case      | Case marking                                                 |
| cc        | Coordinating conjunction                                     |
| ccomp     | Clausal complement                                           |
| compound  | Compound                                                     |
| conj      | Conjunct                                                     |
| csubj     | Clausal subject                                              |
| csubjpass | Clausal subject (passive)                                    |
| dative    | Dative                                                       |
| dep       | Unclassified dependent                                       |
| det       | Determiner                                                   |
| dobj      | Direct object                                                |
| expl      | Expletive                                                    |
| intj      | Interjection                                                 |
| mark      | Marker                                                       |
| meta      | Meta modifier                                                |
| neg       | Negation modifier                                            |
| nmod      | Nominal modifier                                             |
| npadvmod  | Noun phrase as adverbial modifier                            |
| nsubj     | Nominal subject                                              |
| nsubjpass | Nominal subject (passive)                                    |
| nummod    | Numeric modifier                                             |
| oprd      | Object predicate                                             |
| parataxis | Parataxis                                                    |
| pcomp     | Complement of preposition                                    |
| pobj      | Object of preposition                                        |
| poss      | Possession modifier                                          |
| preconj   | Preconjunct                                                  |
| predet    | Predeterminer                                                |
| prep      | Prepositional modifier                                       |
| prt       | Particle                                                     |
| punct     | Punctuation                                                  |
| quantmod  | Modifier of quantifier                                       |
| relcl     | Relative clause modifier                                     |
| xcomp     | Open clausal complement                                      |

### Named Entity Recognizer (NER) Labels

Here's a table listing the named entity types used in the spaCy `en_core_web_md` model for named entity recognition (NER), along with their descriptions.

These entity types are used to classify and label named entities in text, providing information about their semantic meaning and context.


| Entity Type | Description                                                  |
|-------------|--------------------------------------------------------------|
| CARDINAL    | Numerals that do not fall under another type                  |
| DATE        | Absolute or relative dates or periods                        |
| EVENT       | Named hurricanes, battles, wars, sports events, etc.          |
| FAC         | Buildings, airports, highways, bridges, etc.                  |
| GPE         | Countries, cities, states                                    |
| LANGUAGE    | Any named language                                           |
| LAW         | Named documents made into laws                                |
| LOC         | Non-GPE locations, mountain ranges, bodies of water, etc.     |
| MONEY       | Monetary values, including unit                              |
| NORP        | Nationalities or religious or political groups                |
| ORDINAL     | "first", "second", etc.                                      |
| ORG         | Companies, agencies, institutions, etc.                       |
| PERCENT     | Percentage, including "%"                                    |
| PERSON      | People, including fictional                                  |
| PRODUCT     | Objects, vehicles, foods, etc. (not services)                 |
| QUANTITY    | Measurements, as of weight or distance                        |
| TIME        | Times smaller than a day, such as "10:00am"                   |
| WORK_OF_ART| Titles of books, songs, etc.                                 |


### Evaluation Metrics
| `TOKEN_ACC` | Tokenization                                       | 1.00 |
| ----------- | -------------------------------------------------- | ---- |
| `TOKEN_P`   |                                                    | 1.00 |
| `TOKEN_R`   |                                                    | 1.00 |
| `TOKEN_F`   |                                                    | 1.00 |
| `TAG_ACC`   | Part-of-speech tags (fine grained tags, Token.tag) | 0.97 |
| `SENTS_P`   | Sentence segmentation (precision)                  | 0.92 |
| `SENTS_R`   | Sentence segmentation (recall)                     | 0.89 |
| `SENTS_F`   | Sentence segmentation (F-score)                    | 0.91 |
| `DEP_UAS`   | Unlabeled dependencies                             | 0.92 |
| `DEP_LAS`   | Labeled dependencies                               | 0.90 |
| `ENTS_P`    | Named entities (precision)                         | 0.85 |
| `ENTS_R`    | Named entities (recall)                            | 0.85 |
| `ENTS_F`    | Named entities (F-score)                           | 0.85 |


## Implementation
Multiple methods used from the spaCy library to implement the IR:

1. `spacy.load("en_core_web_md")`:
   - This method loads the "en_core_web_md" language model, which is a pre-trained spaCy model for the English language. This model provides various linguistic features and capabilities, such as tokenization, lemmatization, and word embeddings.

2. `nlp(query)` and `nlp(doc)` for each document:
   - These methods use the loaded language model to process the query and each document, respectively. The `nlp` method takes the text as input and returns a `Doc` object, which represents the linguistic structure of the text.
   - This method handles all of the preprocessing involved in the pipeline like sentence segmentation, tokenization, stemming/lemmetization, stopword removal, and parsing.

3. `token.similarity(query_token)`:
   - This method calculates the similarity between a token in a document and a token in the query. The similarity is computed using the cosine similarity between the word embeddings of the two tokens.

4. `max([token.similarity(query_token) for token in doc_tokens])`:
   - This code snippet uses a list comprehension to find the maximum similarity between each token in the document and the query token. It iterates through all the tokens in the document and computes the similarity between each token and the query token, then takes the maximum value.

These spaCy methods allow the us to perform natural language processing tasks, such as tokenization, word embedding, and similarity computation, which are essential for the document retrieval task.

## Vector Representation of Meaning
The meaning of a token in spaCy is represented as a vector through a process called word embedding. This process involves mapping words or phrases from the vocabulary to vectors of real numbers. The model used by spaCy, such as `en_core_web_md`, typically employs pre-trained vectors from algorithms like **GloVe (Global Vectors for Word Representation)**.

Here's a breakdown of how the meaning is captured in a vector:

1. **Semantic Similarity**: Words that are used in similar contexts are positioned closer together in the vector space. For example, "king" and "queen" would have vectors that are close to each other because they tend to appear in similar contexts.

2. **Dimensionality**: Each vector has a fixed number of dimensions, and each dimension represents a latent feature that might capture a linguistic or semantic property. The medium-sized spaCy models usually have vectors with 300 dimensions.

3. **Training**: The vectors are obtained by training on a large corpus of text. During training, the model learns to predict a word based on its context (surrounding words), which results in vectors that encode word meanings.

4. **Contextual Information**: Although individual token vectors are static, meaning they don't change based on the sentence they're in, the way they interact with other vectors (through operations like similarity) can capture some aspects of context.

5. **Vector Operations**: The vectors can be used to perform mathematical operations. For instance, you can calculate the cosine similarity between vectors to determine how similar two words are in terms of their meaning.

6. **Normalization**: Often, vectors are normalized so that their length (norm) is 1. This makes it easier to compare vectors using cosine similarity, as only the angle between them matters.

 
For example, the vector for the word "apple" might look like this (simplified to 3 dimensions for illustration):

$$
\text{apple} = \begin{bmatrix}
-0.36391 \\
0.43771 \\
-0.20447
\end{bmatrix}
$$

This numerical representation allows the model to perform various NLP tasks, such as calculating the similarity between words, clustering words into groups, and using them as features in machine learning models.

It's important to note that while these vectors capture many aspects of word meaning, they are not perfect. They might not capture every nuance, especially for words with multiple meanings or for very domain-specific language.

### Statistical Semantics
In the spaCy `en_core_web_md` model, the word vectors are primarily based on the GloVe algorithm, which uses co-occurrence statistics to capture semantic and syntactic information about words. The factors considered in the representation of word vectors in this model include:

- **Co-occurrence**: How often words appear near each other in the text.
- **Colocation**: The tendency of words to appear in specific positions relative to one another.
- **Contextual Similarity**: Words that appear in similar contexts have similar meanings and thus have similar vectors.

While the GloVe algorithm effectively captures patterns of co-occurrence and colocation, it does not explicitly encode linguistic relationships like synonymy, antonymy, or homonymy. However, because words with similar meanings tend to appear in similar contexts, the vectors can indirectly capture some aspects of synonymy. Antonymy and homonymy are more challenging because they often require understanding beyond mere co-occurrence, such as world knowledge or the specific use of words in context.

## Limitations
The vectors in models like spaCy's `en_core_web_md` do represent aspects of word meaning, but they primarily capture meaning through the lens of contextual similarity and might not accurately represent the meaning as we humans interpret. The vectors are derived from **statistical patterns** in the text data they were trained on, which means they reflect the contexts in which words tend to appear.


- **Indirect Representation of Meaning**: While the vectors don't encode meaning in the same way humans understand it, they do capture relationships between words that can be indicative of meaning. For example, synonyms often have similar vectors because they appear in similar contexts.

- **Contextual Similarity Over Literal Meaning**: The vectors are better at capturing words' contextual usage rather than their dictionary definitions. This means they can be very effective for tasks like similarity comparison but may not always align with human intuition about meaning, especially for words with multiple senses or less common usages.

- **Beyond meaning**: These vectors don't capture the full complexity of human language, such as idiomatic expressions, sarcasm, or nuanced meanings that require world knowledge or situational context.

In summary, the vectors represent a form of meaning that is grounded in statistical patterns of word usage. They are a powerful tool for many NLP tasks, but they are not a complete representation of linguistic meaning as understood by humans. For applications that require a deeper understanding of language, additional context or more advanced models, like those based on transformer architectures, may be necessary.

