import requests
from bs4 import BeautifulSoup
from LinkedInCrawler.Person import Person

__author__ = 'Michelle'


class Crawler:
    def __init__(self):
        pass

    def get_beautiful_soup(self, url):
        page_content = requests.get(url)
        page_content_str = page_content.text
        return BeautifulSoup(page_content_str)

    def crawl_profile_page(self, url):
        person = Person(url)
        beautiful_soup = self.get_beautiful_soup(url)
        self.parse_profile_card(beautiful_soup, person)
        self.parse_profile_background(beautiful_soup, person)
        return person

    def parse_profile_background(self, beautiful_soup, person):
        profile_background = beautiful_soup.findAll('div', {'class': 'profile-background'})
        if len(profile_background) > 0:
            backgrounds = profile_background[0].contents[1].contents
            for background in backgrounds:
                self.parse_background_tags(background, person)

    def parse_background_tags(self, background, person):
        background_type = background.contents[0].contents[0].string.encode('ascii', errors='ignore')
        if background_type.lower() == 'education':
            for org in background.findAll('div', {'class': 'education'}):
                edu = {}
                edu['org'] = org('h4', {'class': 'summary fn org'})[0].text
                if len(org('time')) > 0:
                    edu['from'] = org('time')[0].text
                if len(org('time')) > 1:
                    edu['to'] = org('time')[1].text[3:]
                person.education.append(edu)
        elif background_type.lower() == 'experience':
            try:
                self.parse_position(background, person, 'current-position')
                self.parse_position(background, person, 'past-position')
            except:
                pass
        elif background_type.lower() == 'summary':
            person.details[background_type] = background.text
        elif background_type.lower() == 'skills':
            skills = []
            for skill in background('span', {'class': 'skill-pill'}):
                skills.append(skill.text)
            person.skills = skills

    def parse_position(self, background, person, class_type):
        for position in background.findAll('div', {'class': class_type}):
                job = {}
                job['org'] = position('h5')[0].text
                if job['org'] == '':
                    job['org'] = position('h5')[0]('a')[0].contents[0].attrs['alt']
                job['position'] = position('h4')[0].text
                p_time = position('time')
                if len(p_time) > 0:
                    job['from'] = position('time')[0].text
                if len(p_time) > 1:
                    job['to'] = position('time')[1].text
                person.jobs.append(job)

    def parse_profile_card(self, beautiful_soup, person):
        profile_card = beautiful_soup.findAll('div', {'class': 'profile-card vcard'})
        soup = beautiful_soup.findAll('span', {'class': 'full-name'})
        if len(soup) > 0:
            person.details["name"] = beautiful_soup.findAll('span', {'class': 'full-name'})[0].string
        if len(profile_card) > 0:
            person.details["address"] = profile_card[0]('span', {'class': 'locality'})[0].string
            profile_card_content = profile_card[0]('a')[0].contents
            if len(profile_card_content) > 1:
                pic_url = profile_card[0]('a')[0].contents[1].attrs['src']
                person.details["picture"] = pic_url

    def crawl_profile_search_page(self, url):
        links_to_people = []
        beautiful_soup = self.get_beautiful_soup(url)
        for line in beautiful_soup.findAll('span', {'class': 'given-name'}):
            links_to_people.append(line.parent.attrs['href'])
        return links_to_people

    def crawl_directory_page(self, url):
        name_ranges = {}
        beautiful_soup = self.get_beautiful_soup(url)
        for line in beautiful_soup.findAll('li', {'class': 'content'}):
            attrs = line.contents[0].attrs
            href = str(attrs['href'])
            names = line.string.lower()
            ascii_name = names.encode('ascii', errors='ignore')
            name_ranges[ascii_name] = href
        return name_ranges