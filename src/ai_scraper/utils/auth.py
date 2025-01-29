from playwright.sync_api import sync_playwright
import yaml

def login(domain):
    with open("config/credentials.yaml") as f:
        creds = yaml.safe_load(f).get(domain, {})
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://{domain}/login")
        page.fill(creds["username_selector"], creds["username"])
        page.fill(creds["password_selector"], creds["password"])
        page.click(creds["submit_selector"])
        cookies = page.context.cookies()
        browser.close()
        return {c["name"]: c["value"] for c in cookies}