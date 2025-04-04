from playwright.sync_api import sync_playwright


def get_blog_titles(query):
    print(f"[INFO] Searching blog titles for: {query}")
    titles = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            # Important for containerized environments
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = browser.new_page()

        try:
            search_url = f"https://dev.to/search?q={query}"
            print(f"[INFO] Navigating to: {search_url}")
            page.goto(search_url, timeout=30000)

            # More reliable than wait_for_selector in some cases
            page.wait_for_load_state("networkidle")
            page.wait_for_selector("h3.crayons-story__title a", timeout=10000)

            links = page.query_selector_all("h3.crayons-story__title a")

            for link in links:
                title = link.inner_text().strip()
                if title:
                    titles.append(title)

        except Exception as e:
            print(f"[ERROR] Failed to fetch titles: {e}")

        finally:
            browser.close()

    print(f"[INFO] Found {len(titles)} titles.")
    if not titles:
        print("[WARN] No titles found.")
    print("[FINAL OUTPUT]", titles)
    return titles
