import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

s = Service('/Users/vorrr/chromedriver')

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome(service=s)
   pytest.driver.get('http://petfriends1.herokuapp.com/login')
   pytest.driver.find_element(By.ID, 'email').send_keys('ugugug@mail.ru')
   pytest.driver.find_element(By.ID, 'pass').send_keys('ugugug')
   element = WebDriverWait(pytest.driver, 5).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
   assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "Vormat"


   yield

   pytest.driver.quit()


def test_quantity_my_pets():
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr'))
   )
   quantity = pytest.driver.find_elements(By.XPATH, '//tbody/tr')

   statistics = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text

   number = []
   for i in statistics.split():
      try:
         number.append(int(i))
      except ValueError:
         pass

   assert len(quantity) == number[0]

def test_photo_my_pets():
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr/th/img'))
   )
   images = pytest.driver.find_elements(By.XPATH, '//tbody/tr/th/img')

   photo = 0
   for i in range(len(images)):
      if images[i].get_attribute('src')!='':
         photo +=1

   assert photo >= len(images)//2


def test_data_pets():
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
   )
   info = pytest.driver.find_elements(By.TAG_NAME, 'td')
   data = []
   names, types, age = [], [], []
   for i in info:
      data.append(i.text)

   for n in range(0, len(data), 4):
      names.append(data[n])
      types.append(data[n+1])
      age.append(data[n+2])

   for l in range(len(names)):
      assert names[l] != '' and types[l] != '' and age[l] != ''


def test_names_pets():
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
   )
   info = pytest.driver.find_elements(By.TAG_NAME, 'td')
   data = []
   names, types, age = [], [], []
   for i in info:
      data.append(i.text)

   for n in range(0, len(data), 4):
      names.append(data[n])

   assert len(names) == len(set(names))


def test_identical_pets():
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
   )
   info = pytest.driver.find_elements(By.TAG_NAME, 'td')
   data = []
   for i in info:
      data.append(i.text)

   a = set()

   for n in range(0, len(data), 4):
      pet = (data[n], data[n+1],data[n+2])
      assert pet not in a
      a.add(pet)
