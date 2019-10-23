import re
import string
import spacy
from textacy import preprocessing
from nltk.corpus import stopwords

nlp = spacy.load('/tmp/sbwc')

punct = string.punctuation + '“' + '”' + '¿' + '⋆' + '�'
URL_REGEX = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
DECIMAL_REGEX = '[0-9]+,[0-9]+'
sw1 = spacy.lang.es.stop_words.STOP_WORDS
sw2 = stopwords.words('spanish')

sw = set(sw1) | set(sw2)

def vect(doc, nlp):
    tokens = nlp(" ".join(doc.split()))
    processed = []
    urls = []

    for token in tokens:
        word = None
        if token.is_digit or re.match(DECIMAL_REGEX, token.lower_):
            continue
        elif re.match(URL_REGEX, token.lower_):
            urls.append(token.text)
        elif token.is_stop or token.lower_ in sw:
            continue
        elif (token.is_punct or token.lower_ in punct) and not token.is_quote:
            continue
        elif token.is_quote:
            continue
        else:
            word = token.lemma_
            word = word.lower()
            word = word.strip()
            word = preprocessing.remove_accents(word)
            word = word if word != '' else None

            if word == 'rt':
                word = None
            elif word and word.startswith(('@', '.@')):
                word = None
        if word:
            processed.append(word)

    doc = nlp(' '.join(processed))
    return doc.vector, urls