# General Description of Project

The most common web accessibility issues are missing link text and missing alternative text for
images. These are important because people with visual impairments often use screen readers
to understand a webpage. If there isn’t proper text on images or links, screen readers don’t have
anything to read. This makes it hard to understand web pages that use informative images or
link to relevant content.

My project will work to solve these problems by creating a program that allows a user to see
which links and images have missing text. The user will be able to enter a home page web
address, then the program will use BeautifulSoup to analyze that and other pages beginning
with the home address in order to show missing text across the site.

## Expected output for alt text
- Show the web address the image can be found on.
- Show a thumbnail of the image.
- Show whether or not it has alt text.
- If it has alt text, it should show what that alt text is.
- Give a pass/fail score to the alt text.

## Expected output for link text
- Show the web address the link can be found on.
- Show if the link contains text or not.
- If it has text, it should show what that text is.
- Give a pass/fail score to the text.

The pass or fail score for these would be generated based on what the program deems to be
“bad” alt text or link text. For example, alt text should contain more than 5 words and not start
with the phrases “image of” or “picture of.” Link text will fail if it’s unclear and doesn’t
communicate enough information to the user about what they need to do. Phrases like “read
more” and “click here” create a bad experience for all users–especially those that are using
screen readers. Screen readers also typically navigate from link to link, so unclear links can get
confusing. Ideally, a link should be descriptive and say something like “Read more about our
Python class.”

For the user interface, I will use Flask but start with a jupyter notebook.

# Task Vignettes

## Task 1: Find missing alt text

**User activity:**

- Enter homepage web address, such as https://www.nytimes.com/
- Select “search”
- User sees table with this output
  - Web address the image can be found on.
  - Thumbnail of the image.
  - Whether or not it has alt text.
  - If it has alt text, show what that alt text is.
  - A pass/fail score to the alt text.
- Users can filter table columns based on their criteria.

<img width="650" alt="Intro screen with field that allows user to enter a web address" src="https://github.com/thejordanwood/Web-Accessibility-Checker-HCI584/assets/104526584/437c0ee9-b374-4b94-afe9-2f3fb943dbfa">

*Starting screen where users can enter a web address.*

<img width="650" alt="Alt text table that shows the expected output" src="https://github.com/thejordanwood/Web-Accessibility-Checker-HCI584/assets/104526584/6d2d96d2-f784-475f-b8dd-bd718a03caa0">

*Table where alt text output will show.*

## Task 2: Find missing or unclear link text

**User activity:**

- Enter homepage web address, such as https://www.nytimes.com/
- Select “search for link text”
- User sees table with this output
  - Web address the link can be found on.
  - Whether or not it has alt text.
  - If it has alt text, show what that alt text is.
  - A pass/fail score to the alt text.
- Users can filter table columns based on their criteria.

<img width="650" alt="Link text table that shows the expected output" src="https://github.com/thejordanwood/Web-Accessibility-Checker-HCI584/assets/104526584/a2dd6a0e-0fc0-489e-aea5-f671bd020c38">

*Table where link text output will show.*

# Technical Flow

<img width="610" alt="A flow chart that shows the technical flow of this project." src="https://github.com/thejordanwood/Web-Accessibility-Checker-HCI584/assets/104526584/8e9a996e-3040-4edf-b472-9d243c99694f">

# Self Assessment

After working through this spec, there aren’t any major changes that make it different from my
sketch. I expect that my table wireframe is a starting point, and that the final iteration will end up
looking a bit different.

Overall, I’m fairly confident that I’ll be able to implement this spec. I’m still new to Python, and
worry about falling into the trap of “you don’t know what you don’t know.” I’m sure some
unexpected difficulties will come up as I work through this project.

The biggest problem I need to solve is using BeautifulSoup to scrape HTML content so that
content can go into a table. Having never used BeautifulSoup before, I anticipate needing help
with that. Another area I may need help with is using Flask as a GUI. I used TkInter last
semester for HCI 574 instead of Flask.
