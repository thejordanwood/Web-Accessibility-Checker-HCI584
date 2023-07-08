from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

# Creates the Flask application instance
app = Flask(__name__)

# This defines the function to get alt text image info. 
# Function puts the web address, thumbnail, presence of alt text, alt text content, and pass/fail score into a table. 
def get_image_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Empty list that stores image info dicts
    image_info = []

    def process_img_tag(img):
        image_data = {}

        # Gets the image's web address, thumbnail, presence of alt text, and alt text content
        image_data['Web address'] = url
        if 'src' in img.attrs:
            image_data['Thumbnail'] = img['src']
            if "?" in img['src']:
                qstmark_idx = img['src'].index("?")
                image_data['Web address'] = img['src'][:qstmark_idx]
        else:
            image_data['Thumbnail'] = None

        if 'alt' in img.attrs:
            alt_text = img['alt'].strip()
            if alt_text:
                image_data['Presence of alt text'] = "Yes"
                image_data['Alt text content'] = alt_text

                # Calculates pass/fail score of alt text based on specific criteria
                image_data['Pass/fail score'] = calculate_score(alt_text)
            else:
                image_data['Presence of alt text'] = "No"
                image_data['Alt text content'] = ""
                image_data['Pass/fail score'] = "Fail"
        else:  # no alt
            image_data['Presence of alt text'] = "No"
            image_data['Alt text content'] = ""
            image_data['Pass/fail score'] = "Fail"

        return image_data

    images = soup.find_all('img')  # gets all images, process_img_tag() will deal with alt/no-alt
    for img in images:
        image_data = process_img_tag(img)  # returns a dict
        image_info.append(image_data)

    return image_info


# Function to calculate pass/fail score for alt text based on word count and specific words
def calculate_score(alt_text):
    word_count = len(alt_text.split())
    # Checks if alt text has between 5 - 80 words
    if alt_text == "":
        return ""
    if 5 <= word_count <= 80: 
        # Checks if alt text does not start with "Picture of" or "Image of"
        if not alt_text.startswith("Picture of") and not alt_text.startswith("Image of"):
            return "Pass"  
    return "Fail"


# Defines function to get link text image info
# Function puts the web address, presence of alt text, alt text content, and pass/fail score into a table. 
def get_link_text_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Empty list that stores link text info dicts
    link_text_info = []

    def process_a_tag(a):
        link_data = {}

        # Gets the links web address and link text content
        link_data['Web address'] = url
        link_data['Link text content'] = a.get_text()

        # Adds calclated pass/fail score based on specific criteria
        link_data['Pass/fail score'] = calculate_score(a.get_text())
        
        return link_data

    links = soup.find_all('a')  # gets all links
    for a in links:
        link_data = process_a_tag(a)  # returns a dict
        link_text_info.append(link_data)

    return link_text_info

# Function to calculate pass/fail score of link text based on word count and specific words
def calculate_score(link_text):
    word_count = len(link_text.split())
    # Checks if link text is between 4 - 14 words
    if 4 <= word_count <= 15: 
        # Checks if alt text does not start with "Click Here" or "Read More"
        if not link_text.startswith("Click Here") and not link_text.startswith("Read More"):
            return "Pass"       
    return "Fail"


# Starts screen where user can insert web URL
@app.route('/', methods=['GET', 'POST'])
def start_screen():
    if request.method == 'POST':
        website_url = request.form['website_url']
        image_info = get_image_info(website_url)
        link_info = get_link_text_info(website_url)
        return render_template('both_tables.html', image_info=image_info, link_info=link_info, website_url=website_url)
    else:
        return render_template('both_tables.html')
    
# Displays and toggles between both tables
@app.route('/toggle')
def toggle_table():
    # Retrieves the type and URL parameters from the request
    table_type = request.args.get('type')
    website_url = request.args.get('url')

    # Determines the data for the selected table type
    if table_type == 'link':
        link_info = get_link_text_info(website_url)
        image_info = []  # Empty list for image_info to maintain compatibility
    else:
        link_info = []  # Empty list for link_info to maintain compatibility
        image_info = get_image_info(website_url)

    return render_template('both_tables.html', image_info=image_info, link_info=link_info, table_type=table_type, website_url=website_url)

if __name__ == '__main__':
    app.run()




