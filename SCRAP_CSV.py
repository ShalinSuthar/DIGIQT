#Reference - https://www.medium.com
import pandas as pd
import requests 
from bs4 import BeautifulSoup
url = 'https://www.imdb.com/chart/top'
url_text = requests.get(url).text
soup = BeautifulSoup(url_text, 'html.parser')
template = 'https://www.imdb.com%s'
title_links = [template % a.attrs.get('href') for a in soup.select( 'td.titleColumn a' )]

movie_name = (page_soup.find("div",{ "class":"title_wrapper" }).get_text( strip=True ).split('|')[0]).split('(')[0]
year = ((page_soup.find("div",{ "class":"title_wrapper" }).get_text( strip=True ).split('|')[0]).split('(')[1]).split(')')[0]
rating = page_soup.find("span",{"itemprop":"ratingValue"}).text
vote_count = page_soup.find("span",{"itemprop":"ratingCount"}).text
subtext= page_soup.find("div",{ "class":"subtext" }).get_text( strip=True ).split('|' )

if len(subtext) < 4:
    censor_rating = "No rating"
    movie_length = subtext[0]
    genre_list = subtext[1].split(',')
    while len(genre_list) < 4:
        genre_list.append(' ')
    release_date_and_country = subtext[2].split('(')
    release_date = release_date_and_country[0]
else:
    censor_rating = subtext[0]
    movie_length = subtext[1]
    genre_list = subtext[2].split(',')
while len(genre_list) < 4:
    genre_list.append(' ')
release_date_and_country = subtext[3].split('(')
release_date = release_date_and_country[0]

# Getting the movie summary
summary = page_soup.find("div", {"class":"summary_text"}).get_text( strip=True ).strip()# Getting the credits for the director and writers
credit_summary = []
for summary_item in page_soup.find_all("div",{ "class" : "credit_summary_item" }):
    credit_summary.append(re.split( ',|:|\|' ,summary_item.get_text( strip=True )))
stars = credit_summary.pop()[1:4]
writers = credit_summary.pop()[1:3]
director = credit_summary.pop()[1:]
while len(stars) < 3:
    stars.append(" ")
while len(writers) < 2:
    writers.append(" ")
writer_1, writer_2 = writers
writer_1 = writer_1.split('(')[0]
writer_2 = writer_2.split('(')[0]

box_office_details = []
box_office_dictionary = {'Country':'','Language':'','Budget':'', 'Opening Weekend USA':'','Gross USA':'','Cumulative Worldwide Gross':'','Production Co':''}
for details in page_soup.find_all("div",{"class":"txt-block"}):
    detail = details.get_text(strip=True).split(':')
if detail[0] in box_office_dictionary:
    box_office_details.append(detail)
for detail in box_office_details:
    if detail[0] in box_office_dictionary:
        box_office_dictionary.update({detail[0] : detail[1]})
country = box_office_dictionary['Country'].split("|")
while len(country) < 4: 
   country.append(' ')
language = box_office_dictionary['Language'].split("|")
while len(language) < 5:
    language.append(' ')
budget = box_office_dictionary['Budget'].split('(')[0]
opening_week_usa = ','.join((box_office_dictionary['Opening Weekend USA'].split(' ')[0]).split(',')[:-1])
gross_usa = box_office_dictionary['Gross USA']
gross_worldwide = box_office_dictionary['Cumulative Worldwide Gross'].split(' ')[0]
production_list = box_office_dictionary['Production Co'].split('See more')[0]
production = production_list.split(',')
while len(production) < 4:
    production.append(" ")


dataframe_columns = [ 'ranking', 'movie_name', 'url', 'year', 'rating', 'vote_count', 'summary', 'production_1', 'production_2', 'production_3', 'director', 'writer_1', 'writer_2', 'star_1', 'star_2', 'star_3', 'genre_1', 'genre_2', 'genre_3', 'genre_4','release_date', 'censor_rating', 'movie_length', 'country_1', 'country_2', 'country_3', 'country_4', 'language_1', 'language_2', 'language_3', 'language_4', 'language_5', 'budget', 'gross_worldwide', 'gross_usa','opening_week_usa']
dataframe = pd.DataFrame(columns=dataframe_columns)

for i in range(0, len(imdb_movie_list)):
    dataframe.at[i,'ranking'] = imdb_movie_list[i]['ranking']
    dataframe.at[i,'movie_name'] = imdb_movie_list[i]['movie_name']
    dataframe.at[i,'url'] = imdb_movie_list[i]['url']
    dataframe.at[i,'year'] = imdb_movie_list[i]['year']
    dataframe.at[i,'rating'] = imdb_movie_list[i]['rating']
    dataframe.at[i,'vote_count'] = imdb_movie_list[i]['vote_count']
    dataframe.at[i,'summary'] = imdb_movie_list[i]['summary']
    dataframe.at[i,'production_1']= imdb_movie_list[i]['production'][0]
    dataframe.at[i,'production_2']= imdb_movie_list[i]['production'][1]
    dataframe.at[i,'production_3']= imdb_movie_list[i]['production'][2]
 
    dataframe.at[i,'director'] = imdb_movie_list[i]['director'][0]
    dataframe.at[i,'writer_1'] = imdb_movie_list[i]['writers'][0]
    dataframe.at[i,'writer_2'] = imdb_movie_list[i]['writers'][1]
    dataframe.at[i, 'star_1'] = imdb_movie_list[i]['stars'][0]
    dataframe.at[i, 'star_2'] = imdb_movie_list[i]['stars'][1]
    dataframe.at[i, 'star_3'] = imdb_movie_list[i]['stars'][2]
    dataframe.at[i,'genre_1'] = imdb_movie_list[i]['genres'][0]
    dataframe.at[i,'genre_2'] = imdb_movie_list[i]['genres'][1]
    dataframe.at[i,'genre_3'] = imdb_movie_list[i]['genres'][2]
    dataframe.at[i,'genre_4'] = imdb_movie_list[i]['genres'][3]
    dataframe.at[i,'release_date'] = imdb_movie_list[i]['release_date']
    dataframe.at[i,'censor_rating'] = imdb_movie_list[i]['censor_rating']
    dataframe.at[i,'movie_length'] = imdb_movie_list[i]['movie_length']
    dataframe.at[i,'country_1'] = imdb_movie_list[i]['country'][0]

    dataframe.at[i,'country_2'] = imdb_movie_list[i]['country'][1]
    dataframe.at[i,'country_3'] = imdb_movie_list[i]['country'][2]
    dataframe.at[i,'country_4'] = imdb_movie_list[i]['country'][3]
    dataframe.at[i,'language_1'] = imdb_movie_list[i]['language'][0]
    dataframe.at[i,'language_2'] = imdb_movie_list[i]['language'][1]
    dataframe.at[i,'language_3'] = imdb_movie_list[i]['language'][2]
    dataframe.at[i,'language_4'] = imdb_movie_list[i]['language'][3]
    dataframe.at[i,'language_5'] = imdb_movie_list[i]['language'][4]
    dataframe.at[i,'budget'] = imdb_movie_list[i]['budget']
    dataframe.at[i,'gross_worldwide'] = imdb_movie_list[i]['gross_worldwide']
    dataframe.at[i,'gross_usa'] = imdb_movie_list[i]['gross_usa']
    dataframe.at[i,'opening_week_usa'] = imdb_movie_list[i]['opening_week_usa']
dataframe = dataframe.set_index(['ranking'], drop=False)
dataframe.to_csv('imdb_movies_data.csv')
