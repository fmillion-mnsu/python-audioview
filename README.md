# Audio Visualizer

This is a very simple project to visualize an audio file using Python tools. It uses `matplotlib` and `numpy` to visualize the audio graph, and uses `pydub` to convert non-`.wav` files to `.wav` format for parsing. The output is similar to what you might see in a digital audio editing package.

## Steps to run

1. Setup a virtual environment. If you use `anaconda` then just do `conda create -n (name_of_environment)`. Otherwise use `virtualenv` in the usual way: `python -m virtualenv venv` followed by the appropriate activate command (`venv/bin/activate` on Linux and Mac, `venv\Scripts\activate.bat` or `venv\Scripts.activate.ps1` on Windows for cmd.exe and PowerShell respectively.)
1. Install packages. `pip install -r requirements.txt`
1. Run the app to plot the demo file: `python app.py demo.wav`
1. It also works with mp3 files: `python app.py demo.mp3`

## Notes

For anything other than a `.wav` file, `pydub` is used to first convert it to a temporary `.wav` file. The temporary file is deleted when the program exits. 

You can write the output of the plot directly to a `.png` file by providing the `-o` command line option. This will write the plot to a file rather than displaying it. For example: `python app.py demo.wav -o output.png`

You can control the size of the output plot by using the `-x` and `-y` command line options. These values are passed directly to `matplotlib`'s `figsize` option. For example: `python app.py demo.wav -o output.png -x 8 -y 4` for a small plot.
