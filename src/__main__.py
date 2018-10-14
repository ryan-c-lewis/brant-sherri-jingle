from audio_offset_finder import audio_offset_finder


def get_offset_seconds(filepath):
    print("Processing file: " + filepath)
    offset, score = audio_offset_finder.find_offset(
        filepath,
        "dep/master-jingle-opening.mp3",
        correl_nframes=50)
    print("RESULT: " + str(offset) + " seconds (confidence=" + str(score) + ")")
    return offset


if __name__ == '__main__':
    offset = get_offset_seconds("dep/09_27_18_podcast2.mp3")
