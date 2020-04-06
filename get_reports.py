# get_reports
# this function will scrape the mass.gov COVID-19 report archive and save the reports to a location of choice
#
# Usage:
# get_reports <pdf_save_loc> <docx_save_loc>
#
# Arguments:
# pdf_save_loc - the folder location where scraped pdfs reports will be stored
# docx_save_loc - the folder location where scraped docx reports will be stored

import requests
import sys
import os
import urllib
from bs4 import BeautifulSoup
from pathlib import Path


def get_reports(argv):

    # parse arguments for where to save reports
    if len(argv) < 3:
        raise NotADirectoryError("Missing arguments: " + argv[0] + " <pdf_save_loc> <docx_save_loc>")
    pdf_save_loc = os.path.abspath(Path(argv[1]))
    docx_save_loc = os.path.abspath(Path(argv[2]))

    # create save locations if not already existing
    if not os.path.isdir(pdf_save_loc):
        os.mkdir(pdf_save_loc)
    if not os.path.isdir(docx_save_loc):
        os.mkdir(docx_save_loc)

    # scrape mass.gov COVID-19 cases archive
    mass_covid_url = "https://www.mass.gov/info-details/archive-of-covid-19-cases-in-massachusetts"
    mass_covid_url_domain = "/".join(mass_covid_url.split("/", 3)[:3])
    print("Retrieving data from: " + mass_covid_url + "...")
    mass_covid_request = requests.get(mass_covid_url)
    mass_covid_soup = BeautifulSoup(mass_covid_request.content, 'html.parser')

    # get all report links
    # TODO: scrape href text in addition to link and get a list of dates, also allows for a better way of separating doc
    # files from pdfs and not accidentally downloading any unwanted files
    print("Scraping downloads...")
    mass_covid_a_tags = mass_covid_soup.find_all('a')
    mass_covid_report_links = []
    for link in mass_covid_a_tags:
        link_href = link.get('href')
        # avoid empty links
        if link_href:
            if "download" in link_href or ".pdf" in link_href or ".docx" in link_href:
                mass_covid_report_links.append(mass_covid_url_domain + link_href)

    # extract pdf and docx links
    mass_covid_pdf_links = mass_covid_report_links[::2]
    mass_covid_docx_links = mass_covid_report_links[1::2]

    # TODO: save pdf and docx reports
    print("Saving .pdf reports to: " + str(pdf_save_loc) + "...")
    for pdf_link in mass_covid_pdf_links:
        print(pdf_link.split("/")[-1] + ".pdf")
        # pdf_path = Path(pdf_save_loc, pdf[])
        # urllib.urlretrieve(pdf_link, pdf_path)
    print("Saving .docx reports to: " + str(docx_save_loc) + "...")
    for docx_link in mass_covid_docx_links:
        print(docx_link.split("/")[-1] + ".docx")
        # docx_path = Path(docx_save_loc, pdf[])
        # urllib.urlretrieve(docx_link, docx_path)


if __name__ == "__main__":
    get_reports(sys.argv)
