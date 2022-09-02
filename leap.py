from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import os
import time
import re
import smtplib
from email.message import EmailMessage
from random import randint


LEAPCARD_PASSWORD = os.environ.get('LEAPCARD_PASSWORD')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")

# change this value to change what balance at which you receive an email
min_amount_for_two_journies = 2

options = webdriver.ChromeOptions()
# uncomment this line to run script without a user interface 
# options.add_argument('headless')

driver = webdriver.Chrome(executable_path=r"Path to driver\chromedriver.exe", options=options)
driver.get("https://transportforireland.b2clogin.com/transportforireland.onmicrosoft.com/b2c_1a_signup_signin/oauth2/v2.0/authorize?client_id=90e37d10-35db-4e50-a0d4-26c7dfc92236&redirect_uri=https%3A%2F%2Fwww.leapcard.ie&response_type=code%20id_token&scope=openid%20profile%20offline_access%20https%3A%2F%2Ftransportforireland.onmicrosoft.com%2Fleapcard%2Fread%20https%3A%2F%2Ftransportforireland.onmicrosoft.com%2Fleapcard%2Fwrite&state=OpenIdConnect.AuthenticationProperties%3DrbK2uO0FjPwgqbhFwF3mojimULDaitBzejzR94FRl3QkbkAYjt0IPtHpfU2KGbDT78od_rmnVZywRhWw2aWJHw1ujkpjhC1ApSrevzUO1nsNWPudDZYPAo_S2HKCbdf82wDcD_4fRv_0P--iz1e9-nxk2HxrgIykJISMA3HgN8knpqJLTMGqaP6wYIlElWoQuSMK9DQgYydhgLxjMgXxJ0GR9xnf9KfEBr7MRohRjCOM9Pf8wAK2fqDJySLDhmVu-BE41sIZ6p8UY8h1RsapD2BW_38&response_mode=form_post&x-client-SKU=ID_NET461&x-client-ver=5.3.0.0")
time.sleep(randint(1, 3))
usernameLoginBox = driver.find_element(By.ID, "signInName")
usernameLoginBox.send_keys(EMAIL_ADDRESS)
# time.sleep(randint(1, 3))
passwordLoginBox = driver.find_element(By.ID, "password")
passwordLoginBox.send_keys(LEAPCARD_PASSWORD)
time.sleep(randint(1, 3))
passwordLoginBox.send_keys(Keys.RETURN)
time.sleep(randint(1, 3))
sign_in_btn  = driver.find_element(By.LINK_TEXT, 'Sign In')
sign_in_btn.click()
time.sleep(randint(3, 5))
selectBox = driver.find_element(By.ID, "ContentPlaceHolder1_TabContainer2_MyCardsTabPanel_ddlMyCardsList")
selectBox.click()

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
matches = soup.find_all(string=re.compile(r"(\d\d\.\d\d)|(\d\.\d\d)"))
amount_on_card = matches[len(matches)-1]

euro_float = float(amount_on_card)

if(euro_float<=min_amount_for_two_journies):
  msg = EmailMessage()
  msg["Subject"] = "Leap Card Balance"
  msg["From"] = EMAIL_ADDRESS
  msg["To"] = EMAIL_ADDRESS
  msg.set_content(f"You should top up, you have €{euro_float} on your card")

  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
    smtp.send_message(msg)
else:
  print(f"You have {euro_float} euro on your card")

driver.close()




