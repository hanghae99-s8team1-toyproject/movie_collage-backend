import certifi
from pymongo import MongoClient
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from lib2to3.pgen2 import driver
import requests
from bs4 import BeautifulSoup
import time
import ssl
from dotenv import load_dotenv
import os

load_dotenv()
mongodbUri = os.environ.get('mongodbUri')

ca = certifi.where()
client = MongoClient(mongodbUri, tlsCAFile=ca)
db = client.indieground


ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(
    'https://indieground.kr/indie/libraryList.do?setYear=2021', headers=headers, verify=False)

_URL_MOVIE_LIST = "https://indieground.kr/indie/libraryList.do?setYear=2021"


def set_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")  # 웹 브라우저를 시각적으로 띄우지 않는 headless chrome 옵션
    options.add_argument("lang=ko_KR")  # 언어 설정
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging"]
    )  # 개발도구 로그 숨기기
    options.add_argument("start-maximized")  # 창 크기 최대로
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


driver = set_chrome_driver()
driver.get(_URL_MOVIE_LIST)

# 더보기 버튼 끝까지 클릭
while True:
    try:
        wait = WebDriverWait(driver, 10, 10)
        button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/section/section/section/div[3]/div/div[4]/button")))
        button.click()
        time.sleep(10)
    except:
        break

soup = BeautifulSoup(driver.page_source, 'html.parser')

movies = soup.select('#cms-content > div.library_wrap > div > div')

for movie in movies:
    title = movie.find("h3", {"class": "kr_title"}).get_text()
    keyword = movie.find("p", {"class": "tag"}).get_text()
    genre = movie.find("span", {"class": None}).text.split("/")[0]
    director = movie.find("p", {"class": "director"}
                          ).text.split(":")[1].strip()
    actor = movie.find("p", {"class": "actor"}).text.split(":")[1].strip()
    thumbnail = "https://indieground.kr/" + \
        movie.find("img", {"class": None})["src"]
    movie_url = "https://indieground.kr/" + \
        movie.find("a", {"class": None})["href"]
    movieUrl_seq = int(movie_url.split("=")[1].split("&")[0])

    doc = {
        'title': title,
        'keyword': keyword,
        'genre': genre,
        'director': director,
        'actor': actor,
        'thumbnail': thumbnail,
        'movie_url': movie_url,
        'movieUrl_seq': movieUrl_seq
    }
    # db.movies.insert_one(doc)
