# LaTex Delimeters Conversion Website
#### Youtube Link: https://youtu.be/tKmiF_9sBzw

## Overview

My final project is a tool for converting between the different types of LaTex delimeters. The website was built with bootstrap and makes api request to a backend coded with flask that manages the conversion process.

### Usage

Once loaded, the website has two main pages: home and LaTex files.

The home page allows users to paste in their LaTex source code into an input box and select the desired type of delimeters, converting the source code as per this selection. The converted LaTex is outputed in a text area, which the user can copy as well as edit.

The files page takes in a file of .tex or .md format and similarly converts the delimeters to the selected types. The converted content will both be outputted in a preview box, which the user can edit, and as a file which can be downloaded.

Additionally, there is also a dropdown in the navigation bar for toggling between light and dark mode.
---
## Documentation
- app.py: Contains the flask back end which manages the links and api requests.
- helper.py: Contains the convert function as well as a file validation function.
- static
    - styles.css
    - theme.js: Implements the theme toggle feature in the nav bar to allow changing between light and dark mode.
- templates
    - layout.html: Main template for the website.
    - index.html: Contains content for the home page.
    - file.html: Content for the LaTex file page as well as its javascript.
- test.tex, output.tex: LaTex files used for testing the convert function.


## Motivation for the Website
When making flashcards from Obisidian markdown files with LaTex and tex files, a common problem was that apps like Anki do not accept delimeters with dollar signs, so a delimeter conversion must be done. Since this is tedious to do manually across multiple files, I decided to automate the process, and further implemented it as a web application.


## Development Process
I began by developing the conversion functionality in python, making heavy use of the re library. Initially, the convert function simply performed a find and replace for the LaTex delimeters. However, I later found that this could make unwanted changes in certain edge cases, such as the verbatim environment, or literal dollar signs being used.

This led me to divide the conversion process into two stages: first searching for protected environments such as verbatim sections and 'flagging' them, then doing a search and replace for delimeters that are not in these environments. I encountered several difficulties in deciding how to avoid the protected regions effectively, but the final function essentially records the span of all protected regions in a list, and for each delimeter pair found with regexes, a check is done to ensure they do not lie within a protected span.

I also experimented with many regexes to effectively search for valid LaTex delimeter pairs and minimise accidental conversion of literal dollar signs and other elements. The final regexes and convert function will work as expected in most cases, even with verbatim environments and other environments such as code blocks. However, there can still be minor issues such as two literal dollar signs on one line which are not escaped in markdown.

After the convert function was completed, I began to build the HTML, relying on bootstrap templates for most elements. This occurred in conjunction with building the flask backend. Overall, the website has a simple layout, with its main dynamic features being to do with form submission of user LaTex code, delimeter selection and outputting the converted content.

For user file inputs, my website will output the converted text in a text are, while also providing a link to download the converted file in the original format (.tex or .md). This page also has a clear button to clear the download links and imporve user experience when converting multiple files, introducing some more interactive elements to the page.



