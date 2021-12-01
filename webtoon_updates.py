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
            updates.append((webtoon_name, int(webtoon_chap), int(latest_chap_num)))

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
            