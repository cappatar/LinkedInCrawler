from LinkedInCrawler import Settings

__author__ = 'Michelle'


class Writer:

    def write_people_to_file(self, people):
            with open(Settings.file_path, "w") as text_file:
                for person in people:
                    text_file.write("{0}\n\n".format(person.to_json()))