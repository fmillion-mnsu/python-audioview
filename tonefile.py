# generate tones in a .WAV file
# original code by Flint Million <flint.million@mnsu.edu> (c) 2012-2014

# See the main() function for demo and info on using.

import math
import os.path
import struct

class ToneFile:

    def __init__(self, outputFile):

        if not os.path.isdir(os.path.dirname(os.path.abspath(outputFile))):
            raise ValueError(f"Destination directory '{os.path.dirname(os.path.abspath(putputFile))}' does not exist.")
        
        # Store output wav path
        self.wavPath = os.path.abspath(outputFile)

        # initialize array to hold values to synthesize
        self._objects = []

    def addTone(self, divisor, length_ms=250):
        """Add a tone to the output file.
        
    The tone file is synthesized at 96000Hz. The divisor is a value indicating
    the number of samples per cycle of the waveform. 
    
    To calculate the frequency in Hz of a divisor, use the formula: 
    
        96000 / (divisor * 2)"""

        self._objects.append( (divisor, int(math.floor(length_ms/1000.0*96000))) )

    def addSilence(self, length_ms=250):
        """Add a period of silence to the output file."""
  
        self._objects.append( (0, int(math.floor(length_ms/1000.0*96000))) )

    def addToneByFrequency(self, freq, length_ms=250):
        """Add a tone to the output file.
        
    This function precalculates the nearest divisor to the requested
    frequency. Note that the frequency will *not* be exact most of the
    time."""
        
        divisor = int(math.floor(48000 / freq))

        self._objects.append( (divisor, int(math.floor(length_ms/1000.0*96000))) )

    def write(self):

        # generate bytestring to hold output data, with
        # initial wav header data prepared

        # generate buffer for output samples
        wav_samples = b''

        lastCycle = 0 # 0 = neutral, 1 = >0, -1 = <0

        for obj in self._objects:

            # obj[0] = divisor or 0 for silence
            # obj[1] = length in samples

            # if silence, add empty samples
            if obj[0] == 0:
                wav_samples += b'\x00\x00'*obj[1]
                lastCycle = 0
                continue

            # Determine number of cycles
            # length_in_samples / (divisor * 2)
            cycleCount = int(obj[1] / obj[0] * 2)

            # add extra cycle - we just truncate it later, saves
            # us from having to add samples to match the length
            # manually.
            cycleCount += 1

            # Generate samples
            samples = b''.join([
                b'\x00\x20' * obj[0] 
                if y % 2 == (1 if lastCycle == 1 else 1)
                else b'\x00\xe0' * obj[0] 
                for y in range(cycleCount*2)
            ])

            # truncate to actual length
            samples = samples[:obj[1]*2]

            # This inverts the waveform if the last waveform ended on a negative cycle.
            # Not doing this would introduce noticeable clicks and frequency harmonics.
            if samples[-1] == 0x20:
                lastCycle = 1
            else:
                lastCycle = -1

            # add generated samples to the buffer
            wav_samples += samples

        # samples finished... 
        # now we can start generating the bytes for the wav file
        
        # total size of file = sample bytes + 44
        total_file_size = struct.pack("<L",len(wav_samples)+44)
        wav_data  = b"RIFF"+total_file_size+b"WAVE" # riff header
        wav_data += b"fmt \x10\x00\x00\x00" # fmt chunk header
        wav_data += b"\x01\x00\x01\x00\x00\x77\x01\x00\x00\xEE\x02\x00\x02\x00\x10\x00" # fmt chunk data
        total_sample_size = struct.pack("<L",len(wav_samples))
        wav_data += b"data"+total_sample_size # actual sample data

        # Write the data to the wav file
        of = open(os.path.abspath(self.wavPath),"wb")
        of.write(wav_data)
        of.write(wav_samples)
        of.close()

def main():
    # Tests the tone file generator

    # Initialize a tone generator with the output file 'tone.wav'.
    t = ToneFile("test.wav")

    # This adds a tone to the output file that is the *closest* cycling frequency we can get to 440Hz.
    # It will actually be more like 440.3Hz.
    # The second parameter is the length in milliseconds.
    t.addToneByFrequency(440,250)
    t.addSilence(250)
    
    # Alternatively we can specify the actual divisor.
    # The sampling frequency of the tone data is 96kHz, and the divisor specifies how many samples
    # are used per cycle of the waveform.
    # To calculate the actual frequency given a divisor, use the formula:
    #    96000 / (divisor * 2)
    # The *higher* the number, the *lower* the tone - this iteration going downward
    # in divisor will result in a tone that goes up in frequency.
    for n in range(512,16,-1):
        t.addTone(n,50)
    
    # You can also add periods of silence, again with the time specified in milliseconds.
    t.addSilence(1000)

    # One more example.
    t.addToneByFrequency(1000,500)

    # After adding the tones, you need to call "write" to actually write the .wav file to disk.
    t.write()

    # Program ends here.

# if tonefile.py is invoked directly, run the test code and generate test.wav in the current directory.
if __name__ == "__main__":
    main()
