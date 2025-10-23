

import requests
from bs4 import BeautifulSoup
from ebooklib import epub

# Initialize the EPUB book
book = epub.EpubBook()
book.set_identifier('identifier')                                                       # Set identifier 
book.set_title('Title')                                                                 # Set title of book 
book.set_language('language')                                                           # Set language 
book.add_author('Author')                                                               # Set Author 

# List to hold chapter objects
chapters = []

# Loop through chapter numbers
for i in range(1, 301):                                                                 # Verify number of chapters 
    url = f'https://-{i}/'                                                              # Input link 
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve Chapter {i}")
        continue
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the main content; adjust the selector as needed
    content_div = soup.find('div', class_='entry-content')
    if not content_div:
        print(f"Content not found for Chapter {i}")
        continue
    content_html = str(content_div)
    
    # Create EPUB chapter
    chapter = epub.EpubHtml(title=f'Chapter {i}', file_name=f'chap_{i}.xhtml', lang='en')
    chapter.content = content_html
    book.add_item(chapter)
    chapters.append(chapter)

# Define Table of Contents and Spine
book.toc = tuple(chapters)
book.spine = ['nav'] + chapters

# Add navigation files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Write the EPUB file
epub.write_epub('filename.epub', book)                                              # Set filename for EPUB 
print("EPUB file 'filename.epub' has been created successfully.")