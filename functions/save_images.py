import json
import requests

def save_images():
    # Opening JSON file
    with open('storage/pages.json') as json_file:
        image_urls = json.load(json_file)
        
    # print(image_urls)
    for page in image_urls:
        element = image_urls[page]
        URL = element["url"]
        print(URL)
        filepath = 'images/' + element['name'] + '.png'
        response = requests.get(URL)
        open(filepath, "wb").write(response.content)