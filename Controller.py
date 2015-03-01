from LinkedInCrawler.Crawler import Crawler
from LinkedInCrawler import Settings
from LinkedInCrawler.Writer import Writer

__author__ = 'Michelle'


class Controller:

    def __init__(self):
        self.crawler = Crawler()
        self.people = []
        self.Writer = Writer()

    def write_people_to_file(self):
        self.Writer.write_people_to_file(self.people)

    def find_name(self, name):
        url = Settings.base_url + Settings.directory_link + name[0].lower()
        self.find_page_by_name(name.lower(), url)

    # Some of the links received from Linkedin have no prefix. This fixes that.
    def validate_link(self, url):
        new_url = url.encode('ascii', errors='ignore')
        if new_url[0] != 'h':
            return Settings.base_url[:-1] + url
        return url

    def save_person(self, link):
        fixed_link = self.validate_link(link)
        person = self.crawler.crawl_profile_page(fixed_link)
        if person is not None:
            self.people.append(person)

    '''
    If url param is a directory page, zoom in the ranges (recursion).
    If it's a search page, go through profiles in page.
    If it's a profile page, save it to list.
    '''
    def find_page_by_name(self, name, url):
        fixed_url = self.validate_link(url)
        parts = fixed_url.split('/')
        if parts[3] == 'directory':
            name_ranges = self.crawler.crawl_directory_page(fixed_url)
            next_range = self.get_range(name, name_ranges.keys())
            if next_range is None:
                if name_ranges.has_key(name):
                    if 'dir' in name_ranges[name]:
                        self.iterate_profiles(name_ranges[name])
                    else:
                        self.save_person(name_ranges[name])
            elif '-' not in str(name_ranges.keys()[0]):
                search_link = name_ranges[name]
                if parts[4] == 'dir':
                    self.iterate_profiles(search_link)
                else:
                    self.save_person(search_link)
            else:
                return self.find_page_by_name(name, name_ranges[next_range])
        elif parts[4] == 'dir':
            self.iterate_profiles(fixed_url)
        else:
            self.save_person(fixed_url)

    # being called when needed to crawl search pages (https://www.linkedin.com/pub/dir/William/Gates)
    def iterate_profiles(self, url):
        profiles = self.crawler.crawl_profile_search_page(self.validate_link(url))
        for profile in profiles:
            self.save_person(profile)

    '''
    Zooming in directory pages (by recursion in binary search of name in ranges array),
    returning new range.
    name_array = array of current page ranges.
    '''
    def search_range(self, name, name_array):
        try:
            size = len(name_array)
            _range = name_array[size/2]
            last_name = _range.split('-')[1][1:]
            for index in range(0, min(len(name), len(last_name))):
                if name[index] > last_name[index]:
                    return self.end_case_larger_name(name, name_array, size)
                elif name[index] < last_name[index]:
                    return self.end_cases_larger_end_range(name, name_array, size)
            if len(name) > len(last_name):
                return self.end_case_larger_name(name, name_array, size)
            elif len(name) < len(last_name):
                return self.end_cases_larger_end_range(name, name_array, size)
            return _range
        except:
            return None

    def get_range(self, name, name_array):
        return self.search_range(name, sorted(name_array, key=str.lower))

    def end_cases_larger_end_range(self, name, name_array, size):
        if size == 2:
            return name_array[1]
        if size == 3:
            return self.search_range(name, name_array[:-(size/2)])
        return self.search_range(name, name_array[:-(size/2 - 1)])

    def end_case_larger_name(self, name, name_array, size):
        if size == 2:
            return name_array[0]
        return self.search_range(name, name_array[(size/2):])