from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

executable_path = "C:\\Users\\Viraj Gawde\\Downloads\\chromedriver_win322\\chromedriver.exe"
driver = webdriver.Chrome(executable_path = executable_path)

driver.get("https://vedabase.io/en/library/sb/1/1/1/")

content = driver.page_source
soup = BeautifulSoup(content)

print(soup.find("div", {"id": "bb13392"}).find("h1"))


driver.close()