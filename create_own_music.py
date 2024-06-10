from pretty_midi import PrettyMIDI, Instrument, Note
from play_audio_from_midi_object import play_midi_with_pygame
from play_audio_from_midi_object import play_midi_with_mido
import numpy as np
from pre_processing_tools import is_first_note_aligned
from pre_processing_tools import align_all_notes_to_origin
from pre_processing_tools import make_all_notes_same_duartion
from pre_processing_tools import change_tempo
from pre_processing_tools import filter_to_kick_drum
from pre_processing_tools import make_all_notes_same_volume
from pre_processing_tools import are_tempo_changes_correct


def print_info(midi_data: PrettyMIDI) -> None:
    print("INFO:\n-----")
    print(*midi_data.instruments[0].notes, sep="\n")
    # print(midi_data.instruments[0].notes[0].get_duration())
    print(midi_data.get_beats())
    print()


def create_simple_beat(bpm: int = 120) -> PrettyMIDI:
    # SETUP: Init midi file and create simple beat
    # 120 bpm = 2 bps
    output_midi = PrettyMIDI()
    output_midi.tempo = 120
    drums = Instrument(program=36, is_drum=False)
    output_midi.instruments.append(drums)
    # pitch_sequence = [36, 42, 38, 42]
    drums_notes = [
        Note(velocity=127, pitch=36, start=0, end=0.5),
        Note(velocity=127, pitch=42, start=0.5, end=1),
        Note(velocity=127, pitch=38, start=1, end=1.5),
        Note(velocity=127, pitch=42, start=1.5, end=2),
        # Note(velocity=127, pitch=42, start=2, end=2.5),
        ]
    # drums_notes = [Note(velocity=127, pitch=p, start=t, end=t+10) for t, p in zip([j*10+10 for j in range(4)], pitch_sequence)]
    drums.notes.extend(drums_notes)
    # return change_tempo(output_midi, bpm, 120)
    return output_midi


output_midi = create_simple_beat(bpm=120)


# CHECK: Play the audio
# play_midi_with_mido(output_midi)

# CHECK: Print instruments and notes
print_info(output_midi)


# PREPROCESS: Align all notes
if not is_first_note_aligned(output_midi):
    print("First note is not aligned, shifting everything.")
    output_midi = align_all_notes_to_origin(output_midi)

    # CHECK: Play the audio
    # play_midi_with_mido(output_midi)

    # CHECK: Print instruments and notes
    # print_info(output_midi)
else:
    print("First note is aligned!")


# PREPROCESS: Fix common duration of all notes
output_midi = make_all_notes_same_duartion(output_midi)

# CHECK: Play the audio
# play_midi_with_mido(output_midi)

# CHECK: Print instruments and notes
print_info(output_midi)

# from pathlib import Path
# path = Path.cwd() / "testing_midi_file.mid"
# print(str(path))
# output_midi.write(str(path))

piano_roll = output_midi.get_piano_roll(32)
print(piano_roll.shape)
print(np.count_nonzero(piano_roll))
# print(output_midi.get_beats())
# print(output_midi.get_end_time())
# print(output_midi.get_tempo_changes())
# print(output_midi.estimate_beat_start())
# print(output_midi.estimate_tempo())
# print(output_midi.estimate_tempi())
print(piano_roll[36, :])
print(piano_roll[38, :])
print(piano_roll[42, :])

# print(output_midi.instruments[0].notes)
# print(output_midi.get_chroma())

# exit()
# CHECK: Play the audio
# play_midi_with_mido(output_midi)

# CHECK: Print instruments and notes
# print_info(output_midi)

# from midi2audio import FluidSynth
# print("Path is file?: ", path.is_file())
# # FluidSynth().play_midi(path)

# fs = FluidSynth()
# fs.midi_to_audio(str(path), str(Path.cwd() / "testing_midi_file.wav"))
exit()
print("\n\nTESTIN HERE\n\n")
test_midi_file_path = "C:\\Users\\mrmar\\Downloads\\Neural Networks\\Project\\NN_Drummer_Beat_Project\\data\\drummer8\\session2\\32_rock_117_beat_4-4.mid"
test = PrettyMIDI(test_midi_file_path)
# play_midi_with_mido(test, 5)
test = filter_to_kick_drum(test)
test = make_all_notes_same_volume(test)
test = change_tempo(test, 120, 117)
print(test.instruments[0].notes[0].start)
test = align_all_notes_to_origin(test) if not is_first_note_aligned(test) else test
print(test.instruments[0].notes[0].start)
test = make_all_notes_same_duartion(test)
# play_midi_with_mido(test, 5)
print(test.instruments)
test.instruments[0].is_drum = False
test_piano_roll = test.get_piano_roll()
print(np.count_nonzero(test_piano_roll))

# print_info(test)
# print(test.get_tempo_changes())
print(are_tempo_changes_correct(test))


# One beat is half a second
# Split beat into smaller chunks (mutlplies of 2) like 8
