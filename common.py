import xml.etree.cElementTree as ET
import re
import nltk
import string
import sys
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def gettext(xmltext):
    """
    Parse xmltext and return the text from <title> and <text> tags
    """
    tree = ET.ElementTree(ET.fromstring(xmltext))
    root = tree.getroot()
    title = root.find('title')
    result = title.text
    for element in root.iterfind(".//text/*"):
        result = result + " " + element.text
    return result

def tokenize(text):
    """
    Tokenize text and return a non-unique list of tokenized words
    found in the text. Normalize to lowercase, strip punctuation,
    remove stop words, drop words of length < 3.
    """
    text = text.lower()
    remove = re.compile('[' + string.punctuation + '0-9\\r\\t\\n]')
    cleanText = re.sub(remove, " ", text)
    tokens = nltk.word_tokenize(cleanText)
    tokens = [w.lower() for w in tokens if (len(w) >= 3 and w not in ENGLISH_STOP_WORDS)]
    return tokens

def stemwords(words):
    """
    Given a list of tokens/words, return a new list with each word
    stemmed using a PorterStemmer.
    """
    stemmer = nltk.stem.PorterStemmer()
    result = [stemmer.stem(w) for w in words]
    return result

if __name__=="__main__" :
    f = open(sys.argv[1])
    xmltext = f.read()
    text = gettext(xmltext)
    tokens = stemwords(tokenize(text))
    counts = Counter(tokens)
    for c in counts.most_common(10):
        print c[0], c[1]