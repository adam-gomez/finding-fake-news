import numpy as np
import pandas as pd
import os
import unicodedata
import re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
# nltk.download('wordnet') - needed to run to download 'wordnet' resource to use lemmatize function

def basic_clean(string):
    '''
    This function takes in a string and
    returns the string normalized.
    '''
    # lowercase all characters
    string = string.lower()
    # normalize unicode characters
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    # remove anything that is not a through z, a number, a single quote, or whitespace
    string = re.sub(r"[^a-z0-9'\s]", ' ', string)
    # remove single numbers and single apostrophes
    string = re.sub(r"\s\d\s|'", ' ', string)
    return string

def tokenize(string):
    '''
    This function takes in a string and
    returns a tokenized string.
    '''    
    # Create tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    # Use tokenizer
    string = tokenizer.tokenize(string, return_str=True)
    return string

def stem(string):
    '''
    This function takes in a string and
    returns a string with words stemmed.
    '''
    # Create porter stemmer.
    ps = nltk.porter.PorterStemmer()
    # Use the stemmer to stem each word in the list of words we created by using split.
    stems = [ps.stem(word) for word in string.split()]
    # Join our lists of words into a string again and assign to a variable.
    string_stemmed = ' '.join(stems)
    return string_stemmed

def lemmatize(string):
    '''
    This function takes in string for and
    returns a string with words lemmatized.
    '''
    # Create the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    # Use the lemmatizer on each word in the list of words we created by using split.    
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    # Join our list of words into a string again and assign to a variable.
    string_lemmatized = ' '.join(lemmas)
    return string_lemmatized

def remove_stopwords(string, extra_words=[], exclude_words=[]):
    '''
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    '''
    # Create stopword_list
    stopword_list = stopwords.words('english')

    # If the optional list extra_words contains any strings:
    if len(extra_words) > 0:
        for word in extra_words:
            # Append the word to the stopword_list
            stopword_list.append(word)

    
    # If the optional list exclude_words contains any strings:
    if len(exclude_words) > 0:
        for word in exclude_words:
            if word in stopword_list:
                # Remove the word from the stopword_list
                stopword_list.remove(word)

    
    # Split words in string
    words = string.split()

    # Create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [w for w in words if w not in stopword_list]

    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)

    return string_without_stopwords

def prep_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    # Removes null values from the dataframe
    df = df.dropna().reset_index(drop=True)

    df['clean'] = df[column].apply(basic_clean).apply(tokenize).apply(remove_stopwords, extra_words=extra_words, exclude_words=exclude_words).apply(lemmatize).apply(remove_stopwords, extra_words=extra_words, exclude_words=exclude_words).apply(basic_clean)
    
    df['stemmed'] = df[column].apply(basic_clean).apply(stem)
    
    df['lemmatized'] = df[column].apply(basic_clean).apply(lemmatize)
    
    words = [re.sub(r'([^a-z0-9\s])', '', doc).split() for doc in df.clean]
    df = pd.concat([df, pd.DataFrame({'words': words})], axis = 1)
    
    doc_length = [len(wordlist) for wordlist in df.words]
    df['doc_length'] = doc_length
    
    df['stopwords_removed'] = df.apply(lambda row: len(row['lemmatized'].split()) - len(row['clean'].split()), axis=1)

    # Removes null values from the dataframe
    df = df.dropna().reset_index(drop=True)

    # Drop rows where doc_length = 0
    df = df[df.doc_length != 0]

    # Drop rows where doc_length > 50 (these have all been identified as being gibberish or vietnamese spam)
    df = df[df.doc_length <= 50]
    
#    Uncomment to drop rows that contain the word 'http'
#    df['http'] = df.words.apply(lambda x: 1 if 'http' in x else 0)
#    df = df[df['http'] != 1]
#    df.drop(columns=['http'], inplace=True)

    # Reset index final time
    df = df.reset_index(drop=True)

    # Save df to csv
    df.to_csv('headlines.csv', index=False)

    return df[['label', column, 'stemmed', 'lemmatized', 'clean', 'stopwords_removed', 'doc_length', 'words']]

def get_prepped_data(df, column):
    if not os.path.isfile('headlines.csv'):
        df = prep_data(df, column)
        return df
    else:
        df = pd.read_csv('headlines.csv')
        return df
