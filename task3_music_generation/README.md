# Task 3 — Music Generation with AI

This implementation uses `music21` to read MIDI files and TensorFlow/Keras LSTM to learn note sequences.

## Dataset

Place `.mid` or `.midi` files in:

```text
data/
```

The repository intentionally does not include a copyrighted music dataset. Use MIDI files that you have permission to use.

## Pipeline

MIDI → notes/chords → integer encoding → fixed-length sequences → LSTM → predicted notes → MIDI output.

## Commands

Install dependencies:

```bash
pip install -r ../requirements.txt
```

Extract the dataset and train:

```bash
python train.py
```

Generate a new MIDI file:

```bash
python generate.py
```

For a small demo, the script also supports a reduced model, but meaningful generation requires enough MIDI training data.
