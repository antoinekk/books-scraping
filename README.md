## Table of Contents
1. [General Info](#general-info)
2. [Installation and run](#installation)

### General Info
***
This script has been developed in order to scrape the information contained on this webite : https://books.toscrape.com/

It allows to scrape the infromation of a book, a category or the whole website.

### Installation and run
***
Please follow the instructions below to use and run the script :
```
1. Clone the repository : $ git clone https://github.com/antoinekk/books-scraping.git <your path>

2. Go into the folder of the repository : $ cd ../path/to/the/folder

3. Create a virtual environement : $ python -m venv env

4. Activate your environement : $ source env/bin/activate

5. Install python modules provided in the "requirements.txt" file by using your terminal

6. Open "books_scraping.py" file with your favorite code editor and go into the main section at the end of the file.

7. Here, you can set up the function you want to execute. For example :
   - If you want to retrieve data for the book catageory "Business", you have to set up this function on the main section :  export_all_data_for_a_category("https://books.toscrape.com/catalogue/category/books/business_35/index.html")
   - If you want to retrieve data for all categories, you have to set up this function : export_data_for_all_categories()

8. Go back into your terminal and run the script : $ python3 books_scraping.py

9. The data will be export directly on the project folder
```
