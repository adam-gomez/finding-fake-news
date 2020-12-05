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
Is there a difference between the mean lengths of articles from The Onion and articles not from The Onion?
```
Null hypothesis: There is no difference in article lengths.
Alternative hypothesis: The lengths of Onion articles differs from the lengths of non-Onion articles.
```

```
Null hypothesis: There is no difference in the number of stopwords in Onion articles and non-Onion articles.
Alternative hypothesis: There is a difference in the number of stopwords in Onion articles and non-Onion articles.
```

## Project Steps
### Acquire
Scrape headlines from r/TheOnion and r/NotTheOnion utilizing Reddit's API
### Prepare
- Clean strings by removing non-alphanumeric characters and lowercasing all letters
- Stem and lemmatize words
- Remove common stopwords
- Determine length of each article headline
- Determine number of stopwords removed

### Explore
Can use exandable text for large amounts of text.
<details>
  <summary> Click to Expand </summary>
  
  Text goes in here. Maybe an image.
  ### Headers Still Work
  If you add an empty line between the summary code and text.
</details>

### Model
- Short
  - Description
  
### Conclusions
Key insights from project.


### Tools & Requirements
What tools did you use and what version were they?  
Python version 3.85

## License
Your permissions for users when reproducing your project.

## Creators
Adam Gomez