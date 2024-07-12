import os
from os import path
import pandas as pd

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from utils.context import data_dir, plot_dir

## CONFIG ##
DATA_FOLDER = path.join(data_dir, "viterbi-ball")


## PROCESS DATA ##
df = pd.read_csv(path.join(DATA_FOLDER, "viterbi-ball-feedback.tsv"), delimiter="\t",
                 names=["time", "attended", "rating", "good_things", "bad_things"], skiprows=1)

# main columns are good_things and bad_things. good_things/bad_things is the feedback given by the user
# which can be any sentence or phrase. We can use this to generate a word cloud separately.
df["good_things"] = df["good_things"].str.lower()
df["bad_things"] = df["bad_things"].str.lower()
df["good_things"] = df["good_things"].str.replace(r'[^\w\s]', '')
df["bad_things"] = df["bad_things"].str.replace(r'[^\w\s]', '')
df["good_things"] = df["good_things"].str.split()
df["bad_things"] = df["bad_things"].str.split()

# accumulate all good_things/bad_things in a list
good_things = []
for i in df["good_things"]:
    good_things.extend(i)
good_things = pd.Series(good_things)
bad_things = []
for i in df["bad_things"]:
    bad_things.extend(i)
bad_things = pd.Series(bad_things)

# remove stopwords
remove_words = ["good", "liked", "really"]
good_things = good_things[~good_things.isin(remove_words)]
remove_words = ["bad", "disliked", "better", "good", "really"]
bad_things = bad_things[~bad_things.isin(remove_words)]

# plot using wordcloud library
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(good_things))
plt.figure(figsize=(10, 5))
wordcloud.to_file(path.join(plot_dir, "02a-wordcloud-good-things.png"))

wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(bad_things))
plt.figure(figsize=(10, 5))
wordcloud.to_file(path.join(plot_dir, "02b-wordcloud-bad-things.png"))

# plot the ratings
plt.figure(figsize=(10, 5))
df["rating"].value_counts().sort_index().plot(kind="bar")
plt.savefig(path.join(plot_dir, "02c-viterbi-ball-feedback-ratings.png"))

print("Complete../")
