from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pandas as pd

path='C:\\Users\\Suprakash\\Anaconda3\\chromedriver.exe'

browser=webdriver.Chrome(executable_path=path)

#source_city=input('Enter the source city')
#dest_city=input('Enter the destination city')

source_city="Mumbai"
dest_city="New Delhi"

source_city=source_city.lower()
dest_city=dest_city.lower()

source_city=source_city.replace(" ","_")
dest_city=dest_city.replace(" ","_")


url='https://www.makemytrip.com/flights/'+source_city+"-"+dest_city+"-cheap-airtickets.html" # To create the url
browser.get(url)
time.sleep(10)

# Scroll till the end of the page to load the contents fully
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

pg=browser.page_source
soup=BeautifulSoup(pg,'lxml')

fl_details=[]
fl_timings=[]
fl_price=[]

# To extract the flight details, timings and price
info=soup.findAll('div',{'class':'fli-list one-way'})
for i in info:
    flight_details=i.find('div',{'class':"pull-left airline-info"})
    flight_timings=i.find('div',{'class':"timing-option"})
    flight_price=i.find('div',{'class':'pull-left make_relative price'})
    fl_details.append(flight_details.text)
    fl_timings.append(flight_timings.text[1:])
    fl_price.append(flight_price.text[2:])

print(fl_details)
print(fl_timings)
print(fl_price)


data={'Flight name':fl_details,'Filght timimgs':fl_timings,'Flight price':fl_price}
df=pd.DataFrame(data)
df.to_csv("Flight_Info.csv") #Save the information in a csv file

print("Places of interest :-")
browser.get('https://www.google.co.in/travel/things-to-do?dest_src=ut&tcfs=UgJgAQ&ved=0CAUQyJABahcKEwjAr-HJxYXwAhUAAAAAHQAAAAAQCw&ictx=3')
time.sleep(5)
box=browser.find_element_by_xpath('//*[@id="oA4zhb"]') # Box to enter the destination city name
box.click()
box.send_keys(dest_city)
box.send_keys(Keys.ENTER)
time.sleep(5)

des=browser.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div/div/div[1]/div[2]/c-wiz/div/div[1]/div/div/easy-img/span/div/span').text
print(des)
print()

pg=browser.page_source
soup=BeautifulSoup(pg,'lxml')
reg=soup.find('div',{'class':"kQb6Eb"})
names=reg.findAll('div',{'class':"rbj0Ud"}) # To extract the names of the top tourist places
info=reg.findAll('div',{'class':"nFoFM"}) # Extract the description of the places

for i,j in zip(names,info):
	print(i.text+" -> "+j.text)


