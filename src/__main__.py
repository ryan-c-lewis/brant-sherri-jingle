from audio_offset_finder import audio_offset_finder
from pydub import AudioSegment
import ntpath
import os
import random
import re
import requests
import time

JINGLE_MASTER_FILEPATH = "dep/master-jingle-opening.mp3"
JINGLE_LENGTH = 6.5

def find_jingle_and_trim(filepath):
    print("Processing file: " + filepath)
    new_filepath = "out/trimmed/" + ntpath.basename(filepath)[:-4] + "_trimmed.mp3"
    offset, score = audio_offset_finder.find_offset(
        filepath,
        JINGLE_MASTER_FILEPATH,
        correl_nframes=50)
    print("Found jingle at " + str(offset) + " seconds (confidence=" + str(score) + ")")
    if not os.path.exists("out/trimmed/"):
        os.makedirs("out/trimmed/")
    full_podcast = AudioSegment.from_mp3(filepath)
    trimmed_podcast = full_podcast[offset*1000:((offset+JINGLE_LENGTH)*1000)]
    trimmed_podcast.export(new_filepath, format="mp3")
    print("Saved trim file to: " + new_filepath)


def make_web_request(url):
    time.sleep(2 + random.random()*5)  # I don't want to look like a bot
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    print('Making request to ' + url)
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception('Unexpected error code ' + r.status_code + ' when trying to access url ' + url)
    print('Finished request')
    return r.content


def get_podcast_file_names():
    podcast_file_names = []
    for page in [1,2]:
        search_html = make_web_request('https://branthansen.com/page/' + str(page) + '/?s=jingle')
        podcast_page_links = re.findall('<a href="(.*)"><h2 class="blog-article-header">', search_html)
        for podcast_page_link in podcast_page_links:
            podcast_page_html = make_web_request(podcast_page_link)
            podcast_file_name = re.findall('Podcast: <a href="(.*)" class="powerpress_link_pinw"', podcast_page_html)[0]
            print('Podcast file name: ' + podcast_file_name)
            podcast_file_names.append(podcast_file_name)
    return podcast_file_names


def download_podcast_files():
    for podcast_file_name in get_podcast_file_names():
        print('Downloading ' + podcast_file_name)
        short_file_name = podcast_file_name.split('/')[-1]
        if not os.path.exists("out/raw"):
            os.makedirs("out/raw")
        open('out/raw/' + short_file_name, 'wb').write(make_web_request(podcast_file_name))
        print('Finished download')


def trim_raw_podcast_files():
    for file_name in os.listdir('out/raw/'):
        find_jingle_and_trim('out/raw/' + file_name)


def overlay_trimmed_files():
    trimmed_file_names = os.listdir('out/trimmed/')
    combined_sound = AudioSegment.from_mp3('out/trimmed/' + trimmed_file_names[0])
    for file_name in trimmed_file_names[1:]:
        print('Overlaying ' + file_name)
        trimmed_file = AudioSegment.from_mp3('out/trimmed/' + file_name)
        combined_sound = combined_sound.overlay(trimmed_file)
        combined_sound.export('out/high_quality_very_professional_sounding_jingle.mp3', format='mp3')


if __name__ == '__main__':
    download_podcast_files()
    trim_raw_podcast_files()
    overlay_trimmed_files()
