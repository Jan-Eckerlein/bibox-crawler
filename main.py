from asyncio.windows_events import NULL
from fetch_image_urls import fetch_image_urls
import json
import re

if __name__ == "__main__":
    option = NULL
    
    # Opening JSON file
    with open('config.json') as json_file:
        config = json.load(json_file)
    
    print("Welcome to the BiBox Webcrawler\nThere are following options:\n")
    option = input("Press:\n1: Fetch images from Bibox\n2: Generate PDF from fetched images\n")
    
    if option == '1':
        fetch_image_urls(config)
    
    if option == '2':
        print("this function is WIP")