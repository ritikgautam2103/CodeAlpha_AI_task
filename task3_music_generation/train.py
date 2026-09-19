from pathlib import Path
import pickle
import numpy as np
from music21 import converter, instrument, note, chord, stream
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
MODEL_DIR = BASE / "models"
MODEL_DIR.mkdir(exist_ok=True)

SEQUENCE_LENGTH = 40

def extract_notes():
    notes = []
    midi_files = list(DATA.glob("*.mid")) + list(DATA.glob("*.midi"))
    if not midi_files:
        raise FileNotFoundError(
            f"No MIDI files found in {DATA}. Add MIDI files you are allowed to use."
        )

    for filename in midi_files:
        try:
            midi = converter.parse(filename)
            parts = instrument.partitionByInstrument(midi)
            elements = parts.parts[0].recurse() if parts else midi.flat.notes

            for element in elements:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append(".".join(str(n) for n in element.normalOrder))
        except Exception as exc:
            print(f"Skipping {filename.name}: {exc}")

    if len(notes) <= SEQUENCE_LENGTH:
        raise ValueError(
            f"Only {len(notes)} usable events were extracted. "
            f"Add more MIDI data; at least {SEQUENCE_LENGTH + 1} events are needed."
        )

    return notes

notes = extract_notes()
pitchnames = sorted(set(notes))
note_to_int = {n: i for i, n in enumerate(pitchnames)}

network_input, network_output = [], []
for i in range(len(notes) - SEQUENCE_LENGTH):
    sequence = notes[i:i + SEQUENCE_LENGTH]
    network_input.append([note_to_int[x] for x in sequence])
    network_output.append(note_to_int[notes[i + SEQUENCE_LENGTH]])

n_vocab = len(pitchnames)
X = np.reshape(network_input, (len(network_input), SEQUENCE_LENGTH, 1))
X = X / float(n_vocab)
y = to_categorical(network_output, num_classes=n_vocab)

model = Sequential([
    LSTM(256, input_shape=(SEQUENCE_LENGTH, 1), return_sequences=True),
    Dropout(0.3),
    LSTM(256),
    Dense(128, activation="relu"),
    Dropout(0.3),
    Dense(n_vocab, activation="softmax"),
])
model.compile(loss="categorical_crossentropy", optimizer="adam")

print(f"Training on {len(X)} sequences and {n_vocab} unique events...")
model.fit(X, y, epochs=30, batch_size=64, verbose=1)

model.save(MODEL_DIR / "music_lstm.keras")
with open(MODEL_DIR / "mapping.pkl", "wb") as f:
    pickle.dump({"notes": notes, "pitchnames": pitchnames, "sequence_length": SEQUENCE_LENGTH}, f)

print("Saved model and mapping in models/")
