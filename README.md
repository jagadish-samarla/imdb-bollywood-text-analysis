# IMDB Bollywood Text Analysis

# what is this for?
This project takes movie titles and performs web scraping using python-selenium extracts all the required data from the IMDB website.
After scraping data from website, Text analysis and exploratory data analysis are performed on that extracted data.


# Steps to follow:
Raw movie titles 'Bollywood Movies Dataset.xlsx' is cleaned as 'cleaned_bollywoodlist.xlsx' by running first 9 lines of code in 'IMDB_text_analysis.ipynb'.

'cleaned_bollywoodlist.xlsx' file must be downloaded and added to the local repository to perform web scraping using selenium.

After performing web scraping all the output files uploaded manually to the google drive to perform further text analysis and exploratory data analysis on google collab.


# Naming Convention:
#### Bollywood Movies Datases.xlsx -  Given excel file that contained raw movie titles.
#### cleaned_bollywoodlist.xlsx -  An excel file with cleaned movie titles (by removing special characters and punctuations)
#### complete_database (1).xlsx -  Final database file with all the required attributes
#### Final_textAnalysis.csv -  A csv file that contains with all text analysis attributes
#### top_10_actors.csv -  A csv file that contains top 10 most acted actors from the data.
#### Genre_distribution_of_titles -  A csv file that contains exploratory analysis of 'Genre distribution of titles'
#### scrape_imdb.py -  Python script to perform python selenium web scraping
#### IMDB_text_analysis.ipynb -  Python notebook to perform text analysis and exploratory data analysis. 

