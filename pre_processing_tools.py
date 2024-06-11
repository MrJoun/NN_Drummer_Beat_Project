from pretty_midi import PrettyMIDI
from pretty_midi import Instrument
from pretty_midi import Note
import numpy as np


BATCH_DURATION = 2  # seconds
SLICES_PER_BEAT = 16
DESIRED_BPM = 120
VERBAL = False


def is_first_note_aligned(midi_data: PrettyMIDI) -> bool:
    if len(midi_data.instruments) > 1 or len(midi_data.instruments) == 0:
        raise Exception("Midi object contains more than 1 instrument or no tracks.")
    if len(midi_data.instruments[0].notes) < 1:
        raise Exception("Midi object contains track with no notes.")
    first_note = midi_data.instruments[0].notes[0]
    return first_note.start == 0


def make_instrument_drum(midi_data: PrettyMIDI) -> PrettyMIDI:
    midi_data.instruments[0].is_drum = True
    return midi_data


def make_instrument_not_drum(midi_data: PrettyMIDI) -> PrettyMIDI:
    midi_data.instruments[0].is_drum = False
    return midi_data


def align_all_notes_to_origin(midi_data: PrettyMIDI) -> PrettyMIDI:
    if VERBAL: print("-> Aligning notes...", end="")
    time_shift = midi_data.instruments[0].notes[0].start
    for note in midi_data.instruments[0].notes:
        note.start -= time_shift
        note.end -= time_shift
    if VERBAL: print(" DONE")
    return midi_data


def make_all_notes_same_duartion(midi_data: PrettyMIDI, duration: int = None) -> PrettyMIDI:
    if VERBAL: print("-> Making all notes same duration...", end="")
    if duration is None:
        duration = 1 / SLICES_PER_BEAT
    for note in midi_data.instruments[0].notes:
        note.end = note.start + duration
    if VERBAL: print(" DONE")
    return midi_data


def make_all_notes_same_volume(midi_data: PrettyMIDI, vol: int = 127) -> PrettyMIDI:
    if VERBAL: print("-> Making all notes same volume...", end="")
    for note in midi_data.instruments[0].notes:
        note.velocity = vol
    if VERBAL: print(" DONE")
    return midi_data


def are_tempo_changes_correct(midi_data: PrettyMIDI) -> bool:
    return DESIRED_BPM in midi_data.get_tempo_changes()


def change_tempo(midi_data: PrettyMIDI, target_bpm: int, original_bpm: int) -> PrettyMIDI:
    if VERBAL: print("-> Changing the tempo...", end="")
    # Calculate the ratio of the new BPM to the original BPM
    tempo_ratio = target_bpm / original_bpm
    # Create a new PrettyMIDI object to store the adjusted MIDI
    new_midi_data = PrettyMIDI()
    # Copy the original instruments
    for instrument in midi_data.instruments:
        new_midi_data.instruments.append(instrument)
    for instrument in new_midi_data.instruments:
        for note in instrument.notes:
            note.start *= (1 / tempo_ratio)
            note.end *= (1 / tempo_ratio)
        for cc in instrument.control_changes:
            cc.time *= (1 / tempo_ratio)
    if VERBAL: print(" DONE")
    return new_midi_data


def filter_to_kick_drum(midi_data: PrettyMIDI) -> PrettyMIDI:
    if VERBAL: print("-> Filtering everything but kick...", end="")
    # MIDI note numbers for kick drums
    kick_drum_notes = [35, 36]
    # Create a new PrettyMIDI object to store the filtered MIDI
    new_midi_data = PrettyMIDI()
    # Iterate over instruments and keep only drum instruments
    for instrument in midi_data.instruments:
        if instrument.is_drum:
            # Filter notes to keep only kick drum notes
            new_notes = []
            for note in instrument.notes:
                if note.pitch in kick_drum_notes:
                    note.pitch = 36
                    new_notes.append(note)
            instrument.notes = new_notes
        new_midi_data.instruments.append(instrument)
    if VERBAL: print(" DONE")
    return new_midi_data


def midi_to_bit_vector(midi_data: PrettyMIDI) -> np.ndarray:
    if VERBAL: print("-> Converting MIDI to bit vector...", end="")
    bit_vector = midi_data.get_piano_roll(SLICES_PER_BEAT)
    if VERBAL: print(" DONE")
    return bit_vector


def slice_midi_to_batches(midi_data: PrettyMIDI, batch_duration: float = BATCH_DURATION) -> list | PrettyMIDI:
    if VERBAL: print("-> Slicing midi to batches...", end="")
    num_of_batches = int(midi_data.instruments[0].notes[-1].end // 2)
    batches = [0] * num_of_batches
    batch_idx = 0
    time = 2
    notes = []
    for i, note in enumerate(midi_data.instruments[0].notes):
        # print(f"Note #{i}/{len(midi_data.instruments[0].notes)}")
        # print(f"Batch idx: {batch_idx}")
        if batch_idx >= num_of_batches:
            break
        if note.end >= time:
            # print(f"\t Batch idx: {batch_idx}")
            # print(f"\t Num of notes: {len(notes)}")
            if len(notes) == 0:
                del batches[batch_idx]
            else:
                batch = PrettyMIDI()
                batch_instrument = Instrument(midi_data.instruments[0].program)
                batch_instrument.notes.extend(notes)
                batch.instruments.append(batch_instrument)
                batches[batch_idx] = batch
                batch_idx += 1
            time += batch_duration
            notes = []
        else:
            notes.append(note)
    batches = [batch for batch in batches if batch != 0]
    if VERBAL: print(" DONE")
    return batches
