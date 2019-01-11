import requests
from lxml import html
import urllib
import os

'''

specify directory to save the files
'''

HOME_DIR = os.getenv("HOME")
file_dir = os.chdir(os.path.join(HOME_DIR, "Downloads", "test"))
'''

specify the URL where you want to download the files
'''
url = "http://www.mobile.ifi.lmu.de/lehrveranstaltungen/bs-ws1819/"

links_array = []

ns = {'re': 'http://exslt.org/regular-expressions'}



def get_file_links():

    '''
    get the hyperlinks to pdf files with html parsing and add all links to array with hyperlinks
    '''
    # create response object from url
    r = requests.get(url)
    root = html.fromstring(r.content)

    for node in root.xpath('//a[re:test(@href, "\.pdf$", "i")]', namespaces=ns):
        links_array.append(urllib.parse.urljoin(url, node.attrib['href']))

    return links_array

#download pdf files
def download_files(links):

    '''
    download pdf files from hyperlinks

    :type links: list
    :param links: list with pdf hyperlinks
    '''
    for link in links:

        #download files in defined directory one by one iterating throw the file_links array

        # obtain filename by splitting url and getting the last string
        file_name = link.split('/')[-1]

        print("Downloading file: %s" % file_name)

        # create response object
        r = requests.get(link, stream=True)

        # start download
        with open(file_name, 'wb') as file_dir:
           file_dir.write(r.content)

        print("%s was downloaded!\n" % file_name)

    print("All files were saved in directory:%s" % os.getcwd())
    return


if __name__ == "__main__":
    links_array = get_file_links()
    download_files(links_array)
