import requests
import xml.etree.ElementTree as ET
import csv
import time

# List of European country codes
european_country_codes = [
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE",
    "GR", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "NO",
    "PL", "PT", "RO", "SK", "SI", "ES", "SE", "CH", "GB"
]

output_file = "google_trends/google_trends_europe.csv"
headers = [
    "Country Code", "Title", "Link", "Publication Date", "Approx Traffic",
    "Description", "Picture", "Picture Source", "News Item Titles",
    "News Item URLs", "News Item Pictures", "News Item Sources"
]

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    for country_code in european_country_codes:
        rss_feed_url = f"https://trends.google.com/trending/rss?geo={country_code}"
        
        response = requests.get(rss_feed_url)
        if response.status_code != 200:
            print(f"Failed to fetch RSS feed for {country_code}. Status code: {response.status_code}")
            continue
        
        root = ET.fromstring(response.content)

        for item in root.findall(".//item"):
            title = item.findtext("title", default="N/A")
            link = item.findtext("link", default="N/A")
            pub_date = item.findtext("pubDate", default="N/A")
            approx_traffic = item.findtext("{https://trends.google.com/trending/rss}approx_traffic", default="N/A")
            description = item.findtext("description", default="N/A")
            picture = item.findtext("{https://trends.google.com/trending/rss}picture", default="N/A")
            picture_source = item.findtext("{https://trends.google.com/trending/rss}picture_source", default="N/A")

            news_item_titles = []
            news_item_urls = []
            news_item_pictures = []
            news_item_sources = []

            for news_item in item.findall("{https://trends.google.com/trending/rss}news_item"):
                news_item_titles.append(news_item.findtext("{https://trends.google.com/trending/rss}news_item_title", default="N/A"))
                news_item_urls.append(news_item.findtext("{https://trends.google.com/trending/rss}news_item_url", default="N/A"))
                news_item_pictures.append(news_item.findtext("{https://trends.google.com/trending/rss}news_item_picture", default="N/A"))
                news_item_sources.append(news_item.findtext("{https://trends.google.com/trending/rss}news_item_source", default="N/A"))

            news_item_titles_str = "; ".join(news_item_titles) if news_item_titles else "N/A"
            news_item_urls_str = "; ".join(news_item_urls) if news_item_urls else "N/A"
            news_item_pictures_str = "; ".join(news_item_pictures) if news_item_pictures else "N/A"
            news_item_sources_str = "; ".join(news_item_sources) if news_item_sources else "N/A"

            writer.writerow([
                country_code, title, link, pub_date, approx_traffic, description,
                picture, picture_source, news_item_titles_str, news_item_urls_str,
                news_item_pictures_str, news_item_sources_str
            ])
        time.sleep(1)

print(f"Data successfully written to {output_file}")
