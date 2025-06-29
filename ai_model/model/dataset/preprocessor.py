import json
import os
import shutil
import time

import requests
from bs4 import BeautifulSoup

add_lyrics = False
lyrics_provider = "google"  # google or musixmatch

hooktheory_folder = "hooktheory"
output_folder = "processed"
log_file = "log.txt"
alphabet_paths = [f.path for f in os.scandir(hooktheory_folder) if f.is_dir()]
headers = {
    'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "referer": "https://www.google.com/"
}

def log(text):
    print(text)
    with open(log_file, 'a') as log:
        log.write(f"{text}\n")


def process_song(artist, song, path):
    # files = [f"{path}/{f}" for f in os.listdir(path) if "roman" in f]
    # file = f"{path}/chorus_roman.json"
    # # no chorus_roman.json? Take the largest roman file
    # if not Path(file).is_file():
    #     sorted_files = sorted(files, key=os.path.getsize, reverse=True)
    #     file = sorted_files[0]

    artist_name = artist.replace("-", " ").title()
    song_name = song.replace("-", " ").title()

    if add_lyrics:
        if lyrics_provider == "google":
            lyrics = retrieve_lyrics_google(artist_name, song_name)
        else:
            lyrics = retrieve_lyrics_musixmatch(artist_name, song_name)
        time.sleep(1)

        if lyrics is None:
            return

    for f in os.listdir(path):
        if "roman" not in f:
            continue
        file = f"{path}/{f}"
        with open(file) as json_file:
            json_data = json.load(json_file)

            # skip if no melodies
            if len(json_data["tracks"]["melody"]) == 0 or all(
                    [note["isRest"] for note in json_data["tracks"]["melody"]]):
                continue

            # skip of no chords
            if len(json_data["tracks"]["chord"]) == 0 or all(
                    [chord["isRest"] for chord in json_data["tracks"]["chord"]]):
                continue

            if add_lyrics:
                json_data["lyrics"] = lyrics

            output_name = f"{artist_name} - {song_name} - {f.replace('_roman.json', '')}.json"
            with open(f"{output_folder}/{output_name}", 'w') as outfile:
                json.dump(json_data, outfile)


def retrieve_lyrics_google(artist, song):
    search_query = f"{artist} - {song} lyrics"
    url = f"https://www.google.com/search?q={search_query}"
    print(f"Scraping {url}")

    while True:
        soup = BeautifulSoup(requests.get(url, headers=headers).text, features="html.parser")
        captcha_message = soup.select(".g-recaptcha")
        if len(captcha_message) > 0:
            print("BLOCKED, sleeping...")
            time.sleep(60)
        else:
            break

    lyrics_elements = soup.select("div[data-lyricid]")
    if len(lyrics_elements) == 0:
        log(f"{artist} - {song}: no lyrics found")
        return None

    lyrics = lyrics_elements[0].get_text(separator=u"\n")
    return lyrics


def retrieve_lyrics_musixmatch(artist, song):
    search_query = f"{artist} - {song}"
    url = f"https://www.musixmatch.com/search/{search_query}"

    print(f"Scraping {url}")
    while True:
        soup = BeautifulSoup(requests.get(url, headers=headers).text, features="html.parser")
        captcha_message = soup.select(".mxm-human-verify")
        if len(captcha_message) > 0:
            print("BLOCKED, sleeping...")
            time.sleep(60)
        else:
            break

    lyrics_links = soup.select("a[href^='/lyrics/']")

    if len(lyrics_links) == 0:
        log(f"{artist} - {song}: no lyrics found")
        return None

    url = f"https://www.musixmatch.com{lyrics_links[0]['href']}"
    print(f"Scraping {url}")
    soup = BeautifulSoup(requests.get(url, headers=headers).text, features="html.parser")

    lyrics_elements = soup.select(".mxm-lyrics")

    if len(lyrics_elements) == 0:
        log(f"{artist} - {song}: no lyrics found")
        return None

    lyrics = lyrics_elements[0].get_text()
    return lyrics


def process_hooktheory():
    for letter in [f.name for f in os.scandir(hooktheory_folder) if f.is_dir()]:
        letter_path = f"{hooktheory_folder}/{letter}"
        for artist in [f.name for f in os.scandir(letter_path) if f.is_dir()]:
            artist_path = f"{letter_path}/{artist}"
            for song in [f.name for f in os.scandir(artist_path) if f.is_dir()]:
                path = f"{artist_path}/{song}"
                process_song(artist, song, path)


if __name__ == '__main__':
    if os.path.isfile(log_file):
        os.remove(log_file)
    if os.path.isdir(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)
    process_hooktheory()

