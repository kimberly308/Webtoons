from bs4 import BeautifulSoup
import cloudscraper
import requests

def check_updates(website_link):
    """
    Returns the latest chapter number for the webtoon.
    Only works with s2manga.com
    """
    page = cloudscraper.create_scraper().get(website_link)
    # with open("out.html", "w") as f:
    #     f.write(page.text)
    soup = BeautifulSoup(page.content, 'html.parser')
    chapters = list(soup.select('li.wp-manga-chapter'))  # finds all li tags with a class of wp-manga-chapter
    latest_chapter = str(chapters[0])
    latest_chapter_number = latest_chapter.split()[5]
    return latest_chapter_number

def format_chapters(current_chap, latest_chap):
    """
    Formats two input chapter numbers, provided as a string, 
    into an integer or float
    """
    try: current_chap = int(current_chap)
    except ValueError: current_chap = float(current_chap)
    try: latest_chap = int(latest_chap)
    except ValueError: latest_chap = float(latest_chap)  
    return current_chap, latest_chap



# identifies webtoons with updates
print("\nRunning...")
updates = []
with open ('webtoons.txt', 'r') as data:     # Open webtoons.txt for reading
    for webtoon in data:                     # For each line, read to a string
        webtoon_details = str(webtoon).split(sep = ',')
        webtoon_name = webtoon_details[0]
        webtoon_chap = webtoon_details[1]
        webtoon_website = webtoon_details[2].rstrip()

        latest_chap_num = check_updates(webtoon_website)
        if latest_chap_num > webtoon_chap:
            webtoon_chap, latest_chap_num = format_chapters(webtoon_chap, latest_chap_num)
            updates.append((webtoon_name, webtoon_chap, latest_chap_num))

# prints the webtoons with updates in the form of 
# (name, last chapter I read, latest chapter available)
print("\n")
if len(updates) == 0:
    print("No updates")
else:
    for i in updates:
        print(i)
print("\n")

# writes the info on updated webtoons to updates.txt
with open('updates.txt', 'w') as overwrite:
    if len(updates) >= 1:
        for i in updates:
            overwrite.write(str(i) + '\n')
    else:
        overwrite.write("No updates")
            