from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_link_text_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Empty list that stores link text info dicts
    link_text_info = []
    
    def process_a_tag(a):
        link_data = {}

        # Get the link's web address and link text content
        link_data['Web address'] = url
        link_data['Link text content'] = a.get_text()

        # Calculate pass/fail score based on specific criteria
        link_data['Pass/fail score'] = calculate_score(a.get_text())
        
        return link_data

    links = soup.find_all('a') # get all links
    for a in links:
        link_data = process_a_tag(a) # returns a dict
        link_text_info.append(link_data)

    return link_text_info

# Function to calculate pass/fail score based on specific criteria
def calculate_score(link_text):
    # Check if link text has more than 4 words
    word_count = len(link_text.split())
    if word_count > 4:
        return "Pass"
    else:
        return "Fail"

# Table view with link text information
@app.route('/')
def display_table():
    website_url = 'https://www.nytimes.com/'
    link_text_info = get_link_text_info(website_url) 
    return render_template('linktable.html', link_text_info=link_text_info)

if __name__ == '__main__':
    app.run()


