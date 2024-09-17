from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
import time

SBR_WEBDRIVER = 'https://brd-customer-hl_53433a84-zone-ai_scraper:i2vtxtoctt9p@brd.superproxy.io:9515'

def scrape_website(website):
    print("Launching Chrome browser...")

    # Set up the remote connection with Scraping Browser
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')

    try:
        # Use the Chrome WebDriver with options
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            driver.set_page_load_timeout(30)  # Set a timeout for loading the page
            driver.get(website)
            
            # CAPTCHA handling
            print('Waiting for CAPTCHA to solve...')
            try:
                solve_res = driver.execute(
                    "executeCdpCommand",
                    {
                        'cmd': 'Captcha.waitForSolve',
                        'params': {'detectTimeout': 10000},
                    },
                )
                print('CAPTCHA solve status:', solve_res['value']['status'])
            except Exception as e:
                print("CAPTCHA solving error:", e)
            
            print('Page navigated! Scraping page content...')
            html = driver.page_source

            return html

    except Exception as e:
        print(f"Error occurred during scraping: {e}")
        return None


def extract_body_content(html_content):
    """Extracts the body content from the HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    """Cleans the extracted body content by removing scripts and styles."""
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove <script> and <style> elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get cleaned text
    clean_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in clean_content.splitlines() if line.strip()
    )
    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    """Splits DOM content into chunks to avoid processing large data at once."""
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
