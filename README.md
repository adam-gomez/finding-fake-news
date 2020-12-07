# Identifying Fake News
## About the Project
### Goals
Using natural language processing and classification, the aim of this project is to predict whether a given headline is from a legitimate news source or if it was produce by the satire team at theonion.com.

### Background
Reddit is an American social news aggregation, web content rating, and discussion website. Registered members submit content to the site such as links, text posts, and images, which are then voted up or down by other members. Reddit is partitioned into forums called subreddits, that generally limit content to specific rules or themes. 

The two subreddits of interest in this project are:

1. https://www.reddit.com/r/TheOnion/
- The about section of this subreddit reads: "Articles from The Onion. This is not /r/nottheonion. Only links to the Onion are allowed here."
- The Onion is an American satirical digital media company and newspaper organization that publishes articles on international, national, and local news. 
- As a satirical organization, the Onion parodies topics trending through social media, traditional news organizations, and current events by releasing short and factually false articles with the goal of eliciting humor. 

2. https://www.reddit.com/r/nottheonion/
- The about section of this subreddit reads: "For true stories that are so mind-blowingly ridiculous that you could have sworn they were from The Onion."
- Members of this subreddit contribute links to online articles published by legitimate news sources.
- The content of these articles is considered so sensational and/or unbelievable that they might be mistaken for an onion article. 

Given the proliferation of factually incorrect content throughout social media, it is valuable to develop natural language processing algorithms that can identify legitimate content from fictional content. 

### Deliverables
1. A notebook that walks through the data science pipeline:
    - Acquisition
    - Preparation
    - Exploration
    - Modeling
    - Conclusions
2. A slide presentation that contains the following:
    - Title, intro, and conclusion slides
    - An executive summary on a single slide
    - An explanation of project purpose and goals
    - Details around where the data came from and the data prep
    - A visualization or several of insights gained from exploration
    - A summary of your modeling results

### Acknowledgments
The idea for this project came from [Luke Fielberg](https://github.com/lukefeilberg)

## Data Dictionary
Describe the columns in your final dataset. Use [this link](https://www.tablesgenerator.com/markdown_tables) to easily create markdown tables.

| Feature Name | Description                                                 | Additional Info |
|--------------|-------------------------------------------------------------|-----------------|
| text         | Unedited raw string scraped from Reddit's API               | string          |
| label        | Identifies the text as coming from The Onion (1) or not (0) | int             |

## Initial Thoughts & Hypotheses
### Thoughts
Given that the Onion has a reputation as a satirical organization, I suspect that they are not as bound by norms of decorum compared to traditional news organizations. Consequently, Onion headlines are much more likely to contain expletives and derogatory language. 

There may also be differences in the length of the headline. The Onion has no history of printed publications and it has never had to concern itself with typesetting limits that traditional news agencies may still be adhereing to (even as they switch to digital formats). 

I also suspect that the number of stopwords might be slightly different between Onion and non-Onion publishers. Given the more conversational style of Onion headlines, there might be a significant enough difference to include this as a feature. 

### Hypotheses
Are headlines from The Onion longer than headlines from non-Onion sources?
```
Null hypothesis: There is no difference in headline lengths.
Alternative hypothesis: The lengths of Onion headlines differs from the lengths of non-Onion headlines.
```
Are there more stopwords in Onion headlines than non-Onion headlines?
```
Null hypothesis: There is no difference in the number of stopwords in Onion headlines and non-Onion headlines.
Alternative hypothesis: There is a difference in the number of stopwords in Onion headlines and non-Onion headlines.
```

## Project Steps
### Acquire
Scrape headlines from r/TheOnion and r/NotTheOnion utilizing Reddit's API
### Prepare
- Clean strings by removing non-alphanumeric characters and lowercasing all letters
- Stem and lemmatize words
- Remove common stopwords
- Determine length of each article's headline
- Determine number of stopwords removed

### Explore
Statistical testing established that there Onion headlines are longer and have more stopwords removed than Non-Onion headlines. Although not tested statistically, it appears that Onion headlines have more expletives. Word counts, ratios, and word clouds revealed that the the two classes are very similar to each other in presentation. 

The data suffers from significant class imbalance (94% Non-onion to 6% Onion). Rebalancing the sample will be integral to model performance on unseen data.

### Model
- Logistic Regression with Bag of Words Vectorization and Random Oversampling of Minority Class 
  - Overall accuracy of the top model: 89.5%
  - f1-score: 0.44
  - Onion headlines
    - recall: 0.67
    - precision: 0.33
  - Non-Onion headlines
    - recall: 0.91
    - precision: 0.98
  
### Conclusions
The value of resampling an imbalanced dataset cannot be understated. Resampling the dataset showed substantial improvement in the model's ability to predict the minority class with only a relatively small loss in predicting the majority class. In cases where a false negative is more costly than a false positive (as may often be the case in imbalanced datasets (fraud, disease detection, etc.)) resampling is essential.

In the case of our model, while we did end up with an f1-score of 0.44 (precision: 0.33, recall: 0.67), the model is not accurate enough to use as a hard screen (meaning that we take action on predicted fake news headlines without additional oversight). If this were to be used in production, it could be used to flag headlines for users, to warn them to consider the possibility that the information is fictional.


### Replicating This Project
Data was retrieved from Reddit's API by querying each daily period over a 12 year time frame. This process is very time consuming, and should take 4 hours to complete. 

## License
Your permissions for users when reproducing your project.

## Creators
Adam Gomez