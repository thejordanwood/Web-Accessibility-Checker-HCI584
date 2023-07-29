# Web Accessibility Checker (HCI584)
This application evaluates text that is used for links and alternative text for images.

## Description

The most common web accessibility issues are missing or incorrect text for links and images. Without proper text on these, screen readers won't be able to appropriately relay webpage information. This application allows users to enter a web address and select the type of data (images or links) they want to evaluate. Data is then displayed in a table that shows web address, thumbnail (for images), text content, and pass/fail score.

The image score is determined by checking if the alternative text is between 4 to 80 words and the text doesn't start with the phrases “image of'' or “picture of.” The link score is determined by checking if the text is betweem 4 to 30 words and doesn't start with the phrases “read more” or “click here.”

## Requirements

- Python 3.10 or higher
- Python packages:
    - Flask
    - requests
    - bs4 (BeautifulSoup)
 
 ## Installation

**for main.py:** Use pip to install the required third party packages (pip -r requirements.txt)

**for template.html:** In the main project folder, keep html file within a secondary folder labeled *templates*. 

 ## Usage

1. From an IDE, run the main.py file. If you don’t have an IDE, open a terminal to the appropriate folder and type in python <.py file>. The application will start, and you should see a local URL (e.g., http://127.0.0.1:5000/) in the terminal.

2. Access this application by opening your web browser, then enter the local URL provided.

![Entering a web address and selecting the type of data to view](https://github.com/thejordanwood/Web-Accessibility-Checker-HCI584/blob/main/docs/search.gif)

3. Enter a web address and select the type of data to view. The web address must start with http:// or https://. Select "Images" or "Links" from the dropdown menu to view the corresponding data.

![Sorting the table by clicking on the *Score* header](https://github.com/thejordanwood/Web-Accessibility-Checker-HCI584/blob/main/docs/sort.gif)

4. View the results. After submitting the web address and data type, the application will display a table containing the relevant information. Sort the table by clicking on the *Score* header to order the pass/fail score in ascending or descending order

5. Export data to CSV. To export the displayed table data to a CSV file, click on the "Export Image Table" or "Export Link Table" button.

 ## Known Issues

- The application might not handle certain web page structures or non-standard HTML formats effectively.
- Some web pages may have security measures that prevent the scraper from accessing their content.

 ## Acknowledgments
 This project makes use of the Flask framework, BeautifulSoup, and other helpful Python packages.


