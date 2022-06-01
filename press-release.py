from requests_html import HTMLSession
import csv
import re

urls_to_scrap = ["https://www.constructiondive.com/press-release/", "https://www.retaildive.com/press-release/",
                 "https://www.k12dive.com/press-release/", "https://www.healthcaredive.com/press-release/"]

# will add the scraped companies data to this list
companies_data_list = []


def page_request(url):  # request the page

    session = HTMLSession()
    response = session.get(url=url)
    session.close()
    response.close()
    return response


def get_base_url(url):

    return re.findall("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", url)[0]


# this function returns a list of the companies links in the page
def get_companies_links(response):

    companies_links_list = []
    # this will get a list of relative urls
    companies_urls_list = response.html.xpath(
        '//h3/a[@class="analytics t-pr-feed-item"]/@href')
    # looping through the companies links in the page
    for company_relative_url in companies_urls_list:
        # getting the absolute link for the company
        company_absolute_url = get_base_url(
            response.url) + company_relative_url
        companies_links_list.append(company_absolute_url)
    return companies_links_list


def scrap_companies(links_list):
    session = HTMLSession()
    # we get this script from website inspection
    email_decoding_script = """
    !function(){"use strict";function e(e){try{if("undefined"==typeof console)return;"error"in console?console.error(e):console.log(e)}catch(e){}}function t(e){return d.innerHTML='<a href="'+e.replace(/"/g,"&quot;")+'"></a>',d.childNodes[0].getAttribute("href")||""}function r(e,t){var r=e.substr(t,2);return parseInt(r,16)}function n(n,c){for(var o="",a=r(n,c),i=c+2;i<n.length;i+=2){var l=r(n,i)^a;o+=String.fromCharCode(l)}try{o=decodeURIComponent(escape(o))}catch(u){e(u)}return t(o)}function c(t){for(var r=t.querySelectorAll("a"),c=0;c<r.length;c++)try{var o=r[c],a=o.href.indexOf(l);a>-1&&(o.href="mailto:"+n(o.href,a+l.length))}catch(i){e(i)}}function o(t){for(var r=t.querySelectorAll(u),c=0;c<r.length;c++)try{var o=r[c],a=o.parentNode,i=o.getAttribute(f);if(i){var l=n(i,0),d=document.createTextNode(l);a.replaceChild(d,o)}}catch(h){e(h)}}function a(t){for(var r=t.querySelectorAll("template"),n=0;n<r.length;n++)try{i(r[n].content)}catch(c){e(c)}}function i(t){try{c(t),o(t),a(t)}catch(r){e(r)}}var l="/cdn-cgi/l/email-protection#",u=".__cf_email__",f="data-cfemail",d=document.createElement("div");i(document),function(){var e=document.currentScript||document.scripts[document.scripts.length-1];e.parentNode.removeChild(e)}()}();
    """

    for company_link in links_list:
        company_page_response = session.get(company_link)
        # getting the needed data from every company page
        try:
            compay_name = company_page_response.html.xpath(
                '//span[@class="header__wrapper__secondary-label"]/a/text()'
            )[0]
        except IndexError:
            compay_name = "Not Provided"
        try:
            date = company_page_response.html.xpath(
                '//div[@class="content__publish-date"]/text()')[0]
        except IndexError:
            date = "Not Provided"
        try:
            title = company_page_response.html.xpath(
                '//h1[@class="heading-02 header__wrapper__title"]/text()'
            )[0]
        except IndexError:
            title = "Not Provided"
        try:
            company_page_response.html.render(
                script=email_decoding_script, reload=False
            )
            pre_email_list = company_page_response.html.xpath(
                '//div[@class="content__contacts-wrapper__contact__email"]/a/text()'
            )
            if len(pre_email_list) == 0:
                pre_email = "Not Provided"
            elif len(pre_email_list) == 1:
                pre_email = pre_email_list[0]
            else:
                pre_email = pre_email_list
            print(
                f"Item No. ({links_list.index(company_link)+1})/({len(links_list)}) is Rendered Correctly"
            )
        except:
            print("EMAIL DID NOT RENDERED")
            pre_email = "Not Provided"

        # gathering data in a dictionary
        company_data = {
            "name": compay_name,
            "date": date,
            "title": title,
            "pre_email": pre_email,
            "company_url": company_link,
        }
        companies_data_list.append(company_data)
    # closing session
    company_page_response.close()


def export_to_csv(all_companies_data):

    field_names = ["name", "date", "title", "pre_email", "company_url"]
    with open("companies.csv", "w", encoding="UTF-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(all_companies_data)
    print("exported to csv file")


def start_scraping(url):

    page_response = page_request(url)
    while True:
        companies_links_list = get_companies_links(page_response)
        scrap_companies(companies_links_list)
        # check if it is the last page if there is a next page
        if (page_response.html.xpath('//div[@class="pagination"]/a [position()= last()]/text()[2]')[0]
                .strip() == "Next"):
            print("*****GOING TO THE NEXT PAGE*****")
            page_response = page_request(page_response.html.next())
        else:
            print("----------Finished---------")
            break


for url in urls_to_scrap:
    print(f"start scraping website: {get_base_url(url)}")
    start_scraping(url)
export_to_csv(companies_data_list)
