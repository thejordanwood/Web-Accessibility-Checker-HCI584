from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

# Create the flask application instance
app = Flask(__name__)

# Define function to get alt text image info
def get_image_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Empty list that stores image info
    image_info = []
    
    images_with_alt = soup.find_all('img', alt=True)
    
    # Dictionary that stores image info that does have alt text
    for img in images_with_alt:
        image_data = {}
        
        # Get the image's web address, thumbnail URL, presence of alt text, and alt text content
        image_data['Web address'] = url
        if 'src' in img.attrs:
            image_data['Thumbnail'] = img['src']
        else:
            image_data['Thumbnail'] = None
        image_data['Presence of alt text'] = True
        image_data['Alt text content'] = img['alt']

        # Calculate pass/fail score based on specific criteria
        image_data['Pass/fail score'] = calculate_score(img['alt'])
        
        image_info.append(image_data)
    
    images_without_alt = soup.find_all('img', alt=False)
    
    # Dictionary that stores image info that doesn't have alt text
    for img in images_without_alt:
        image_data = {}
        
        # Get the image's web address, thumbnail URL, presence of alt text, and alt text content (None)
        image_data['Web address'] = url
        if 'src' in img.attrs:
            image_data['Thumbnail'] = img['src']
        else:
            image_data['Thumbnail'] = None
        image_data['Presence of alt text'] = False
        image_data['Alt text content'] = None

        # Calculate pass/fail score based on specific criteria
        image_data['Pass/fail score'] = None
        
        image_info.append(image_data)
    
    return image_info

# Function to calculate pass/fail score based on specific criteria
def calculate_score(alt_text):
    # Put scoring logic here
    return 0

# Pull in table decoration and an example website URL
@app.route('/')
def display_table():
    website_url = 'https://www.nytimes.com/'
    image_info = get_image_info(website_url)
    return render_template('table.html', image_info=image_info)

if __name__ == '__main__':
    app.run()