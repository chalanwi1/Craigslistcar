from bs4 import BeautifulSoup
import lxml
import requests
import pandas as pd

# Web page being scraped
base_url = 'https://oklahomacity.craigslist.org/search/sss?query=car&sort=rel'

# Send get request for http
page = requests.get(base_url)

# If response is good(200), render page
if page.status_code == requests.codes.ok:
    bs = BeautifulSoup(page.text, 'lxml')

# Get list of all items in container
car_list = bs.find(class_='rows').find_all('li')

# Create dictionary for scraped data
data = {
    'Date': [],
    'Title': [],
    'Price': [],
    'Link': [],
}

# Loop through car list and get each date, title, price, link
for car_item in car_list:

    date = car_item.find('time').text
    if date:
        data['Date'].append(date)
    else:
        data['Date'].append('NA')

    title = car_item.find(class_='result-title hdrlnk').text
    if title:
        data['Title'].append(title)
    else:
        data['Title'].append('NA')

    price = car_item.find(class_='result-price').text
    if price:
        data['Price'].append(price)
    else:
        data['Price'].append('NA')

    link = car_item.find(class_='result-title hdrlnk').get('href')
    if link:
        data['Link'].append(link)
    else:
        data['Link'].append('NA')

# Convert data dictionary to panda data frame
final = pd.DataFrame(data, columns=['Date', 'Title', 'Price', 'Link'])

# Start list number at 1
final.index += 1

# Write result to csv file
final.to_csv('craigslist_cars_file.csv', index=False, sep=',', encoding='utf-8')

print(final)
