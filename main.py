import time
import io
import csv
from selenium import webdriver

address = input('Enter the URL: ')

def getComments(url):
    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    time.sleep(3)

    title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
    commentary = driver.find_element_by_xpath('//*[@id="comments"]')

    driver.execute_script("arguments[0].scrollIntoView();", commentary)
    time.sleep(5)

    latest_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        time.sleep(3)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == latest_height:
            break
        latest_height = new_height

    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    user_elements = driver.find_elements_by_xpath('//*[@id="author-text"]')
    comments = driver.find_elements_by_xpath('//*[@id="content-text"]')

    print(f'YouTube Video: {title}')

    with io.open('data.csv', 'w', newline='', encoding="utf-16") as file:
        writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
        writer.writerow(["User", "Comment"])
        for username, comment in zip(user_elements, comments):
            writer.writerow([username.text, comment.text])

    driver.close()

if __name__ == '__main__':
  getComments(address)