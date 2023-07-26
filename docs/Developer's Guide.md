# Developer's Guide
This guide covers installation, user interaction flow, known issues, and future work of the Accessibility Checker project.

## Overview
The Accessibility Checker is a web application built with Flask that evaluates text that is used for links and alternative text for images. It allows users to enter a web address and select the type of data (images or links) they want to evaluate. The application then scrapes the web page, processes the data, and displays it in a table format. 

## Planning Specs
The application currently includes the following functionality:

- Ability to enter a web address and choose between viewing image or link data.
- Web scraping to gather information about images and links from the provided web page.
- Calculation of a pass/fail score based on specific criteria for both alt text and link text.
- Displaying the relevant data in a table format.
- Sorting of the table based on the pass/fail score.

## User Interaction + Code

**User Interaction Flow**
1. User enters a web address and selects the type of data (images or links).
2. User clicks on the "View data" button to submit the request.
3. The application scrapes the web page and gathers relevant information about images or links.
4. The data is processed, and a pass/fail score is calculated based on specific criteria.
5. The application displays the data in a table format, showing the web address, thumbnail (for images), text content, and pass/fail score.

**Code Flow**
1. The Flask application starts by running the *main.py* file.
2. User interactions are handled through the `start_screen` function in *main.py*.
3. When the user submits the web address and data type, the corresponding `get_image_info` or `get_link_text_info` function is called, which handles web scraping and data processing.
4. The results are displayed using the HTML template in *template.html*.

## Known Issues

**Major Issues**
- The application may break when scraping web pages with extensive dynamic content or requiring authentication.
- The scraper may encounter errors when dealing with complex web page layouts or heavy JavaScript usage.
  
**Minor Issues**
- The application might not handle certain web page structures or non-standard HTML formats effectively.
- Some web pages may have security measures that prevent the scraper from accessing their content.

## Future Work
The Accessibility Checker has the potential for expansion and improvement. Some ideas for future work include:

- Adding support for additional data types, such as form fields or media elements.
- Consider supporting new web page formats and handling various JavaScript frameworks.

