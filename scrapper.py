from playwright.sync_api import sync_playwright


def get_blog_titles(query):
    print(f"[INFO] Searching blog titles for: {query}")

    titles = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        search_url = f"https://dev.to/search?q={query}"
        page.goto(search_url)

        page.wait_for_selector("h3.crayons-story__title a", timeout=5000)

        links = page.query_selector_all("h3.crayons-story__title a")

        for link in links:
            title = link.inner_text().strip()
            titles.append(title)

        browser.close()

    print(f"[INFO] Found {len(titles)} titles.")
    if not titles:
        print("[WARN] No titles found.")
    print("[FINAL OUTPUT]", titles)
    return titles


# if __name__ == "__main__":
 #   get_blog_titles("python")
