from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

# Set up WebDriver (Chrome)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (optional)
service = Service('path/to/chromedriver')  # Replace with the path to your WebDriver
driver = webdriver.Chrome()

# Main team page URL
TEAM_PAGE_URL = "https://www.lawlanesolicitors.co.uk/our-team/"

def fetch_profile_links():
    """Fetches all profile links from the team page."""
    driver.get(TEAM_PAGE_URL)
    time.sleep(2)  # Wait for the page to load
    profile_links = driver.find_elements(By.CSS_SELECTOR, "a.teama")
    return [link.get_attribute("href") for link in profile_links]

def fetch_profile_data(profile_url):
    """Fetches detailed data from a profile page."""
    driver.get(profile_url)
    time.sleep(2)  # Wait for the page to load

    try:
        # Extract profile data
        image = driver.find_element(By.CSS_SELECTOR, ".wp-block-media-text__media img").get_attribute("src")
        email = driver.find_element(By.CSS_SELECTOR, 'a[href^="mailto:"]').text
        designation = driver.find_element(By.XPATH, "//p[strong[contains(text(),'Designation')]]").text.split(":")[1].strip()
        languages = driver.find_element(By.XPATH, "//p[strong[contains(text(), 'Languages')]]").text.split(":")[1].strip()
        ul_element = driver.find_element(By.XPATH, "//p[strong[contains(text(), 'Practice Areas:')]]/following-sibling::ul[1]")
        # Extract all list items from the `<ul>`
        practice_areas = [li.text for li in ul_element.find_elements(By.TAG_NAME, "li")]

        return {
            "name":driver.find_element(By.XPATH,'//h1').text,
            "image": image,
            "email": email,
            "designation": designation,
            "languages": languages,
            "practice_areas": practice_areas,
        }
    except Exception as e:
        print(f"Error fetching data for {profile_url}: {e}")
        return None

def main():
    """Main scraping function."""
    profiles = []
    profile_links = fetch_profile_links()
    print(f"Found {len(profile_links)} profiles.")

    for link in profile_links:
        print(f"Fetching profile: {link}")
        profile_data = fetch_profile_data(link)
        if profile_data:
            profiles.append(profile_data)

    # Save data to JSON file
    with open("profiles.json", "w") as file:
        json.dump(profiles, file, indent=2)

    print("Profile data saved to profiles.json")

# Run the script
if __name__ == "__main__":
    main()

# Close the browser
driver.quit()
