import os
import pandas as pd
import matplotlib.pyplot as plt

# Load the analysed data from Task 3
df = pd.read_csv("data/trends_analysed.csv")

# Create the outputs folder if it does not already exist
os.makedirs("outputs", exist_ok=True)

print(f"Loaded data: {df.shape}")

# Select the 10 stories with the highest scores
top_stories = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title if len(title) <= 50 else title[:50] + "..."
)

# Create a horizontal bar chart 1

plt.figure(figsize=(10, 6))
plt.barh(top_stories["short_title"], top_stories["score"])

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

# Put the highest-scoring story at the top
plt.gca().invert_yaxis()

plt.tight_layout()

# Save the chart before displaying it
plt.savefig("outputs/chart1_top_stories.png")
plt.show()
plt.close()



# Count stories in each category chart 2

category_counts = df["category"].value_counts()

# Create a bar chart with a different colour for each category
colors = plt.cm.tab10(range(len(category_counts)))

plt.figure(figsize=(10, 6))
plt.bar(category_counts.index, category_counts.values, color=colors)

plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.tight_layout()

# Save the chart before displaying it
plt.savefig("outputs/chart2_categories.png")
plt.show()
plt.close()

# Separate popular and non-popular stories chart 3

popular = df["is_popular"] == True
not_popular = df["is_popular"] == False

# Create a scatter plot
plt.figure(figsize=(10, 6))

plt.scatter(
    df.loc[not_popular, "score"],
    df.loc[not_popular, "num_comments"],
    label="Not Popular"
)

plt.scatter(
    df.loc[popular, "score"],
    df.loc[popular, "num_comments"],
    label="Popular"
)

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()

plt.tight_layout()

# Save the chart before displaying it
plt.savefig("outputs/chart3_scatter.png")
plt.show()
plt.close()


# Create one dashboard containing all three charts
fig, axes = plt.subplots(1, 3, figsize=(20, 7))

# Chart 1: Top 10 stories
axes[0].barh(top_stories["short_title"], top_stories["score"])
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")
axes[0].invert_yaxis()

# Chart 2: Stories per category
axes[1].bar(
    category_counts.index,
    category_counts.values,
    color=colors
)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].tick_params(axis="x", rotation=45)

# Chart 3: Score vs comments
axes[2].scatter(
    df.loc[not_popular, "score"],
    df.loc[not_popular, "num_comments"],
    label="Not Popular"
)

axes[2].scatter(
    df.loc[popular, "score"],
    df.loc[popular, "num_comments"],
    label="Popular"
)

axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

# Add the overall dashboard title
fig.suptitle("TrendPulse Dashboard", fontsize=18)

plt.tight_layout()

# Save the complete dashboard
plt.savefig("outputs/dashboard.png")
plt.show()
plt.close()