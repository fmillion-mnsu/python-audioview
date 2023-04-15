import argparse
import os.path
import tempfile
import wave

import matplotlib.pyplot as plt
import numpy as np
import pydub

KNOWN_TYPES = ['.mp3','.wav','.flac','.m4a','.ogg']

def main():

    # get command line argument(s)
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--output",metavar="PNG_FILE",help="Save visualization to this output file instead of displaying")
    parser.add_argument("-x",metavar="MATPLOTLIB_SIZE",type=int,default=24,help="Width (x) of the plot")
    parser.add_argument("-y",metavar="MATPLOTLIB_SIZE",type=int,default=12,help="Height (y) of the plot")
    parser.add_argument("FILE",nargs=1,help="File to visualize")
    args = parser.parse_args()

    # get full absolute path to given file
    this_file = os.path.abspath(args.FILE[0])

    # test if file type is known
    if os.path.splitext(this_file)[1].lower() not in KNOWN_TYPES:
        parser.error(f"unknown file type {os.path.splitext(this_file)[1]}")

    # test if file exists
    if not os.path.isfile(this_file):
        parser.error(f"file '{this_file}' does not exist.")

    # extract file type from filename
    ftype = os.path.splitext(this_file)[1][1:].lower()

    # if the file type is not .wav, convert to wav using pydub
    if ftype != "wav":

        # open file
        audio_seg = pydub.AudioSegment.from_file(os.path.abspath(this_file),ftype)

        # convert file to .wav format and store in a temp file
        temp_wav_file = tempfile.mkstemp(suffix=".wav")

        # since mkstemp actually opens the file, but we can't use the open handle with pydub,
        # close the file and use the path instead
        os.close(temp_wav_file[0]) # tuple item 0 is the handle
        temp_wav_file = temp_wav_file[1] # tuple item 1 is the absolute path

        # write the audio data to the wav file
        # force output to be 16-bit little-endian format
        audio_seg.export(temp_wav_file,format="wav",parameters=["-f","pcm_s16le"])

        # update this_file to point to the tempfile
        this_file = temp_wav_file
    
    # finished with conversion, proceed to plotting.

    # open wav file
    wav_handle = wave.open(this_file, "r")

    # extract the raw audio samples from the .wav file
    # first, read the samples as a binary string, then use numpy to convert to array of int16 values (16-bit samples)
    signal = wav_handle.readframes(-1)
    signal = np.frombuffer(signal, dtype=np.int16)

    print("Generating plot...")

    # plot the samples using matplotlib
    plt.figure(1,figsize=(args.x,args.y))
    plt.title("Audio Signal Waveform")
    plt.plot(signal)

    if args.output:
        plt.savefig(args.output)
        print("Plot saved to "+args.output)
    else:
        plt.show()

    wav_handle.close()
    
    # if not .wav, a tempfile was used; remove the tempfile
    if ftype != "wav":
        os.unlink(this_file)

if __name__ == "__main__":
    main()
