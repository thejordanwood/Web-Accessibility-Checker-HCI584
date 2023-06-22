from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

# Create the Flask application instance
app = Flask(__name__)

# Define function to get alt text image info
def get_image_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Empty list that stores image info dicts
    image_info = []

    def process_img_tag(img):
        image_data = {}

        # Get the image's web address, thumbnail URL, presence of alt text, and alt text content
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

                # Calculate pass/fail score of alt text based on specific criteria
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

    images = soup.find_all('img')  # get all images, process_img_tag() will deal with alt/no-alt
    for img in images:
        image_data = process_img_tag(img)  # returns a dict
        image_info.append(image_data)

    return image_info


# Function to calculate pass/fail score for alt text based on specific criteria
def calculate_score(alt_text):
    # Check if alt text has more than 5 words
    word_count = len(alt_text.split())
    if word_count > 5:
        # Check if alt text does not start with "Picture of" or "Image of"
        if not alt_text.startswith("Picture of") and not alt_text.startswith("Image of"):
            return "Pass"
    return "Fail"


# Define function to get link text image info
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

    links = soup.find_all('a')  # get all links
    for a in links:
        link_data = process_a_tag(a)  # returns a dict
        link_text_info.append(link_data)

    return link_text_info

# Function to calculate pass/fail score of link textbased on specific criteria
def calculate_score(link_text):
    # Check if link text has more than 4 words
    word_count = len(link_text.split())
    if word_count > 4:
        return "Pass"
    else:
        return "Fail"


# Start screen where user can insert web URL
@app.route('/', methods=['GET', 'POST'])
def start_screen():
    if request.method == 'POST':
        website_url = request.form['website_url']
        image_info = get_image_info(website_url)
        link_info = get_link_text_info(website_url)
        return render_template('both_tables.html', image_info=image_info, link_info=link_info, website_url=website_url)
    else:
        return render_template('start.html')
    
# Display and toggle between both tables
@app.route('/toggle')
def toggle_table():
    # Retrieve the type and URL parameters from the request
    table_type = request.args.get('type')
    website_url = request.args.get('url')

    # Determine the data for the selected table type
    if table_type == 'link':
        link_info = get_link_text_info(website_url)
        image_info = []  # Empty list for image_info to maintain compatibility
    else:
        link_info = []  # Empty list for link_info to maintain compatibility
        image_info = get_image_info(website_url)

    return render_template('both_tables.html', image_info=image_info, link_info=link_info, table_type=table_type, website_url=website_url)

if __name__ == '__main__':
    app.run()




