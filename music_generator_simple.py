import numpy as np
from music21 import stream, note, chord
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import LSTM, Dropout, Dense, Activation 
from tensorflow.keras.utils import to_categorical 


notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5',
         '60.64.67', '62.65.69', '64.67.71']


sequence_length = 4
note_to_int = dict((note, number) for number, note in enumerate(sorted(set(notes))))
int_to_note = dict((number, note) for note, number in note_to_int.items())
n_vocab = len(note_to_int)

network_input = []
network_output = []

for i in range(len(notes) - sequence_length):
    seq_in = notes[i:i + sequence_length]
    seq_out = notes[i + sequence_length]
    network_input.append([note_to_int[n] for n in seq_in])
    network_output.append(note_to_int[seq_out])

n_patterns = len(network_input)
network_input = np.reshape(network_input, (n_patterns, sequence_length, 1)) / float(n_vocab)
network_output = to_categorical(network_output)

model = Sequential()
model.add(LSTM(128, input_shape=(sequence_length, 1)))
model.add(Dropout(0.2))
model.add(Dense(n_vocab, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.fit(network_input, network_output, epochs=200, batch_size=8, verbose=0)


pattern = network_input[0]
pattern = np.reshape(pattern, (1, pattern.shape[0], 1))  

prediction_output = []

for i in range(30): 
    prediction = model.predict(pattern, verbose=0)
    index = np.argmax(prediction)
    result = int_to_note[index]
    prediction_output.append(result)

   
    next_value = np.array([[[index / float(n_vocab)]]], dtype=np.float32)
    
    
    pattern = np.concatenate((pattern, next_value), axis=1)
    pattern = pattern[:, 1:, :]



output_notes = []

for pattern in prediction_output:
    if '.' in pattern or pattern.isdigit():
        notes_in_chord = pattern.split('.')
        chord_notes = [note.Note(int(n)) for n in notes_in_chord]
        new_chord = chord.Chord(chord_notes)
        new_chord.duration.quarterLength = 0.5
        output_notes.append(new_chord)
    else:
        new_note = note.Note(pattern)
        new_note.duration.quarterLength = 0.5
        output_notes.append(new_note)

midi_stream = stream.Stream(output_notes)
midi_stream.write('midi', fp='simple_generated_music.mid')

print("✅ Music generated and saved as 'simple_generated_music.mid'")
