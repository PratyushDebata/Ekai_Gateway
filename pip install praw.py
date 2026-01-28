import json
import requests
from datetime import datetime

TARGET_SUBREDDITS = ["ClaudeAI", "claudeCode"]
SEARCH_KEYWORDS = ["limit", "pricing", "error", "complaint", "bug", "rate limit", "pay", "cost"]

OUTPUT_PATH = "c:/Users/ASUS/Desktop/reddit_posts.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def post_matches_criteria(title, body):
    """Check if post matches search criteria"""
    text = (title + " " + body).lower()
    return any(keyword.lower() in text for keyword in SEARCH_KEYWORDS)


def fetch_reddit_posts(subreddit_name, limit=100):
    """Fetch posts from a subreddit using reddit's JSON endpoint"""
    posts = []
    try:
        
        for sort_type in ["hot", "new", "top"]:
            if len(posts) >= 3:
                break
                
            url = f"https://www.reddit.com/r/{subreddit_name}/{sort_type}.json"
            params = {"limit": limit, "t": "week"}  # Last week
            
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "data" in data and "children" in data["data"]:
                for child in data["data"]["children"]:
                    if len(posts) >= 3:
                        break
                        
                    post = child.get("data", {})
                    
                    title = post.get("title", "")
                    body = post.get("selftext", "")
                    post_url = "https://reddit.com" + post.get("permalink", "")
                    
                    if post_matches_criteria(title, body):
                        posts.append({
                            "subreddit": subreddit_name,
                            "title": title,
                            "body": body[:1000] if body else "[No text content - likely a link post]",
                            "url": post_url,
                            "posted_at": datetime.fromtimestamp(post.get("created_utc", 0)).isoformat()
                        })
        
        print(f"✓ Fetched {len(posts)} qualifying posts from r/{subreddit_name}")
        return posts
        
    except Exception as e:
        print(f"✗ Error fetching from r/{subreddit_name}: {e}")
        return []


def gather_posts():
    """Gather posts from all target subreddits"""
    all_posts = []
    
    for subreddit in TARGET_SUBREDDITS:
        posts = fetch_reddit_posts(subreddit, limit=100)
        all_posts.extend(posts)
    
    return all_posts[:3] 


def main():
    print("Fetching Reddit posts...")
    posts = gather_posts()
    
    if posts:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Successfully exported {len(posts)} posts to {OUTPUT_PATH}")
        print("\nPosts saved:")
        for i, post in enumerate(posts, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   Subreddit: r/{post['subreddit']}")
            print(f"   URL: {post['url']}")
    else:
        print("✗ No posts found matching criteria")


if __name__ == "__main__":
    main()