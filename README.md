# Web Accessibility Checker (HCI584)
This is a web accessibility tester that checks for alt text and link text.

## What is the purpose of this project?

The most common web accessibility issues are missing link text and missing alternative text for images. These are important to have on a website because people with visual impairments often use screen readers to understand a webpage. If there isn’t proper text on images or links, screen readers don’t have anything to read. This makes it hard to understand web pages that use informative images or link to relevant content. My project will work to solve these problems by creating a program that allows a user to see which links and images have missing text. 

## What is the expected functionality?

The user will be able to enter a home page web address, then the program will analyze that and other pages beginning with the home address in order to show missing text across the site.

### Expected output for alt text
- Show the web address the image can be found on.
- Show a thumbnail of the image. 
- Show whether or not it has alt text. 
- If it has alt text, it should show what that alt text is. 
- Give a pass/fail score to the alt text.

### Expected output for link text
- Show the web address the link can be found on.
- Show if the link contains text or not.
- If it has text, it should show what that text is. 
- Give a pass/fail score to the text. 

The pass or fail score for these would be generated based on what the program deems to be bad alt text or link text. For example, alt text should contain more than 5 words and avoid starting with the phrases “image of” or “picture of.” Link text will fail if it’s unclear and doesn’t communicate enough information to the user about what they need to do. Phrases like “read more” and “click here” create a bad experience for all users–especially those that are using screen readers. Ideally, a link should be descriptive and say something like “Read more about our Python class.”

