#importing requirements
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#importing cleaned movie title list as pandas dataframe
df = pd.read_excel("cleaned_bollywoodlist.xlsx", header=0)

#converting data frame as numpy array for further scraping
movie_list = df['Movie Title'].to_numpy()


#sample_movies = ['Teri Meri Kahaani (film)', 'Raja Natwarlal', 'Dum Maaro Dum (film)']

#instantitating drivers
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.implicitly_wait(3)

#these counts will help scraping to resume from the point where it stopped.
count = 0
start = 0

#instantiating empty lists for every attribute required
title_list = []
genre_list = []
cast_list = []
crew_list = []
plot_summary_list = []
plot_keywords_list = []
imdb_ratings_list = []
url_list = []
exception_count = 0

try:
    for index, movie in enumerate(movie_list[start:]):
        try:
            count += 1
            print(index+start, ': Processing ', movie)
            url = 'https://www.google.com/search?q=' + str(movie)
            driver.get(url)
            driver.implicitly_wait(2)
            driver.find_element_by_xpath("//a[contains(@href, 'https://www.imdb.com/')]").click()
            #appending 'url' to extract IMDB ID from it
            url_list.append(driver.current_url)
            driver.implicitly_wait(3)
            #acquiring all required links in the existing page.
            cast_link_node = driver.find_element_by_xpath("//a[contains(text(),'All cast & crew')]")
            cast_link = cast_link_node.get_attribute('href')
            summary_link_node = driver.find_element_by_xpath("//a[contains(text(),'Plot summary')]")
            summary_link = summary_link_node.get_attribute('href')

            #appending titles
            title_list.append(driver.find_element_by_xpath("//h1").text)
            #appending IMDB ratings
            imdb_ratings_list.append(driver.find_element_by_xpath(
                "//span[@class='AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV']").text)
            genres = driver.find_elements_by_xpath("//li[@data-testid='storyline-genres']//div/ul/li")
            genre_list_particular_movie = []
            for i in genres:
                genre_list_particular_movie.append(i.text)
                #appending genres
            genre_list.append(genre_list_particular_movie)
            driver.get(cast_link)
            driver.implicitly_wait(5)
            #cast_element = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@id='fullcredits_content']//table[@class='cast_list']/tbody/tr/td[2]/a")))
            cast = driver.find_elements_by_xpath("//div[@id='fullcredits_content']//table[@class='cast_list']/tbody/tr/td[2]/a")
            cast_list_particular_movie = []
            #driver.implicitly_wait(3)
            for i in cast:
                cast_list_particular_movie.append(i.text)
                #appending cast list
            cast_list.append(cast_list_particular_movie)
            crew = driver.find_elements_by_xpath("//div[@id='fullcredits_content']/table/tbody/tr/td[@class='name']/a")
            crew_list_particular_movie = []
            #driver.implicitly_wait(4)
            for i in crew:
                crew_list_particular_movie.append(i.text)
                #appending crew list
            crew_list.append(crew_list_particular_movie)
            # not a good thing
            # driver.back()
            driver.get(summary_link)
            time.sleep(2)
            driver.implicitly_wait(2)
            #summary_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(By.XPATH, "//ul[@id='plot-summaries-content']/li[1]/p"))
            plot_summary = driver.find_element_by_xpath("//ul[@id='plot-summaries-content']/li[1]/p")
            #appending plot summary
            plot_summary_list.append(plot_summary.text)
            driver.find_element_by_xpath("//a[contains(text(),'Plot Keywords')]").click()
            driver.implicitly_wait(5)
            #keywords_element = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located(By.XPATH, "//div[@id='keywords_content']/table/tbody/tr/td/div/a"))
            plot_keywords = driver.find_elements_by_xpath("//div[@id='keywords_content']/table/tbody/tr/td/div/a")
            plot_keywords_particular_movie = []
            for i in plot_keywords:
                plot_keywords_particular_movie.append(i.text)
            #appending plot keywords
            plot_keywords_list.append(plot_keywords_particular_movie)
        except Exception as e:
            print(e)
            df_temp = pd.DataFrame()
            #adding all data collected to dataframe and exporting it to an excel sheet for every exception
            df_temp['IMDB Title'] = pd.Series(title_list, dtype=str).to_frame()
            df_temp['url'] = pd.Series(url_list, dtype=str).to_frame()
            df_temp['Genre'] = pd.Series(genre_list, dtype=str).to_frame()
            df_temp['Cast'] = pd.Series(cast_list, dtype=str).to_frame()
            df_temp['Crew'] = pd.Series(crew_list, dtype=str).to_frame()
            df_temp['Plot summary'] = pd.Series(plot_summary_list, dtype=str).to_frame()
            df_temp['Plot keywords'] = pd.Series(plot_keywords_list, dtype=str).to_frame()
            df_temp['IMDB Ratings'] = pd.Series(imdb_ratings_list, dtype=str).to_frame()
            df_temp.to_excel("final_output_{0}-{1}.xlsx".format(start+index-count+1, start+index))
            #emptying the lists after every export
            title_list = []
            genre_list = []
            cast_list = []
            crew_list = []
            plot_summary_list = []
            plot_keywords_list = []
            imdb_ratings_list = []
            url_list = []
            count = 0
            if exception_count > 200:
                break
            exception_count += 1
except Exception as e:
    print(e)
    pass
finally:
    driver.close()
