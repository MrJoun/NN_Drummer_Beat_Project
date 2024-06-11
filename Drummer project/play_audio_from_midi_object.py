import pygame
from pathlib import Path
from pretty_midi import PrettyMIDI
import mido
from tqdm import tqdm
from time import sleep


def play_midi_with_pygame(midi_data: PrettyMIDI, duration: float = 5.0) -> None:
    print("PLAYING...\n----------")
    cwd = Path.cwd()
    midi_file_path = cwd / "py_game_temp_midi_file"
    midi_data.write(str(midi_file_path))

    # Initialize Pygame and audio mixer
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(midi_file_path)
    pygame.mixer.music.play()

    # Keep the program running until the MIDI file is done playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    print("FINISHED\n")


def play_midi_with_mido(midi_data: PrettyMIDI, duration: float = 5.0) -> None:
    # return
    print("PLAYING...\n----------")
    cwd = Path.cwd()
    midi_file_path = cwd / "mido_temp_midi_file"
    midi_data.write(str(midi_file_path))
    midi_data = mido.MidiFile(midi_file_path)

    # Create output port for playing samples
    with mido.open_output(autoreset=True) as outport:
        if isinstance(duration, (float, int)):
            for msg in tqdm(midi_data.play(), desc="Playback", ncols=100, mininterval=0.01):
                if duration <= 0: break
                outport.send(msg)
                duration -= msg.time
        else:
            for msg in midi_data.play():
                print(msg)
                outport.send(msg)
    sleep(1)
    if not outport.closed:
        print("Closing port...")
        outport.close()
    print("FINISHED\n")
