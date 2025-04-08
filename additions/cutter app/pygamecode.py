import pygame
from pygame.locals import *
from pydub import AudioSegment
import numpy as np

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Audio Cutter with Pygame')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Константы
# OUTPUT_PREFIX = "L33_现在几点了"  # Префикс для названий выходных файлов

# Global variables
audio = None
data = None
markers = []  # List to store markers in seconds
current_time = 0  # Current play time in milliseconds
is_playing = False  # Control the state of playing
playback_speed = 1  # Playback speed (1x for normal speed)
paused_time = 0  # Track the paused time to resume correctly


def load_audio(file_name):
    global audio, data
    audio = AudioSegment.from_file(file_name)
    pygame.mixer.music.load(file_name)

    # Get raw audio data for waveform plotting
    data = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        data = data.reshape((-1, 2))
        data = data.mean(axis=1)  # Convert to mono if stereo


def plot_waveform():
    screen.fill(WHITE)

    if data is not None:
        # Normalize data for display
        waveform = data / np.max(np.abs(data))
        for x in range(WIDTH):
            idx = int(len(waveform) * (x / WIDTH))
            y = int((1 - waveform[idx]) * HEIGHT / 2)
            pygame.draw.line(screen, BLACK, (x, HEIGHT // 2), (x, y), 1)

    # Draw markers in red
    for marker in markers:
        marker_x = int((marker / (len(data) / audio.frame_rate)) * WIDTH)
        pygame.draw.line(screen, RED, (marker_x, 0), (marker_x, HEIGHT), 2)

    # Draw current play position in blue
    play_x = int((current_time / 1000 / (len(data) / audio.frame_rate)) * WIDTH)
    pygame.draw.line(screen, BLUE, (play_x, 0), (play_x, HEIGHT), 2)

    pygame.display.flip()


def cut_audio():
    if audio and markers:
        markers.sort()
        start = 0
        segments = []
        for marker in markers:
            end = int(marker * 1000)
            segment = audio[start:end]
            segment = trim_to_loudness(segment)
            segments.append(segment)
            start = end

        # Last segment
        segment = audio[start:]
        segment = trim_to_loudness(segment)
        segments.append(segment)

        # Save segments
        for i, segment in enumerate(segments):
            segment.export(f'{OUTPUT_PREFIX}_{i}.mp3', format='mp3')
        print(f"Audio cut and saved with prefix '{OUTPUT_PREFIX}'.")


def trim_to_loudness(segment):
    threshold = -20  # dB
    buffer_ms = 100  # extra milliseconds to include before loud part
    for ms in range(0, len(segment)):
        if segment[ms].dBFS > threshold:
            return segment[max(0, ms - buffer_ms):]
    return segment


def play_audio():
    global is_playing, paused_time
    is_playing = True
    pygame.mixer.music.play(start=paused_time / 1000)  # Start from paused position


def pause_audio():
    global is_playing, paused_time
    is_playing = False
    paused_time = pygame.mixer.music.get_pos()  # Save current position in milliseconds
    pygame.mixer.music.pause()


def rewind_audio(ms):
    global current_time, paused_time
    current_time = max(0, current_time - ms)
    paused_time = current_time  # Update paused position
    pygame.mixer.music.rewind()
    pygame.mixer.music.set_pos(current_time / 1000)


def forward_audio(ms):
    global current_time, paused_time
    current_time = min(len(data) / audio.frame_rate * 1000, current_time + ms)
    paused_time = current_time  # Update paused position
    pygame.mixer.music.set_pos(current_time / 1000)


def add_marker():
    marker_time = current_time / 1000  # Convert to seconds
    markers.append(marker_time)
    print(f"Marker set at {marker_time:.2f} seconds")


def remove_last_marker():
    if markers:
        removed_marker = markers.pop()
        print(f"Removed last marker at {removed_marker:.2f} seconds")
    else:
        print("No markers to remove")


def main():
    global current_time, is_playing
    running = True
    clock = pygame.time.Clock()

    while running:
        plot_waveform()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_SPACE:  # Space to toggle play/pause
                    if is_playing:
                        pause_audio()
                    else:
                        play_audio()

                if event.key == K_LEFT:  # Left arrow for rewind
                    rewind_audio(5000)  # Rewind 5 seconds

                if event.key == K_RIGHT:  # Right arrow for forward
                    forward_audio(5000)  # Forward 5 seconds

                if event.key == K_m:  # 'M' to add marker
                    add_marker()

                if event.key == K_x:  # 'X' to remove last marker
                    remove_last_marker()

                if event.key == K_c:  # 'C' to cut audio
                    cut_audio()

        # Update current play time
        if is_playing:
            current_time += clock.get_time() * playback_speed
            if not pygame.mixer.music.get_busy():  # Stop when playback finishes
                is_playing = False

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    # Load audio file
    # markers = [13.21, 30.04, 42.66]
    # time = 4*60+18
    # markers = [time]

    OUTPUT_PREFIX = "L37_"+"Text"+""
    audio_file = "L37_1_Text.mp3"
    load_audio(audio_file)

    main()
