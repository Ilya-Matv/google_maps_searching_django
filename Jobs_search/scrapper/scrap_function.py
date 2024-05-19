"""This script serves as an example on how to use Python 
   & Playwright to scrape/extract data from Google Maps"""

from playwright.sync_api import sync_playwright
from .Global_Variable_Manager import GlobalVariable



def extract_coordinates_from_url(url: str) -> tuple[float,float]:
    """helper function to extract coordinates from url"""
    
    coordinates = url.split('/@')[-1].split('/')[0]
    # return latitude, longitude
    return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])


def start_scrap(queue, search_list=None, total=None):
    
    ########
    # input 
    ########
    
    
    # read search from arguments
    if search_list is None:
        search_list = []
    
        
    if total == 'all':
        total = 1_000_000

        
    ###########
    # scraping
    ###########
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)
        # wait is added for dev phase. can remove it in production
        page.wait_for_timeout(5000)
        
        for search_for_index, search_for in enumerate(search_list):
            print(f"-----\n{search_for_index} - {search_for}".strip())

            page.locator('//input[@id="searchboxinput"]').fill(search_for)
            page.wait_for_timeout(3000)

            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)

            # scrolling
            page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

            # this variable is used to detect if the bot
            # scraped the same number of listings in the previous iteration
            previously_counted = 0
            while True:
                page.mouse.wheel(0, 10000)
                page.wait_for_timeout(3000)

                if (
                    page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count()
                    >= total
                ):
                    listings = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).all()[:total]
                    listings = [listing.locator("xpath=..") for listing in listings]
                    print(f"Total Scraped: {len(listings)}")
                    break
                else:
                    # logic to break from loop to not run infinitely
                    # in case arrived at all available listings
                    if (
                        page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        == previously_counted
                    ):
                        listings = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).all()
                        print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                        break
                    else:
                        previously_counted = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        print(
                            f"Currently Scraped: ",
                            page.locator(
                                '//a[contains(@href, "https://www.google.com/maps/place")]'
                            ).count(),
                        )

            progress_number = 0
            list = []
            # scraping
            for listing in listings:
                business_data = {}
                try:
                    listing.click()
                    page.wait_for_timeout(5000)

                    name_xpath = '//div[contains(@class, "fontHeadlineSmall")]'
                    address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                    website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                    phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'

                    
                    if listing.locator(name_xpath).count() > 0:
                        business_data['name'] = listing.locator(name_xpath).all()[0].inner_text()
                    else:
                        business_data['name'] = ""
                    if page.locator(address_xpath).count() > 0:
                        business_data['address'] = page.locator(address_xpath).all()[0].inner_text()
                    else:
                        business_data['address'] = ""
                    if page.locator(website_xpath).count() > 0:
                        business_data['website'] = page.locator(website_xpath).all()[0].inner_text()
                    else:
                        business_data['website'] = ""
                    if page.locator(phone_number_xpath).count() > 0:
                        business_data['phone_number'] = page.locator(phone_number_xpath).all()[0].inner_text()
                    else:
                        business_data['phone_number'] = ""
                    
                    
                except Exception as e:
                    print(f'Error occured: {e}')
                list.append(business_data)
                progress_number += 1
                queue.put(progress_number)
                
               
                
                
                                    
            
            #########
            # output
            #########
           
        browser.close()
    
    queue.put(list)
    

