from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # 1. Total Number of Messages
    num_messages = df.shape[0]

    # 2. Total Number of Words
    words = []
    for message in df["message"]:
        words.extend(message.split())

    # 3. Total Media Shared
    num_media = df[df["message"] == "<Media omitted>\n"].shape[0]


    # 4. Toatl Link Shared
    extractor = URLExtract()
    links = []
    for message in df["message"]:
        links.extend(extractor.find_urls(message))
    return num_messages, len(words), num_media, len(links)

def most_active_users(df):
    x = df["user"].value_counts()
    df = round((df["user"].value_counts()/df.shape[0])*100, 2).reset_index().\
        rename(columns={"index": "Name", "user": "Percentage of Activity"})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # remove group notification, Media omitted, This message was deleted
    temp = df[df["user"] != "group_notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]
    temp = temp[temp["message"] != "This message was deleted\n"]

    def remove_stop_words(message):
        file = open("stop_hinglish.txt", "r")
        stop_words = file.read()
        words = []

        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)

    temp["message"] = temp["message"].apply(remove_stop_words)
    wc = WordCloud(width=1300, height=700, background_color="black", min_font_size=10)
    df_wc = wc.generate(temp["message"].str.cat(sep=" "))
    return df_wc

def most_common_word(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # remove group notification, Media omitted, This message was deleted
    temp = df[df["user"] != "group_notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]
    temp = temp[temp["message"] != "This message was deleted\n"]

    file = open("stop_hinglish.txt", "r")
    stop_words = file.read()

    words = []
    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(10))[::-1]
    most_common_df.rename(columns={0: 'Word', 1: 'Count'}, inplace=True)
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([i for i in message if i in emoji.distinct_emoji_list(i)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.rename(columns={0: 'Emoji', 1: 'Count'}, inplace=True)
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    month_timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()
    time = []
    for i in range(month_timeline.shape[0]):
        print(month_timeline["month"][i] + "-" + str(month_timeline["year"][i]))
        time.append(month_timeline["month"][i] + "-" + str(month_timeline["year"][i]))
    month_timeline["time"] = time
    return month_timeline

def day_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby(["date_only"]).count()["message"].reset_index()
    return daily_timeline

def week_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df["day_name"].value_counts()

def month_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df["month"].value_counts()