from audio_offset_finder import audio_offset_finder
from pydub import AudioSegment
import ntpath
import os

JINGLE_MASTER_FILEPATH = "dep/master-jingle-opening.mp3"
JINGLE_LENGTH = 6.5

def find_jingle_and_trim(filepath):
    print("Processing file: " + filepath)
    new_filepath = "out/" + ntpath.basename(filepath)[:-4] + "_trimmed.mp3"
    offset, score = audio_offset_finder.find_offset(
        filepath,
        JINGLE_MASTER_FILEPATH,
        correl_nframes=50)
    print("Found jingle at " + str(offset) + " seconds (confidence=" + str(score) + ")")
    if not os.path.exists("out"):
        os.makedirs("out")
    full_podcast = AudioSegment.from_mp3(filepath)
    trimmed_podcast = full_podcast[offset*1000:((offset+JINGLE_LENGTH)*1000)]
    trimmed_podcast.export(new_filepath, format="mp3")
    print("Saved trim file to: " + new_filepath)


if __name__ == '__main__':
    find_jingle_and_trim("dep/09_27_18_podcast2.mp3")