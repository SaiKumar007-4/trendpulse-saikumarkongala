import pandas as pd

# Load the JSON file created in Task 1
input_file = "data/trends_20260901.json"

df = pd.read_json(input_file)

print(f"Loaded {len(df)} stories from {input_file}")

# Remove duplicate stories using post_id as the unique identifier
df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")

# Remove rows where important fields are missing
df = df.dropna(subset=["post_id", "title", "score"])

print(f"After removing nulls: {len(df)}")

# Convert score and num_comments to integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)
# Remove stories with a score below 5
df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")

# Remove extra spaces from the beginning and end of titles
df["title"] = df["title"].str.strip()

# Save the cleaned data as a CSV file
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# Show how many stories belong to each category
print("\nStories per category:")
print(df["category"].value_counts())