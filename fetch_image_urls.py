# These are the imports to be made
import time
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import json
import re

def fetch_image_urls ():
    
    # path of the chromedriver we have just downloaded
    PATH = r"C:\chromedriver"

    # Enable Performance Logging of Chrome.
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    # Create the webdriver object and pass the arguments
    options = webdriver.ChromeOptions()

    # Chrome will start in Headless mode
    options.add_argument('headless')

    # Ignores any certificate errors if there is any
    options.add_argument("--ignore-certificate-errors")

    # Startup the chrome webdriver with executable path and
    # pass the chrome options and desired capabilities as
    # parameters.

    driver = webdriver.Chrome(
        PATH,
        chrome_options=options,
        desired_capabilities=desired_capabilities
    )

    # url of google news website
    url = 'https://bibox2.westermann.de/shelf/'
    
    # Opening JSON file
    with open('user.json') as json_file:
        user_data = json.load(json_file)

    # to open the url in the browser
    driver.get(url)

    time.sleep(3)

    user_name = driver.find_element(By.ID, "account")
    user_pwd = driver.find_element(By.ID, "password")
    button_login = driver.find_element(By.NAME, "action")
    user_name.send_keys(user_data['name'])
    user_pwd.send_keys(user_data['password'])
    button_login.click()

    time.sleep(3)
    book = driver.find_element(By.TAG_NAME, "app-shelf-item")
    book.click()
    bookButton = driver.find_element(By.CLASS_NAME, "book-action")
    # time.sleep(2)
    bookButton.click()
    # print(books)
    
    time.sleep(5)
    
    last_page = False
    waited = 0
    while last_page == False:
        try:
            print("next page")
            next = driver.find_element(By.XPATH, "//button[@title= 'weiterblättern' and contains(@class,'visible')]")
            next.click()
        except NoSuchElementException:
            if waited >= 5:
                waited += 0.25
            else:
                print ("no next page")
                last_page = True


    # Gets all the logs from performance in Chrome
    logs = driver.get_log("performance")
    
    # Opens a writable JSON file and writes the logs in it
    with open("network_log.json", "w", encoding="utf-8") as f:
        f.write("[")
  
        # Iterates every logs and parses it using JSON
        for log in logs:
            network_log = json.loads(log["message"])["message"]
  
            # Checks if the current 'method' key has any
            # Network related value.
            if("Network.response" in network_log["method"]
                    or "Network.request" in network_log["method"]
                    or "Network.webSocket" in network_log["method"]):
  
                # Writes the network log to a JSON file by
                # converting the dictionary to a JSON string
                # using json.dumps().
                f.write(json.dumps(network_log)+",")
        f.write("{}]")
  
    print("Quitting Selenium WebDriver")
    driver.quit()
  
    # Read the JSON File and parse it using
    # json.loads() to find the urls containing images.
    json_file_path = "network_log.json"
    with open(json_file_path, "r", encoding="utf-8") as f:
        logs = json.loads(f.read())
  
    url_dict = {}
  
    # Iterate the logs
    for log in logs:
  
        # Except block will be accessed if any of the
        # following keys are missing.
        try:
            # URL is present inside the following keys
            url = log["params"]["request"]["url"]
            if re.search("\/bookpages\/.*\.png", url):
                print(url)
                match = re.search("(?<===/)[a-zA-Z0-9]*(?=.png)", url)
                if match:
                    page = match.group()
                    url_dict[page] = url
                
        except Exception as e:
            pass
    
    print(url_dict)
    
    pages_file_path = "pages.json"
    with open(pages_file_path, 'w') as convert_file:
     convert_file.write(json.dumps(url_dict))