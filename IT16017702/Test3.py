import pandas as pd
import string
from sklearn.model_selection import train_test_split
#from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report



sup = pd.read_csv("C:/Users/Kushi/Desktop/Research/Book1.csv")
sup.head()
sup.describe()
sup.groupby('Level').describe()



# to change use .astype() 
sup['Level'] = sup.Level.astype(int)
sup.head()
sup['Length'] = sup['Issue'].apply(len)
sup.head()

import matplotlib.pyplot as plt
import seaborn as sns



sup['Length'].plot(bins=50,kind = 'hist')

sup['Length'].describe()

sup[sup['Length'] == 103]['Issue'].iloc[0]
mess = 'Sample message ! Notice: it has punctuation'
sup.hist(column='Length',by ='Level',bins=50,figsize = (10,4))
from nltk.corpus import stopwords
stopwords.words('english')[0:10]
nopunc = [char for char in mess if char not in string.punctuation]

nopunc = ''.join(nopunc)
nopunc
nopunc.split()
clean_mess = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
clean_mess

def text_process(mess):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Returns a list of the cleaned text
    """
    # Check characters to see if they are in punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)
    
    # Now just remove any stopwords
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]


sup.head()

sup['Issue'].head(5).apply(text_process)
from sklearn.feature_extraction.text import CountVectorizer

bow_transformer = CountVectorizer(analyzer=text_process)

bow_transformer.fit(sup['Issue'])

message4 = sup['Issue'][3]

print (message4)

bow4 = bow_transformer.transform([message4])

print (bow4)

print (bow_transformer.get_feature_names()[40])
#dataset
messages_bow = bow_transformer.transform(sup['Issue'])

print ('Shape of Sparse Matrix: ', messages_bow.shape)
print ('Amount of Non-Zero occurences: ', messages_bow.nnz)
print ('sparsity: %.2f%%' % (100.0 * messages_bow.nnz /
                             (messages_bow.shape[0] * messages_bow.shape[1])))


from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer().fit(messages_bow)


tfidf4 = tfidf_transformer.transform(bow4)

print (tfidf4)

print (tfidf_transformer.idf_[bow_transformer.vocabulary_['u']])
print (tfidf_transformer.idf_[bow_transformer.vocabulary_['university']])

messages_tfidf = tfidf_transformer.transform(messages_bow)

print (messages_tfidf.shape)

from sklearn.naive_bayes import MultinomialNB

spam_detect_model = MultinomialNB().fit(messages_tfidf,sup['Level'])

print ('Predicted: ',spam_detect_model.predict(tfidf4)[0] )
print ('Expected: ',sup['Level'][8])

all_predictions = spam_detect_model.predict(messages_tfidf)
print (all_predictions)

from sklearn.metrics import classification_report
print (classification_report(sup['Level'], all_predictions))

msg_train, msg_test, label_train, label_test = \
train_test_split(sup['Level'], sup['Level'], test_size=0.2)

print (len(msg_train), len(msg_test), len(msg_train) + len(msg_test))

from sklearn.pipeline import Pipeline

pipeline = Pipeline([('bow',CountVectorizer(analyzer =text_process)),
                    ('tfidf',TfidfTransformer()),
                    ('classifier',MultinomialNB())])


pipeline.fit(msg_train,label_train)

predictions = pipeline.predict(msg_test)

print (classification_report(predictions,label_test))






