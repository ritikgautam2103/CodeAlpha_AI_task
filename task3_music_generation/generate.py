from pathlib import Path
import pickle
import random
import numpy as np
from music21 import note, chord, stream
from tensorflow.keras.models import load_model

BASE = Path(__file__).resolve().parent
MODEL_DIR = BASE / "models"
OUTPUT_DIR = BASE / "generated"
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "music_lstm.keras"
MAPPING_PATH = MODEL_DIR / "mapping.pkl"
OUTPUT_PATH = OUTPUT_DIR / "generated_music.mid"

model = load_model(MODEL_PATH)

with open(MAPPING_PATH, "rb") as f:
    data = pickle.load(f)

notes = data["notes"]
pitchnames = data["pitchnames"]
sequence_length = data["sequence_length"]
note_to_int = {n: i for i, n in enumerate(pitchnames)}

start = random.randint(0, len(notes) - sequence_length - 1)
pattern = [note_to_int[n] for n in notes[start:start + sequence_length]]

prediction_length = 200
output_notes = []

for _ in range(prediction_length):
    x = np.reshape(pattern, (1, sequence_length, 1))
    x = x / float(len(pitchnames))
    prediction = model.predict(x, verbose=0)[0]
    index = int(np.argmax(prediction))
    result = pitchnames[index]
    output_notes.append(result)
    pattern.append(index)
    pattern = pattern[1:]

offset = 0.0
output = []

for pattern_item in output_notes:
    if "." in pattern_item and all(part.isdigit() for part in pattern_item.split(".")):
        chord_notes = [note.Note(int(p)) for p in pattern_item.split(".")]
        new_chord = chord.Chord(chord_notes)
        new_chord.offset = offset
        output.append(new_chord)
    else:
        new_note = note.Note(pattern_item)
        new_note.offset = offset
        output.append(new_note)
    offset += 0.5

midi_stream = stream.Stream(output)
midi_stream.write("midi", fp=OUTPUT_PATH)
print(f"Generated MIDI: {OUTPUT_PATH}")
