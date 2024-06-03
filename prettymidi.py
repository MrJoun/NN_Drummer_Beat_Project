# import jax
# import jax.numpy as np
# import math
import numpy as np
# import tensorflow as tf
import time
#import matplotlib.pyplot as plt
import pygame
from pathlib import Path
import prettymidi

np.int = int

import pretty_midi


data_filename = "info.csv"
data_folder_path = Path().cwd() / "data"
data_path = data_folder_path / data_filename

def change_tempo(midi_file_path, new_bpm):
    # Convert the midi_file_path to a string
    midi_file_path_str = str(midi_file_path)
    midi_data = pretty_midi.PrettyMIDI(midi_file_path_str)

    # Calculate the ratio of the new BPM to the original BPM
    original_bpm = midi_data.estimate_tempo()
    tempo_ratio = new_bpm / original_bpm

    # # Get tempo changes
    # tempo_change_times, tempo = midi_data.get_tempo_changes()

    # # Adjust each tempo-related event
    # new_tempo_change_times = tempo_change_times * (1 / tempo_ratio)

    # Create a new PrettyMIDI object to store the adjusted MIDI
    new_midi_data = pretty_midi.PrettyMIDI()

    # Copy the original instruments
    for instrument in midi_data.instruments:
        new_midi_data.instruments.append(instrument)

    for instrument in new_midi_data.instruments:
        for note in instrument.notes:
            note.start *= (1 / tempo_ratio)
            note.end *= (1 / tempo_ratio)
        for cc in instrument.control_changes:
            cc.time *= (1 / tempo_ratio)

    # Save the modified MIDI data to a new file
    new_file_path = midi_file_path_str.replace('.mid', f'_tempo_{new_bpm}.mid')
    new_midi_data.write(new_file_path)

    print(f"New MIDI file with BPM {new_bpm} saved to: {new_file_path}")
    return new_file_path

def filter_to_kick_drum(midi_file_path):
    # Convert the midi_file_path to a string
    midi_file_path_str = str(midi_file_path)

    # Load the MIDI file
    midi_data = pretty_midi.PrettyMIDI(midi_file_path_str)

    # MIDI note numbers for kick drums
    kick_drum_notes = [35, 36]

    # Create a new PrettyMIDI object to store the filtered MIDI
    new_midi_data = pretty_midi.PrettyMIDI()

    # Iterate over instruments and keep only drum instruments
    for instrument in midi_data.instruments:
        if instrument.is_drum:
            # Filter notes to keep only kick drum notes
            new_notes = [note for note in instrument.notes if note.pitch in kick_drum_notes]
            instrument.notes = new_notes
        new_midi_data.instruments.append(instrument)

    # Save the filtered MIDI data to a new file
    new_file_path = midi_file_path_str.replace('.mid', '_kick_only.mid')
    new_midi_data.write(new_file_path)

    print(f"New MIDI file with only kick drums saved to: {new_file_path}")
    return new_file_path

if __name__ == '__main__':

    with data_path.open() as file:
        columns = file.readline()
            # Attach absolute path to midi & audio files
        midi_data_path = data_folder_path / "drummer1/session1/82_neworleans-funk_84_beat_4-4.mid"
        midi_file = midi_data_path

        new_path = change_tempo(midi_file, 300)
        new_path = filter_to_kick_drum(new_path)

        pygame.mixer.init()
        pygame.init()
        #pygame.mixer.music.load(midi_file)
        pygame.mixer.music.load(new_path)
        pygame.mixer.music.play()

        # Keep the program running until the MIDI file is done playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    del np.int


# with data_path.open() as file:
#     columns = file.readline()


#     for i, line in enumerate(file):
#         # Strip line of new line and split into list
#         line = line.strip().split(",")

#         # Check
#         print(line)

#         # Attach absolute path to midi & audio files
#         midi_data_path = data_folder_path / line[7]
#         midi_file = midi_data_path

#         pygame.mixer.init()
#         pygame.init()
#         pygame.mixer.music.load(midi_file)
#         pygame.mixer.music.play()

#         # Keep the program running until the MIDI file is done playing
#         while pygame.mixer.music.get_busy():
#             pygame.time.Clock().tick(10)









