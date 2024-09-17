from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
import time
import httpx

SBR_WEBDRIVER = 'https://brd-customer-hl_53433a84-zone-ai_scraper:i2vtxtoctt9p@brd.superproxy.io:9515'

def scrape_website(website, retries=3):
    print("Launching chrome browser...")

    attempt = 0
    while attempt < retries:
        try:
            sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
            with Remote(sbr_connection, options=ChromeOptions()) as driver:
                driver.get(website)
                
                # CAPTCHA handling
                print('Waiting for CAPTCHA to solve...')
                solve_res = driver.execute(
                    "executeCdpCommand",
                    {
                        'cmd': 'Captcha.waitForSolve',
                        'params': {'detectTimeout': 10000},
                    },
                )
                print('CAPTCHA solve status:', solve_res['value']['status'])
                print('Navigated! Scraping page content...')
                html = driver.page_source
                
                return html

        except (httpx.ConnectError, httpx.RequestError) as e:
            attempt += 1
            print(f"Retrying due to error: {e}. Attempt {attempt}/{retries}")
            time.sleep(5)  # Delay before retrying
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            break  # Exit retry loop for unexpected errors

    # If all retries fail, raise an exception or return a failure message
    raise RuntimeError("Failed to scrape the website after several attempts.")

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    clean_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in clean_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
