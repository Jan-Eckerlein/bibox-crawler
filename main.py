from asyncio.windows_events import NULL
from functions.fetch_image_urls import fetch_image_urls
from functions.save_images import save_images 
from functions.create_pdf import create_pdf
import json
import os
import re

if __name__ == "__main__":
    # create Folders:
    dirs = ["./output", "./images"]
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
    
    option = NULL
    
    # Opening JSON file
    with open('config.json') as json_file:
        config = json.load(json_file)
    
    print("Welcome to the BiBox Webcrawler\nThere are following options:\n")
    option = input("Press:\nENTER: Execute all necessary commands to create the PDF\n    1: Crawl images URLS from Bibox\n    2: Download all images \n    3: Generate PDF from fetched images\n")
    
    if option == '1':
        fetch_image_urls(config)
    
    if option == '2':
        save_images()
    
    if option == '3':
        create_pdf()