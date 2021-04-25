from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pandas as pd

path='C:\\Users\\Suprakash\\Anaconda3\\chromedriver.exe'

browser=webdriver.Chrome(executable_path=path)

#dest_city=input('Enter the destination city')
#min=int(input("Enter the minimum price"))
#max=int(input("Enter the maximum price"))

dest_city="Leh" # Name of the destination city
min=500 
max=3000

browser.get('https://www.google.co.in/travel/hotels?tcfs=UgJgAQ&ts=CAESABogCgIaABIaEhQKBwjlDxAEGBMSBwjlDxAEGBQYATICEAAqDwoLKAFKAiABOgNJTlIaAA&ved=0CAAQ5JsGahgKEwiYlsCE3oXwAhUAAAAAHQAAAAAQlgw&ictx=3&rp=OAH4AQE')
box=browser.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div[1]/div[1]/div[2]/div[1]/c-wiz/div/div[1]/div[2]/div[1]/div/div[1]/input')
box.click()
box.send_keys(dest_city) # Search for the box to enter the destination city name
box.send_keys(Keys.ENTER)

time.sleep(10)
hotels=[]
price=[]
c=1

while (c<=10): # Loading the information of the top 10 pages only
	try:
		pg=browser.page_source
		soup=BeautifulSoup(pg,'lxml')

		info_hotels=soup.findAll('h2',{'class':"BgYkof ogfYpf ykx2he"}) # Search for hotel names

		for i in info_hotels:
			hotels.append(i.text)

		info_price=soup.findAll('span',{'class':"Q01V4b W2A2sb"}) # Search for the price

		for i in info_price:
			j=i.text
			idx=j.index('P') # To just extract the price and remove the extra text that starts with a P
			p=int(j[1:idx].replace(",","")) 
			price.append(p)

		# Since the xpath is different for the next button on the first page and rest of the pages both xpaths are provided in try error block
		if(c==1):
			next=browser.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div[1]/div[1]/div[2]/main/div/div[2]/c-wiz/div[8]/div/div/span')
		else:
			next=browser.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div[1]/div[1]/div[2]/main/div/div[2]/c-wiz/div[8]/div[2]/div/span')
		next.click()
		time.sleep(10)
		c=c+1

	except:
		break

price_list=[]

for i,j in enumerate(price): # The price scraped was repeated twice so keeping only one of them
	if(i%2==0):
		price_list.append(j)

print("Matching hotels :-")

for i,j in zip(hotels,price_list): #Scraping the hotels that meet the criteria
	if(j>=min and j<=max):
		print(i+" --> "+str(j))

browser.quit()

