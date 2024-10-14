# Audio Cutter with Pygame

## Features

- Audio waveform visualization
- Audio playback control (play, pause, rewind, forward)
- Setting markers at specific points in the audio
- Cutting audio based on set markers
- Adjustable output file naming

## Requirements

- Python 3.x
- Pygame
- pydub
- NumPy
- SciPy


## Usage

1. Place your audio file in the same directory as the script.
2. Open the script and modify the `audio_file` variable in the `__main__` section to match your audio file name:

```python
audio_file = "your_audio_file.wav"  # Replace with your audio file name
```

3. If you want to change the prefix for the output files, modify the `OUTPUT_PREFIX` constant at the top of the file:

```python
OUTPUT_PREFIX = "your_preferred_prefix"  # Change this to your desired prefix
```

4. Run the script:

```
python audio_cutter.py
```

5. Use the following controls in the application:
   - Space: Play/Pause audio
   - Left Arrow: Rewind 5 seconds
   - Right Arrow: Forward 5 seconds
   - M: Add a marker at the current position
   - X: Remove the last added marker
   - C: Cut the audio based on the current markers

6. The cut audio segments will be saved in the same directory as the script, with names following the pattern: `{OUTPUT_PREFIX}_{number}.wav`

## Note

This application currently supports WAV files. For other audio formats, you may need to modify the `load_audio` function and ensure you have the necessary codecs installed.
