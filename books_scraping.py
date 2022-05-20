#!/usr/bin/python3


import requests
import csv
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import urllib.request
import os


# function to return book data in a dictionnary by passing book url as parameter
def get_book_data(book_url):
	# check if GET request is working well and retrieve html structure
	response = requests.get(book_url)
	soup = bs(response.text, "html.parser")
	# empty dictionnary to fill in with book data
	book = {}
	if response.ok:
		try:
			# create keys and append values by using BeautifulSoup
			book["title"] = (soup.h1.string).encode("ascii", "ignore")
			book["title"] = book["title"].decode()
			book["category"] = soup.find_all("a")[3].string
			book["product_url"] = book_url
			book["review_rating"] = soup.find_all("p")[2]["class"][1]
			img_url = soup.find_all("img")[0]["src"]
			book["image_url"] = img_url.replace("../..", "https://books.toscrape.com")
			book["product_description"] = (soup.find_all("meta")[2]["content"]).encode("ascii", "ignore")
			book["product_description"] = book["product_description"].decode()
			book["universal_product_code"] = soup.find_all("td")[0].string
			book["price_excluding_tax"] = soup.find_all("td")[2].string.replace("Â", "")
			book["price_including_tax"] = soup.find_all("td")[3].string.replace("Â", "")
			book["availability"] = soup.find_all("td")[5].string
		# the script still running despite a KeyError
		except KeyError:
			pass
	else:
		# error message if the url can't be reachable
		print("No access to" + book_url)
	# dictionnary is returned
	return book


# function to return all books url in a list for a given category
def get_books_url_for_a_category(category_url):
	# empty list to store urls
	books_url = []
	# as long as there are other pages
	while True:
		response = requests.get(category_url)
		soup = bs(response.text, "html.parser")
		footer_element = soup.select_one("li.current")
		# check if there is still a "next page" link at the bottom of the page
		next_page = soup.select_one("li.next > a")
		for h3 in soup.find_all("h3"):
			# retrieve the href, complete the url and add it to the list
			books_url.append(h3.contents[0]["href"].replace("../../..", "https://books.toscrape.com/catalogue"))
		if next_page:
			next_page_url = next_page.get("href")
			category_url = urljoin(category_url, next_page_url)
		else:
			# the function stops if there are no more pages
			break
	# the list is returned
	return books_url


# function to return all books data in a list by passsing category url as parameter
def get_books_data_for_a_category(category_url):
	# call the function to return all books url for the category
	books_to_scrape = get_books_url_for_a_category(category_url)
	books_data = []
	# for each book of the category, call the function to retrieve data
	for book in books_to_scrape:
		data = get_book_data(book)
		books_data.append(data)
	# a list of books data is returned
	return books_data


# function to create a folder with csv file and images for a category
def export_all_data_for_a_category(category_url):
	# call the function to retrieve data for a category
	books = get_books_data_for_a_category(category_url)
	folder_name = books[0]["category"]
	file_name = folder_name + ".csv"
	# check the current path
	script_path = os.getcwd()
	# create a folder
	os.mkdir(folder_name)
	# go into the folder
	os.chdir(folder_name)
	with open(file_name, "w", encoding="utf-8") as file:
		# define header of each column
		header = ["Title", "Category", "Product url", "Review rating", "Image url","Product description",
				  "Universal product code", "Price excluding tax", "Price including tax", "Availability"]
		# write headers to csv file
		writer = csv.writer(file)
		writer.writerow(header)
		for book in books:
			try:
				# retrieve data for each book and write it to the file
				data = [book["title"], book["category"], book["product_url"], book["review_rating"], book["image_url"], book["product_description"],
					    book["universal_product_code"], book["price_excluding_tax"], book["price_including_tax"], book["availability"]]
				writer.writerow(data)
				# retrieve image for each book and save it into the folder
				img_name = book["title"] + ".jpg"
				img = urllib.request.urlretrieve(book["image_url"], img_name )
			# the script still running if there is no image
			except FileNotFoundError:
				pass
	# back to the initial path
	os.chdir(script_path)


# function to return all categories urls in a list
def get_url_for_each_category(home_url):
	response = requests.get(home_url)
	soup = bs(response.text, "html.parser")
	if response.ok:
		urls = []
		for category in soup.find_all("a"):
			href = category["href"]
			if "catalogue/category" in href:
				# append urls to the list
				urls.append("https://books.toscrape.com/" + href)
	# return the list
	return urls[1:]


# function to export all data
def export_data_for_all_categories():
	# call the function to return all categories urls
	all_categories_url = get_url_for_each_category("https://books.toscrape.com/index.html")
	for category_url in all_categories_url:
		# for each category, retrieve and export all the data
		export_all_data_for_a_category(category_url)


# execution of functions
if __name__ == "__main__":
	export_all_data_for_a_category("https://books.toscrape.com/catalogue/category/books/business_35/index.html")
	#export_data_for_all_categories()
