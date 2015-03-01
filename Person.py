import json

__author__ = 'Michelle'


class Person:

    def __init__(self, url):
        self.url = url
        self.details = {}
        self.education = []
        self.jobs = []
        self.skills = []

    def to_json(self):
        data = {}
        data['url'] = self.url
        data['details'] = self.details
        data['education'] = self.education
        data['jobs'] = self.jobs
        #data['skills'] = self.skills
        json_data = json.dumps(data, indent=4)
        return json_data