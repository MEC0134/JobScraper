import asyncio
from pyppeteer.launcher import launch

async def main():

    # launch the browser
    browser = await launch(headless=False)

    # open a new page 
    page = await browser.newPage()

    # go to indeed.com
    await page.goto('https://tr.indeed.com/')

    # wait for the input fields to load
    await page.waitForSelector('text-input-what')
    await page.waitForSelector('text-input-where')

    # type in the job title and geo-location
    await page.type('text-input-what', 'Yazılımcı')
    await page.type('text-input-where', 'Türkiye')

    # lauch search
    await page.click('button[type="submit"]')

    # wait for next page to load
    await page.waitForNavigation()


    # once page with job listings is loaded 
    job_listings = await page.querySelectorAll('.resultContent')
    for job in job_listings:
        # Extract job title
        title_element = await job.querySelector('h2.jobTitle span[title]')
        title = await page.evaluate('(element) => element.textContent', title_element)

        # Exract company name
        company_element = await job.querySelector('div.company_location [data-testid="company-name"]')
        company = await page.evaluate('(element) => element.textContent', company_element)

        # Extract location
        location_element = await job.querySelector('div.company_location [data-testid="text-location"]') 
        location = await page.evaluate('(element) => element.textContent', location_element)


        print({'title': title, 'company': company, 'location': location})

        # close the browser
        await browser.close()

    