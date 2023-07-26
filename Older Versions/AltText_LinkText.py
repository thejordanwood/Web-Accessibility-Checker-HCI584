from flask import Flask, make_response, render_template, request
import requests
from bs4 import BeautifulSoup

# Creates the Flask application instance
app = Flask(__name__)
    
# Defines the function to get alt text image info. 
# Function puts the web address, thumbnail, presence of alt text, alt text content, and pass/fail score into a table.
def get_image_info(url):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    # Empty list that stores image info dicts
    image_info = []
    
    # Processes the image's web address and thumbnail, and calculates pass/fail score of alt text
    def process_img_tag(img):
        image_data = {}
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
                image_data['Alt Text Content'] = alt_text

                # Calculates pass/fail score of alt text based on specific criteria
                image_data['Pass/Fail Score'] = calculate_score_img(alt_text)
            else:
                image_data['Alt Text Content'] = ""
                image_data['Pass/Fail Score'] = "Fail"
        else: # no alt
            image_data['Alt Text Content'] = ""
            image_data['Pass/Fail Score'] = "Fail"
        
        return image_data
    
    images = soup.find_all('img') # finds all images, process_img_tag() will deal with alt/no-alt
    for img in images:
        image_data = process_img_tag(img) # returns a dict
        image_info.append(image_data)
    
    return image_info

# Function to calculate pass/fail score for alt text based on word count and specific words
def calculate_score_img(alt_text):
    word_count = len(alt_text.split())
    # Checks if there are any empty alt text tags. This could mean the image is decorative, which means it doesn't need alt text.
    if alt_text == " ":
        return " "
    # Checks if alt text has between 4 - 80 words
    if 4 <= word_count <= 80: 
        # Checks if alt text does not start with "Picture of" or "Image of"
        if not alt_text.startswith("Picture of") and not alt_text.startswith("Image of"):
            return "Pass"  
    return "Fail"

# Defines function to get link text image info
# Function puts the destination address, link text content, and pass/fail score into a table. 
def get_link_text_info(url):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    # Empty list that stores link text info dicts
    link_text_info = []
    
    # Processes the link's destination address and link text content
    def process_a_tag(a):
        link_data = {}
        link_data['Web address'] = url
        link_data['Link text content'] = a.get_text()

        # Calculates pass/fail score based on specific criteria
        link_data['Pass/fail score'] = calculate_score_link(a.get_text())
        link_destination = a['href']

        if not link_destination.startswith("http://") and not link_destination.startswith("https://"):
            link_destination = url + link_destination

        link_data['Link destination'] = link_destination

        if a.get_text().strip():
            link_data['Presence of link text'] = "Yes"
        else:
            link_data['Presence of link text'] = "No"

        return link_data
    
    links = soup.find_all('a') # finds all links
    header_links = soup.find('header').find_all('a')
    footer_links = soup.find('footer').find_all('a')
    
    for a in links:
        if a in header_links or a in footer_links:
            continue
        
        link_data = process_a_tag(a) # returns a dict
        link_text_info.append(link_data)
    
    return link_text_info

# Function to calculate pass/fail score of link text based on word count and specific words
def calculate_score_link(link_text):
    word_count = len(link_text.split())
    # Checks if link text is between 4 - 30 words
    if 4 <= word_count <= 30: 
        # Checks if alt text does not start with "Click Here" or "Read More"
        if not link_text.startswith("Click Here") and not link_text.startswith("Read More"):
            return "Pass"       
    return "Fail"

# Starts screen where user can insert web address and select which table to view
@app.route('/', methods=['GET', 'POST'])
def start_screen():
    try:
        website_url = request.args.get('website_url', default='')
        table_type = request.args.get('table_type', default='None')
    except Exception as e:
        website_url = ''
        table_type = 'None'
    
    if table_type == "alt":
        image_info = get_image_info(website_url)
        if image_info is not None:
            msg = "" # No error
        else:
            msg =  website_url + " is invalid. Please try again."
        return render_template('both_tables.html', msg=msg, image_info=image_info, table_type=table_type, website_url=website_url)
        
    elif table_type == "link":
        link_info = get_link_text_info(website_url)  # Pass the correct URL
        if link_info is not None:
            msg = "" # No error
        else:
            msg =  website_url + " is invalid. Please try again."
        return render_template('both_tables.html', msg=msg, link_info=link_info, table_type=table_type, website_url=website_url)
    else:
        return render_template('both_tables.html', table_type='None', website_url=website_url)

# This checks and receives the table data that will be exported into a csv
@app.route('/export', methods=['GET'])
def export_table():
    website_url = request.args.get('website_url')
    table_type = request.args.get('table_type')

    if table_type == "alt":
        table_data = get_image_info(website_url)
        if table_data is None:
            return "The web address you entered is invalid. Please try again."
        filename = "alt_image_table.csv"
    elif table_type == "link":
        table_data = get_link_text_info(website_url)
        if table_data is None:
            return "The web address you entered is invalid. Please try again."
        filename = "link_text_table.csv"
    else:
        return "Invalid table type"

    response = make_response(generate_csv(table_data))
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.headers['Content-type'] = 'text/csv'
    
    return response

# This generates the csv that gets downloaded
def generate_csv(table_data):
    if not table_data:
        return ''

    csv_content = ''
    keys = table_data[0].keys()
    csv_content += ','.join(keys) + '\n'

    for data in table_data:
        values = [str(data[key]).replace(',', '') for key in keys]
        csv_content += ','.join(values) + '\n'

    return csv_content

if __name__ == '__main__':
    app.run()






