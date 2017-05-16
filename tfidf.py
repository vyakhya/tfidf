from common import gettext, tokenize, stemwords
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import os
import fnmatch

def tokenizer(text):
    tokens = tokenize(text)
    tokens = stemwords(tokens)
    return tokens

tfidf = TfidfVectorizer(input='filename', # argument to transform() is list of files
                        analyzer='word',
                        preprocessor=gettext, # convert xml to text
                        tokenizer=tokenizer,  # tokenize, stem
                        stop_words='english', # strip out stop words
                        decode_error = 'ignore') 
root = sys.argv[1]
file = sys.argv[2]
list_of_filenames = [os.path.join(dirpath, f) for (dirpath, dirnames, filenames) in os.walk(root) for f in fnmatch.filter(filenames, '*.xml')]

for i in range(len(list_of_filenames)):
    if file == list_of_filenames[i]:
        file_index = i
        break


matrix1 = tfidf.fit_transform(list_of_filenames)
matrix2 = matrix1.nonzero()

word_index = []
for i in range(len(matrix2[0])):
    if matrix2[0][i] == file_index:
        word_index.append(matrix2[1][i])

results = []
for index in word_index:
    if matrix1[(file_index, index)] >= 0.09:
        results.append((tfidf.get_feature_names()[index], matrix1[(file_index, index)]))

results = sorted(results, key=lambda x: x[1], reverse = True)

for value in results:
    print value[0], '%.3f' % value[1]