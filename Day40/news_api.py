import requests
import json

def build_url(base_url, query, from_date, to_date, sort_by, api_key):
    url = f"{base_url}?q={query}"

    if from_date:
        url += f"&from={from_date}"
    if to_date:
        url += f"&to={to_date}"
    if sort_by:
        url += f"&sortBy={sort_by}"
    
    url += f"&apiKey={api_key}"

    return url


def main():
    print("=== NewsAPI Fetcher ===")

    # 🔹 User Inputs
    query = input("Enter search keyword: ").strip()
    from_date = input("From date (YYYY-MM-DD, optional): ").strip()
    to_date = input("To date (YYYY-MM-DD, optional): ").strip()
    sort_by = input("Sort by (relevancy/popularity/publishedAt): ").strip()
    # api_key = input("Enter your NewsAPI key: ").strip()
    API_KEY = "81c6793e75944e5191123468a39d3674"

    base_url = "https://newsapi.org/v2/everything"

    # 🔹 Build URL
    url = build_url(base_url, query, from_date, to_date, sort_by, API_KEY)

    print("\nFetching news...\n")

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("status") != "ok":
            print(" Error:", data)
            return

        articles = data.get("articles", [])

        if not articles:
            print("No articles found.")
            return

        # 🔹 Extract useful data
        results = []
        for article in articles:
            item = {
                "title": article.get("title"),
                "author": article.get("author"),
                "source": article.get("source", {}).get("name"),
                "publishedAt": article.get("publishedAt"),
                "url": article.get("url"),
                "description": article.get("description"),
                "content":article.get("content")    
            }
            results.append(item)

        # 🔹 Save to file
        with open("news_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

        print(f"Saved {len(results)} articles to news_results.json")

    except Exception as e:
        print(" Error occurred:", e)


if __name__ == "__main__":
    main()