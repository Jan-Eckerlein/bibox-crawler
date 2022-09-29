# These are the imports to be made
import time
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import json
import re

def fetch_image_urls(config):

    # url of google news website
    input_success = False
    while not input_success:
        url = input("URL in Config is: " + config['url'] + "\nPress ENTER to use this or enter your BiBox url:\n")
        if url == '': 
            url = config['url']
            break
        
        url_regex = re.search(r'https://bibox2\.westermann\.de/book/[0-9]+/page/1', url)
        if url_regex:
            input_success = True
        else:
            print("The provided URL is not valid")
    
    username = input("Username in Config is: " + config['username'] + "\nPress ENTER to use this as your BiBox User or enter your BiBox Username:\n ")
    password = ''
    if username == '':
        username = config['username']
        password = config['password']
    else:
        password = input("Please Enter your Password\n")
    
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
    
    # to open the url in the browser
    print('Start webdriver')
    driver.get(url)

    time.sleep(3)

    print('Login')
    user_name = driver.find_element(By.ID, "account")
    user_pwd = driver.find_element(By.ID, "password")
    button_login = driver.find_element(By.NAME, "action")
    user_name.send_keys(username)
    user_pwd.send_keys(password)
    button_login.click()

    time.sleep(5)
    
    print('Force all Images to load')
    last_page = False
    waited = 0
    while last_page == False:
        try:
            next = driver.find_element(By.XPATH, "//button[@title= 'weiterblättern' and contains(@class,'visible')]")
            next.click()
        except NoSuchElementException:
            if waited >= 5:
                waited += 0.25
            else:
                print ("last page reached")
                last_page = True


    # Gets all the logs from performance in Chrome
    print('log driver network log')
    logs = driver.get_log("performance")
    
    # Opens a writable JSON file and writes the logs in it
    with open("storage/network_log.json", "w", encoding="utf-8") as f:
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
    print('read storage/network_log.json and convert to DICT')
    json_file_path = "storage/network_log.json"
    with open(json_file_path, "r", encoding="utf-8") as f:
        logs = json.loads(f.read())
  
    # Iterate the logs
    print('Extract urls')
    url_dict = {}
    for log in logs:
        # Except block will be accessed if any of the
        # following keys are missing.
        try:
            # URL is present inside the following keys
            url = log["params"]["request"]["url"]
            if re.search("\/bookpages\/.*\.png", url):
                match = re.search("(?<===/)[a-zA-Z0-9]*(?=.png)", url)
                if match:
                    page = match.group()
                    url_dict[page] = {"name": page, "url": url}
                
        except Exception as e:
            pass
    
    print('Save url DICT into storage/pages.json')
    pages_file_path = "storage/pages.json"
    with open(pages_file_path, 'w') as convert_file:
     convert_file.write(json.dumps(url_dict))