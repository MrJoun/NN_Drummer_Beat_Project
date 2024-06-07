import numpy as np
from pretty_midi import PrettyMIDI


def midi_to_piano_roll(midi_file, timestep=0.1, pitches=(0, 0)):
  """
  Converts a MIDI file to a piano roll representation.

  Args:
      midi_file (str): Path to the MIDI file.
      timestep (float, optional): Duration of a time step in seconds. Defaults to 0.1.
      pitches (tuple, optional): Range of pitches to consider (inclusive). Defaults to (21, 108) (C1 to C8).

  Returns:
      numpy.ndarray: Piano roll representation with shape (time_steps, num_pitches).
  """

  # Load MIDI data
  midi_data = PrettyMIDI(midi_file)

  # Define time steps and number of pitches
  num_timesteps = int(midi_data.get_end_time() / timestep)
  num_pitches = pitches[1] - pitches[0] + 1
  print("number of pitches:", num_pitches)

  # Create empty piano roll
  piano_roll = np.zeros((num_timesteps, num_pitches))

  # Extract note events
  for instrument in midi_data.instruments:
    for note in instrument.notes:
      # Convert note pitch to index (within defined range)
      pitch_idx = note.pitch - pitches[0]
      if 0 <= pitch_idx < num_pitches:
        # Calculate time step indices for note on and off events
        onset_idx = int(note.start / timestep)
        offset_idx = int(note.end / timestep)

        # Set piano roll values for active note during the timestep range
        piano_roll[onset_idx:offset_idx, pitch_idx] = 1

  return piano_roll

# # Example usage
# midi_file = "your_song.midi"
# piano_roll = midi_to_piano_roll(midi_file)

# # You can now use the piano_roll for RNN training (e.g., reshape, normalize)
# print(piano_roll.shape)
