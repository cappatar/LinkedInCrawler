from LinkedInCrawler.Controller import Controller

__author__ = 'Michelle'


c = Controller()
c.find_name('william gates')
c.write_people_to_file()
print 'done'