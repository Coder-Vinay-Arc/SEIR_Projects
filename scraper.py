from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys
import time

url = sys.argv[1]

if not url.startswith("http"):
    url = "https://" + url

options = Options()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)

driver.get(url)
time.sleep(5)


print(driver.title)

body = driver.find_element(By.TAG_NAME, "body").text
print(body)

links = driver.find_elements(By.TAG_NAME, "a")
for link in links:
    href = link.get_attribute("href")
    if href:
        print(href)

driver.quit()
