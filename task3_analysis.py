import pandas as pd
import numpy as np

# Loaded the cleaned CSV from Task 2
df = pd.read_csv("data/trends_clean.csv")

print(f"Loaded data: {df.shape}")

# Display the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Display the number of rows and columns
print(f"\nShape: {df.shape}")

# Calculate average score and average comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")

# Calculate statistics using NumPy
scores = df["score"].to_numpy()

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")

# Find the highest and lowest scores
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Find the category with the most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_category_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

# Find the story with the highest number of comments
most_commented = df.loc[df["num_comments"].idxmax()]

print(
    f'Most commented story: "{most_commented["title"]}" '
    f'— {most_commented["num_comments"]} comments'
)

# Calculate engagement for each story
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Mark stories as popular when their score is above the average
df["is_popular"] = df["score"] > average_score

print("\nNew columns added: engagement, is_popular")
print(df[["title", "engagement", "is_popular"]].head())

# Saving the analysed data
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")