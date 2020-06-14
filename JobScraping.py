

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import csv
import os
import json

from datetime import date

#Extracting todays' date
today=date.today()
Current_Date = today.strftime("%m-%d-%y")

#Initiating driver
browser =webdriver.Chrome(executable_path=r"C:\Users\yoges\Documents\Work\ML (Udemy)\Testing_Web_Scraping\chromedriver.exe")
browser.maximize_window()
browser.get("https://www.amazon.jobs/en/")

#Explicit wait time
WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main-content"]/div[1]/div/div/nav/div[2]/a'))).click()

#Wait until username form is not located
username = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/main/div[2]/div/div[1]/div/div[1]/div/div/input')))
#Enter your username
username.send_keys({Enter your username})

#Click on continue button
browser.find_element_by_xpath('/html/body/main/div[2]/div/div[1]/div/button[1]').click()

#Wait until password form is not located
password = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="signInFormPasswordInputField"]')))
#Enter your passsword
password.send_keys({Enter your password})

#Click on continue button
browser.find_element_by_xpath('//*[@id="signInForm"]/div[6]/button').click()

#Wait until element to be clicked is not located
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[1]/header/div/div/div/nav/div[1]/a[1]/div'))).click()

#Click on the containers
browser.find_element_by_xpath('//*[@id="nav-item-job-categories"]').click()
browser.find_element_by_xpath('//*[@id="nav-item-job-categories"]/div').click()
browser.find_element_by_xpath('//*[@id="nav-item-job-categories"]/div/div').click()

#Wait until element(job categories) to be clicked is not located
WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="nav-item-job-categories"]/div/div/a'))).click()

#Wait until element(Business Intelligence category) to be clicked is not located
WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="job-categories"]/div[2]/div/div/div/div[4]/a/div/div[1]/h3'))).click()

#Wait until element(Sort By) to be clicked is not located
WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="search-results-box"]/div[2]/div/div/div[2]/content/div/div/div[2]/div[1]/div[2]/div/button'))).click()

#Wait until element(recent) to be clicked is not located
WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="recent"]'))).click()

#Click on Seattle, USA 
browser.find_element_by_xpath('//*[@id="search-results-box"]/div[2]/div/div/div[2]/content/div/div/div[1]/div/div[6]/div/div/fieldset/div/button[1]/p').click()
#Wait for 5 seconds to display open positions in SEATTLE
time.sleep(5)

#Create an empty list to hold job titles
dailyJobs= []
#Extract by class job-title
jobTitle = browser.find_elements_by_class_name('job-title')
for html in jobTitle:
    #extract the html content inside the class
    dailyJobs.append(html.get_attribute('innerHTML'))

#Create an empty list to hold job Ids
jobId = []  
locationAndId = browser.find_elements_by_class_name('location-and-id')
for Id in locationAndId:
    #extract the html content inside the class
    jobId.append(re.split('\W',Id.get_attribute('innerHTML'))[-1])

#Wait for 10 seconds
time.sleep(10)
#Click on 2nd page
browser.find_element_by_xpath('//*[@id="search-results-box"]/div[2]/div/div/div[2]/content/div/div/div[2]/div[3]/div[1]/div/div/button[3]').click()
#Wait for 5 seconds
time.sleep(5)
jobTitle = browser.find_elements_by_class_name('job-title')
for html in jobTitle:
    #extract the html content inside the class
    dailyJobs.append(html.get_attribute('innerHTML'))

locationAndId = browser.find_elements_by_class_name('location-and-id')
for Id in locationAndId:
    #extract the html content inside the class
    jobId.append(re.split('\W',Id.get_attribute('innerHTML'))[-1])
  
#Create a dataframe
df = pd.DataFrame(columns=['jobTitle','jobId'])
df['jobTitle']=dailyJobs
df['jobId']=jobId

#Export the df to a csv
df.to_csv(r"latestJobs{}.csv".format(Current_Date),index=False)
browser.quit()
