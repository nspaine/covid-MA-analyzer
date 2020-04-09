# get_reports
# this function will scrape the mass.gov COVID-19 report archive and save the reports to a location of choice
#
# Usage:
# get_reports <pdf_save_loc> <docx_save_loc>
#
# Arguments:
# pdf_save_loc - the folder location where scraped pdfs reports will be stored
# docx_save_loc - the folder location where scraped docx reports will be stored

import grequests
import sys
import os
import time
import warnings
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin


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
    print("Retrieving data from: " + mass_covid_url + "...")
    mass_covid_request = grequests.get(mass_covid_url)
    mass_covid_resp = grequests.map([mass_covid_request])
    mass_covid_soup = BeautifulSoup(mass_covid_resp[0].text, 'html.parser')

    # get PDF and DOCX report links and dates
    mass_covid_a_tags = mass_covid_soup.find_all('a')
    mass_covid_report_pdf_links = []
    mass_covid_report_docx_links = []
    mass_covid_report_dates = []
    pdf_match_str = "COVID-19 cases in Massachusetts as of "
    docx_match_str = "Doc"
    print("Scraping archive for PDF and DOCX reports...")
    for idx, link in enumerate(mass_covid_a_tags):
        pdf_link_text = str(link.string)
        if pdf_link_text.startswith(pdf_match_str):

            # DATE
            try:
                report_date = time.strptime(pdf_link_text, pdf_match_str + "%B %d, %Y")
                mass_covid_report_dates.append(report_date)
            except ValueError:
                warnings.warn(pdf_link_text + " does not contain a date.")
                mass_covid_report_dates.append(None)

            # PDF LINK
            pdf_href = link.get('href')
            pdf_full_link = urljoin(mass_covid_url, pdf_href)
            mass_covid_report_pdf_links.append(pdf_full_link)

            # DOCX LINK
            if idx < (len(mass_covid_a_tags) - 1):
                docx_link = mass_covid_a_tags[idx+1]
                docx_link_text = str(docx_link.string)
                if docx_link_text == docx_match_str:
                    docx_href = docx_link.get('href')
                    docx_full_link = urljoin(mass_covid_url, docx_href)
                    mass_covid_report_docx_links.append(docx_full_link)
                else:
                    warnings.warn(docx_link_text + " does not match DOCX name " + docx_match_str)
                    mass_covid_report_docx_links.append(None)
            else:
                warnings.warn("DOCX does not exist for " + pdf_link_text)
                mass_covid_report_docx_links.append(None)

    print("Requesting link content types...")
    if not mass_covid_report_pdf_links and not mass_covid_report_docx_links:
        raise IndexError("No valid report links found in " + mass_covid_url)
    report_links = mass_covid_report_pdf_links + mass_covid_report_docx_links
    report_requests = grequests.map((grequests.get(report) for report in report_links))

    # TODO: validate PDF and DOCX types then save
    print("Validating PDF and DOCX types...")
    for report in report_requests:
        link_content_type = report.headers['content-type']
        print(link_content_type)
    '''
    if link_content_type != "application/pdf":
        mass_covid_report_pdf_links.append(None)
        warnings.warn(full_link + " is not a PDF, content type is " + link_content_type)
    else:
        mass_covid_report_pdf_links.append(full_link)
    # TODO: save pdf and docx reports
    # Save PDF and DOCX reports to save locations
    print("Saving .pdf reports to: " + str(pdf_save_loc) + "...")
    for pdf_link in mass_covid_pdf_links:
        pdf_name = pdf_link.split("/")[-1]
        if not pdf_name.endswith(".pdf"):
            pdf_name = pdf_name + ".pdf"
        #print(pdf_name)
        # pdf_path = Path(pdf_save_loc, pdf[])
        # urllib.urlretrieve(pdf_link, pdf_path)
    print("Saving .docx reports to: " + str(docx_save_loc) + "...")
    for docx_link in mass_covid_docx_links:
        docx_name = docx_link.split("/")[-1]
        if not docx_name.endswith(".docx"):
            docx_name = docx_name + ".docx"
        #print(docx_name)
        # docx_path = Path(docx_save_loc, pdf[])
        # urllib.urlretrieve(docx_link, docx_path)
    '''


if __name__ == "__main__":
    get_reports(sys.argv)
