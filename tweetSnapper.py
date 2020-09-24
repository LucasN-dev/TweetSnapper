from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import requests
import re

# browser settings
lang = 'en'
options = Options()
options.add_argument("--lang={}".format(lang))
options.headless = True # hides the chrome windows


driver = webdriver.Chrome(executable_path = "Chrome driver path", chrome_options = options)


# twitter username and url

username = "username"
accountUrl = "https://twitter.com/" + username

print("Looking for new tweets to archive on @" + username + "'s Twitter account...")

while True:

    # retrieve the page
    driver.get(accountUrl)

    # waiting for the page to load (adjust if needed)
    time.sleep(2)

    # check for a pinned tweet
    pinnedTweet = driver.find_elements_by_xpath('//span[.="Pinned Tweet"]')

    # retreive tweets url
    tweets = driver.find_elements_by_css_selector("a[href*='status']")

    tweetsUrls=[]

    for tweet in tweets:
        tweetsUrls.append(tweet.get_attribute('href'))

    # if there is a pinned tweet, we ignore it
    if not pinnedTweet:
        first = 0
    else:
        first = 1

    
    for i in range(first,len(tweetsUrls)):

        tweetUrl = tweetsUrls[i]

        # cleaning the url, removing everything after the tweet id (e.g. /photo/1)
        urlSplit = re.split('(/status/[0-9]*)', tweetUrl)
        tweetUrl = urlSplit[0] + urlSplit[1]

        

        # API call to check if an archive already exists
        # documentation : https://archive.readme.io/docs/website-snapshots
        request = "https://archive.org/wayback/available?url=" + tweetUrl
        time.sleep(2) # waiting for the API response, can be adjusted
        result = requests.get(request).json()

        alreadyArchived = result['archived_snapshots']

        if not alreadyArchived:

            # we create a snapshot of the page using selenium, I didn't find any working API

            print("One recent tweet is not archived yet\nCreating snapshot...")
            saveUrl = "https://web.archive.org/save/"
            driver.get(saveUrl)
            time.sleep(3)  # waiting for the page to load (adjust if needed)
            urlField = driver.find_element_by_name('url')
            urlField.send_keys(tweetUrl)
            templist = driver.find_elements_by_xpath("//*[@type='submit']")
            driver.find_elements_by_xpath("//*[@type='submit']")[1].click()

            try:
                # waiting for the "done" icon to show up
                timeoutDelay = 90 # can be adjusted

                element = WebDriverWait(driver, timeoutDelay).until(ec.presence_of_element_located((By.CLASS_NAME, "iconochive-Done")))
                time.sleep(1)
                links = driver.find_elements_by_css_selector("a[href*='web']")
                print("Tweet archived succesfully! It can be found at the following address:")
                print(links[0].get_attribute('href'))
            except Exception:
                print("Error: timeout")

    # delay before next check, can be adjusted
    delay = 10
    time.sleep(delay)
    