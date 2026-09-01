import requests
import json
import os
import time
from datetime import datetime

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"

ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {
    "User-Agent": "TrendPulse/1.0"
}

categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "Netflix", "game", "book",
        "show", "award", "streaming"
    ]
}

#Test the Hacker News API by getting the story IDs 
try:
    response = requests.get(TOP_STORIES_URL, headers=headers, timeout=10)
    response.raise_for_status()
    story_ids = response.json()[:500]

    print("API connection successful!")
    print("Number of story IDs retrieved:", len(story_ids))
    print("First 5 story IDs:", story_ids[:5])

except requests.RequestException as error:
    print("Failed to fetch top stories:", error)

# Store the details of successfully fetched stories
all_stories = []

for number, story_id in enumerate(story_ids, start=1):
    try:
        story_url = ITEM_URL.format(story_id)

        response = requests.get(
            story_url,
            headers=headers,
            timeout=5
        )

        response.raise_for_status()

        story = response.json()

        # Only keep items that contain a title
        if story and story.get("title"):
            all_stories.append(story)

        # Show progress so we know the program is still running
        if number % 25 == 0:
            print(f"Processed {number}/500 stories...")

    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        continue

print("Successfully fetched", len(all_stories), "stories.")

# Keep track of how many stories we collect in each category
category_stories = {
    "technology": [],
    "worldnews": [],
    "sports": [],
    "science": [],
    "entertainment": []
}

# Check the titles against the keywords for each category
for category, keywords in categories.items():

    for story in all_stories:

        # Stop once this category has 25 stories
        if len(category_stories[category]) >= 25:
            break

        title = story.get("title", "")
        title_lower = title.lower()

        # Check whether any keyword appears in the title
        for keyword in keywords:
            if keyword.lower() in title_lower:

                category_stories[category].append(story)
                break

    # Wait 2 seconds before processing the next category
    time.sleep(2)

# Display the number of stories collected in each category
for category, stories in category_stories.items():
    print(f"{category}: {len(stories)} stories")

# Create the final list using only the required fields
final_stories = []

for category, stories in category_stories.items():

    for story in stories:
        story_data = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().isoformat()
        }

        final_stories.append(story_data)

print(f"Total stories prepared: {len(final_stories)}")

# Create the data folder if it does not already exist
os.makedirs("data", exist_ok=True)

# Create a filename using today's date
date_string = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{date_string}.json"

# Save all collected stories to the JSON file
with open(filename, "w", encoding="utf-8") as file:
    json.dump(final_stories, file, indent=4)

print(f"Collected {len(final_stories)} stories. Saved to {filename}")