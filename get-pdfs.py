# get-pdfs
# this function will scrape the mass.gov COVID-19 report archive and save the reports to a location of choice

# libraries to use
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# where to save pdfs
pdf_save_loc = Path("C:/Users/Nigel/PycharmProjects/covid-MA-analyzer/covid-MA-data")

# scrape mass.gov COVID-19 cases archive
mass_covid_url = "https://www.mass.gov/info-details/archive-of-covid-19-cases-in-massachusetts"
mass_covid_url_domain = "/".join(mass_covid_url.split("/", 3)[:3])
mass_covid_request = requests.get(mass_covid_url)
mass_covid_soup = BeautifulSoup(mass_covid_request.content, 'html.parser')

# get all report links
mass_covid_a_tags = mass_covid_soup.find_all('a')
mass_covid_report_links = []
for link in mass_covid_a_tags:
    link_href = link.get('href')
    # avoid empty links
    if link_href:
        if "download" in link_href or ".pdf" in link_href or ".docx" in link_href:
            mass_covid_report_link = mass_covid_url_domain + link_href
            # add report link if it isn't already in the report links list
            mass_covid_report_links.append(mass_covid_url_domain + link_href)

# extract pdf and docx links
mass_covid_report_pdfs = mass_covid_report_links[::2]
mass_covid_report_docxs = mass_covid_report_links[1::2]
