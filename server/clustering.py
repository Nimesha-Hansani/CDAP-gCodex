#Third Function
# NLTK Stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy
import string
# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
# %matplotlib inline
#Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
import warnings
#warnings.filterwarnings("ignore",category=DeprecationWarning)
from github  import Github
import collections

def defectsClustering(username,password,repo):

    g = Github(username, password)
    user =g.get_user()
    repository=g.get_repo(repo)
    repoName=repo

    Issues =repository.get_issues()
    commitIssues = []

    try:
        from collections.abc import Callable  # noqa
    except ImportError:
        from collections import Callable  # noqa

    print("I am here")
    # Import Dataset
    df_issues = pd.read_csv('D:/CDAP/g-Codex/dataset.csv')
   #print(df.target_names.unique())
    print(df_issues)
    # df.head()
    #df_issues=pd.DataFrame(commitIssues)

    #Get all to lowercase
    #df_issues = df_issues.apply(lambda x: x.lower())
    
    #Remove punctuations
    df_issues.Issue= df_issues.Issue.apply(lambda x: x.translate(string.punctuation))
    #print("step 1")
   # Convert to list
    data = df_issues.Issue.values.tolist()
    #Sent to word
    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence),deacc=True))
    # Remove Emails
    data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]

    # Remove new line characters
    data = [re.sub('\s+', ' ', sent) for sent in data]

    # Remove distracting single quotes
    data = [re.sub("\'", "", sent) for sent in data]

    data_words = list(sent_to_words(data))
    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100) 
    
    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # See trigram example
    # print(trigram_mod[bigram_mod[data_words[0]]])
    print("step 2")
     # Define functions for stopwords, bigrams, trigrams and lemmatization
    def remove_stopwords(texts):
       return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]

    def make_trigrams(texts):
       return [trigram_mod[bigram_mod[doc]] for doc in texts]

    # def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    #     """https://spacy.io/api/annotation"""
    #     texts_out = []
    #     for sent in texts:
    #         doc = nlp(" ".join(sent)) 
    #         texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    #     return texts_out

# Remove Stop Words
    data_words_nostops = remove_stopwords(df_issues.Issue)

# Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops)

# Create Dictionary
    id2word = corpora.Dictionary(data_words_bigrams)

# Create Corpus
    texts = data_words_bigrams

# Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

# View


    id2word[0]

# Human readable format of corpus (term-frequency)
    [[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]

#Testing for four topics
# Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=4, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

# Compute Coherence Score
    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words_bigrams, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherence_lda)

    # Print the Keyword in the 10 topics
    pprint(lda_model.print_topics())
    doc_lda = lda_model[corpus]

    for idx, topic in lda_model.print_topics(-1):
        print('Topic: {} \nWords: {}'.format(idx, topic))
    
# Compute Perplexity
    print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

# Compute Coherence Score
    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words_bigrams, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score for for five topics: ', coherence_lda)


# Visualize the topics
    #pyLDAvis.enable_notebook()
    
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    # pyLDAvis.show(vis, '192.168.8.100', port=8888, n_retries=5, local=False, open_browser=True, http_server= None)
    #pyLDAvis.save_html(vis,'kush.html')
    print('hi')
    ad = pyLDAvis.prepared_data_to_html(vis,template_type="general")
    print(ad)
    return ad










