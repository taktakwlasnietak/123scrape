from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import sys
import time
from selenium.common.exceptions import NoSuchElementException


#mirrors
def embed_link(mirrorsAmount):
	x = 0
	global embeds_array
	embeds_array = []
	embed1 = driver.find_element_by_class_name("tab-content")
	embed = embed1.find_element_by_tag_name("iframe").get_attribute("src")
	embeds_array.append(embed)
	while x <= mirrorsAmount:
		try:
			mirrorlinkA = driver.find_elements_by_class_name("server_play")[x]
			mirrorlinkB = mirrorlinkA.find_element_by_tag_name("a")
			mirrorlink = mirrorlinkB.get_attribute("href")
			driver.get(mirrorlink) 
			embed1 = driver.find_element_by_class_name("tab-content")
			embed = embed1.find_element_by_tag_name("iframe").get_attribute("src")
			embeds_array.append(embed)
			x+=1
		except:
			embed = "[[brak]]"
			embeds_array.append(embed)
			x+=1
			pass
	return embeds_array


#genres, actor, director, country
def mvici_left():
	x = 0
	global left_array
	left_array = []
	while x <= 3:
		try:
			mvleft1 = driver.find_element_by_class_name("mvici-left")
			mvleft2 = mvleft1.find_elements_by_tag_name("p")[x]
			mvleft = mvleft2.find_element_by_tag_name("a")
			mvleft = mvleft.text
			left_array.append(mvleft)
			x+=1
		except:
			mvleft = "[[brak]]"
			left_array.append(mvleft)
			x+=1
			pass
	return left_array
	
#movie, production, duration, release
def mvici_right():
	x = 0
	global right_array
	right_array = []
	while x <= 3:
		try:
			mvright1 = driver.find_element_by_class_name("mvici-right")
			mvright = mvright1.find_elements_by_tag_name("p")[x]
			mvright = mvright.text
			right_array.append(mvright)
			x+=1
		except:
			mvright = "[[brak]]"
			right_array.append(mvright)
			x+=1
			pass
	return right_array
	
#year in title
def year_pattern(text):
	if len(text) != 4:
		return False
	for i in range(0,4):
		if not text[i].isdigit():
			return False
	return True

driver = webdriver.Chrome('/home/krzys/Downloads/chromedriver')

lines = [line.rstrip('\n') for line in open('list')]

def scrape():
	x = 0
	#global embeds_array
	for l in lines:
		try:
			site = lines[x]
			driver.get(site)

			embed_link(3)
			embeds = ' !! '.join(embeds_array)
			#print embeds
					
			#title
			try:
				titleA = driver.find_element_by_class_name("mvic-desc")
				title = titleA.find_element_by_tag_name("h3")
				title = title.text
			except:
				title = "[[brak]]"
				pass			
			#removing year from title if it is there
			for i in range(len(title)):
				year = title[i:i+4]
				if year_pattern(year):
					delete_year = title.split(("("),1)[0]
					title = delete_year
				else:
					title = title
					
			#description
			try:
				desc = driver.find_element_by_class_name("desc")
				desc = desc.text
				description = desc.strip("\n")
			except:
				description = "[[brak]]"
			#print desc
					
			#poster image
			try:
				poster = driver.find_element_by_xpath("//meta[@property='og:image']").get_attribute("content")
			except:
				poster = "[[brak]]"
					
			#genres, actor, director, country
			mvici_left()
			leftSide = ' ## '.join(left_array)
			#print leftSide
			
			#movie, production, duration, release
			mvici_right()
			year = right_array[3]
			year = year.replace("Release: ","")
			rightSide = ' ## '.join(right_array)
			#print rightSide
			
			print("%s ## %s ## %s ## %s ## %s ## %s ## %s" % (year, title, description, leftSide, rightSide, poster, embeds))
				
			x+=1
		except:
			print "ten wyzej do poprawki"
			x+=1
			pass

scrape()
