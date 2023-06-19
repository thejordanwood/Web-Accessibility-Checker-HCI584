from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

# Create the flask application instance
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

                # Calculate pass/fail score based on specific criteria
                image_data['Pass/fail score'] = calculate_score(alt_text)
            else:
                image_data['Presence of alt text'] = "No"
                image_data['Alt text content'] = ""
                image_data['Pass/fail score'] = "Fail"
        else: # no alt
            image_data['Presence of alt text'] = "No"
            image_data['Alt text content'] = ""
            image_data['Pass/fail score'] = "Fail"

        return image_data

    images = soup.find_all('img') # get all images, process_img_tag() will deal with alt/no-alt
    for img in images:
        image_data = process_img_tag(img) # returns a dict
        image_info.append(image_data)

    return image_info

# Function to calculate pass/fail score based on specific criteria
def calculate_score(alt_text):
    # Check if alt text has more than 5 words
    word_count = len(alt_text.split())
    if word_count > 5:
        # Check if alt text does not start with "Picture of" or "Image of"
        if not alt_text.startswith("Picture of") and not alt_text.startswith("Image of"):
            return "Pass"
    return "Fail"

#start screen where user can insert web url
@app.route('/', methods=['GET', 'POST'])
def start_screen():
    if request.method == 'POST':
        website_url = request.form['website_url']
        image_info = get_image_info(website_url)
        return render_template('table.html', image_info=image_info)
    else:
        return render_template('start.html')

if __name__ == '__main__':
    app.run()

