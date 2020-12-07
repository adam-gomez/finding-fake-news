import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from numpy.random import choice
from sklearn.metrics import roc_auc_score, roc_curve
import re
import unicodedata
import nltk

# default viz size settings
plt.rc('figure', figsize=(9, 7))
plt.rc('font', size=15)

from wordcloud import WordCloud

def idf(words_df, train):
    '''
    Takes in a dataframe made of a single column where each row is a single word and 
    returns a dataframe containing the top 10 most frequent words,
    the number of documents each word shows up in, and the idf value for each word
    Also requires the train dataframe to be passed in as an argument in order to identify the
    total number of documents
    '''
    
    # Creates a dictionary of the top ten words and their number of counts
    top_10_words = words_df[0].value_counts(dropna=False).head(10).keys().tolist()
    top_10_counts = words_df[0].value_counts(dropna=False).head(10).tolist()
    word_counts = dict(zip(top_10_words, top_10_counts))
    
    # Derives the 10 most common words from the given dataframe of words
    most_common_words = [word[0] for word in list(words_df.value_counts().head(10).index)]
    
    # This dictionary will store how many documents each word appears in 
    appearances_dict = dict.fromkeys(most_common_words)
    
    # The total number of documents is based on the number of rows in the train dataframe
    number_of_documents = train.shape[0]
    
    # This is essentially a list containing the contents of the words column in the dataframe. It is a list of lists.
    list_of_wordlists = list(train.words.values)
    
    # Start iterating through the list of common words. We want to collect information for each one.
    for word in most_common_words:
        
        # Set the initial number of documents that the word appears in to zero
        number_of_appearances = 0
        
        # Start iterating through the list made from the words column in the dataframe 
        for words in list_of_wordlists:
            
            # If the current word is in a document, add 1 to the number of appearances and then move to the next document
            if word in words:
                number_of_appearances += 1
        
        # Once all the documents have been iterated through, add the sum total of all appearances to our appearances dictionary
        appearances_dict[word] = number_of_appearances
        
    # Create a new dictionary that will contain the IDF values for each word
    idf_dict = dict.fromkeys(most_common_words)
    
    # Start iterating through the list of common words again, using the number of appearances and the total number of documents to calculate the IDF and update the relevant key:value in the dictionary
    for word in most_common_words:
        idf_dict[word] = np.log(number_of_documents / appearances_dict[word])
    
    # Create dataframes containing the information of the total counts, the number of documents, and the idf value
    idf_df1 = pd.DataFrame.from_dict(word_counts, orient='index', columns=['total_count']).reset_index().rename(columns={'index':'word'})
    idf_df2 = pd.DataFrame.from_dict(appearances_dict, orient='index', columns=['num_of_documents']).reset_index().rename(columns={'index':'word'})
    idf_df3 = pd.DataFrame.from_dict(idf_dict, orient='index', columns=['idf_value']).reset_index().rename(columns={'index':'word'})
    
    # Merge the dataframes into a single dataframe
    idf_df = pd.merge(idf_df1, idf_df2, left_on = 'word', right_on = 'word')
    idf_df = pd.merge(idf_df, idf_df3, left_on = 'word', right_on = 'word')
    
    # Return the dataframe
    return idf_df

def h_bar_proportions(word_counts, onion_words_df, all_words_df):
    '''
    This function takes in a dataframe that contains the counts of words (labeled by the index)
    and displays those counts in an 'all' column (the count in the entire dataset), a 'onion' column
    (the count in the onion subset of words) and a 'not-onion' column (the count in the non-onion subset
    of words). 

    It displays a horizontal bar chart showing the top 20 words within the dataset and the relative 
    proportion between onion words and non-onion words. 
    '''
    # Developing horizontal stacked bar chart showing proportion or onion words to not-onion words
    (word_counts
    .assign(onion=word_counts.onion / word_counts['all'],
            not_onion=word_counts.not_onion / word_counts['all'])
    .sort_values(by='all')
    [['onion', 'not_onion']]
    .tail(20)
    .sort_values('onion')
    .plot.barh(stacked=True, width = .75, color = ['dodgerblue', 'lightgrey'], figsize=(12,8), fontsize=18))

    # Cleaning up the y_axis labels by deriving them from the word_counts
    word_counts_y_ticks_df = word_counts.sort_values(by='all', ascending = False).head(20) # Gets the top 20 words in the index
    word_counts_y_ticks_df['proportion'] = word_counts_y_ticks_df.onion / word_counts_y_ticks_df['all'] # creates a proportion to then order the index by
    word_counts_y_ticks_index = word_counts_y_ticks_df.sort_values(by='proportion', ascending = False).index # orders the index by the proportion
    y_ticks = [element[0] for element in word_counts_y_ticks_index] # converts the index from ugly tuples (word, ) into simple strings and puts them in a list
    y_ticks.reverse() # reverses the list to match the bar graphs orientation
    plt.yticks(range(len(y_ticks)), y_ticks) # adds the cleaner labels to the bar graph

    # Adding an x-axis label
    plt.xlabel('Proportion')

    # Removing the unnecessary a y-axis label
    plt.ylabel('')
    
    # Adding a vertical line indicating the relative proportion of onion words in the overall train data
    onion_words_proportion = onion_words_df.shape[0]/all_words_df.shape[0]
    plt.vlines(onion_words_proportion, -1, 20, colors = 'black', linestyles = 'dashed')
    plt.annotate('Relative Proportion of Onion Words in All Words', xy=(onion_words_proportion + .01, -.10), fontsize=12)

    # Adding a title
    plt.title('Proportion of Onion vs Not-Onion for the 20 most common words', fontsize=18)

def generate_auc_roc_curve(clf, X_set, Y_set):
    y_pred_proba = clf.predict_proba(X_set)[:, 1]
    fpr, tpr, thresholds = roc_curve(Y_set,  y_pred_proba)
    auc = roc_auc_score(Y_set, y_pred_proba)
    plt.plot(fpr,tpr,label="AUC ROC Curve with Area Under the Curve ="+str(auc))
    plt.legend(loc=4)
    plt.show()
    pass