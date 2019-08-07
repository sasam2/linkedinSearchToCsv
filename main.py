#python 2.7

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

if len(sys.argv) != 5:
    print "Usage: python main.py <email> <password> <search_url> <filename>"
    exit(1)
email = sys.argv[1]
password = sys.argv[2]
url = sys.argv[3]
filename = sys.argv[4]


driver = webdriver.Firefox()

#wait for login page to be available
driver.get("https://www.linkedin.com/")
sigin_form_xpath="//Form[@action=\"https://www.linkedin.com/uas/login-submit\"]"
signInForm = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,sigin_form_xpath)))
#print signInForm.get_attribute("class")
print "Login form loaded."

#get login elements
emailInput = driver.find_element_by_xpath("//Input[@name=\"session_key\"]")
#print emailInput.get_attribute("class")
passwordInput = driver.find_element_by_xpath("//Input[@name=\"session_password\"]")
#print passwordInput.get_attribute("class")
button = driver.find_element_by_xpath("//Button[text()=\"Sign in\"]")
#print button.get_attribute("class")
print "Got login elements."

#log in
emailInput.send_keys(email)
passwordInput.send_keys(password)
button.click()
print "Logged in."

#set search url
driver.get(url)
print "Get search page."


# create and init csv results file
file_wr = open(filename, "w")
file_wr.write("name;title;location;current_position\n")
print "Wrote header to csv file."

#read all results
next_button_disabled = None
while not next_button_disabled: #if next button was enabled, read next page results

    # wait for result list to be available
    results_list_xpath = "//ul[contains(@class,'search-results__list')]"
    results_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, results_list_xpath)))

    # scroll to load all page w/ search results
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3)")
    time.sleep(5)
    driver.execute_script("window.scrollTo(document.body.scrollHeight/3, 2*document.body.scrollHeight/3)")
    time.sleep(5)
    driver.execute_script("window.scrollTo(2*document.body.scrollHeight/3, document.body.scrollHeight)")
    print "Loaded search page, by scrolling."

    ##get result list from page
    #results_list = driver.find_element_by_xpath("//ul[contains(@class,'search-results__list')]")
    results = results_list.find_elements_by_tag_name("li")
    for res in results: #for each result
        print ""
        csv_line = ""
        name_elem = res.find_element_by_tag_name("h3") #get name
        name_list = name_elem.text.split("\n")
        name = name_list[0]
        print name
        csv_line += name+";"
        info_list = res.find_elements_by_tag_name("p") #get infos
        for info in info_list:
            print info.text
            csv_line += info.text+";"
        csv_line += "\n"
        #print csv_line
        file_wr.write(csv_line.encode('utf-8'))
        print "Wrote line to csv file."
    # get next button
    next_button_xpath = "//button[contains(@class,'artdeco-pagination__button--next')]"
    next_button = driver.find_element_by_xpath(next_button_xpath)
    next_button_disabled = next_button.get_attribute("disabled") #check if next button is disabled - meaning no more pages
    print next_button_disabled
    next_button.click() #go to next page if the case
    print "Clicked \"next\" button (if enabled, goes to next page)."
    time.sleep(5) #wait for next page to load
file_wr.close()
driver.close()

print "end"