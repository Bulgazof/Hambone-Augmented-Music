import rtmidi
import keyboard
import threading
# import msvcrt
from playsound import playsound
import time

# midiout = rtmidi.MidiOut()

# available_ports = midiout.get_ports()  # will give the port of 'Microsoft GS Wavetable Synth 0'
# print(available_ports)

# if available_ports:
#     midiout.open_port(1)
# else:
#     midiout.open_virtual_port("My virtual output")


velocity = 100
drum = 0
note_on = [0x90, drum, velocity]
note_off = [0x80, drum, velocity]

while True:
    drum_version = input("Select a local_drum kit:\n1) Regular\n2) Bongos\n3) Erik\nSelect a number:")
    if drum_version == '1' or drum_version == '2' or drum_version == '3':
        break


def play_sound_async(file_path):
    threading.Thread(target=playsound, args=(file_path,), daemon=True).start()
    
    
def sound_controller(prediction):
    local_drum = 0
    # Tom 1
    if drum_version == '1':
        if prediction == '1':  # check what data type is being sent\
            play_sound_async('1. mid-tom.wav')

        # Tom 2
        elif prediction == '2':
            play_sound_async('2. floor-tom.wav')

        # Crash
        elif prediction == '3':
            play_sound_async('3. Crash.wav')

        # High hat
        elif prediction == '4':
            play_sound_async('4. HiHat.wav')

    elif drum_version == '2':
        if prediction == '1':  # check what data type is being sent
            play_sound_async('5. low-bongo.wav')

        # Tom 2
        elif prediction == '2':
            play_sound_async('6. split bongo.wav')

        # Crash
        elif prediction == '3':
            play_sound_async('7. kalimba.wav')

        # High hat
        elif prediction == '4':
            play_sound_async('8. Marimba.wav')

    elif drum_version == '3':
        if prediction == '1':  # check what data type is being sent
            play_sound_async('9. HandPan1.wav')

        # Tom 2
        elif prediction == '2':
            play_sound_async('10. HandPan 2.wav')

        # Crash
        elif prediction == '3':
            play_sound_async('11. HandPan 3.wav')

        # High hat
        elif prediction == '4':
            play_sound_async('12. HandPan 4.wav')

    # note_on[1] = local_drum  # Update the drum value in the note_on list
    # note_off[1] = local_drum

    return local_drum

while True:
    drumdrum = input("Drum: ")
    print(drumdrum)
    if drumdrum == '1' or drumdrum == '2' or drumdrum == '3' or drumdrum == '4':
        sound_controller(drumdrum)

    elif drumdrum == 'q':
        break

    else:
        print("Invalid input")



#     del midiout

# with midiout:
#     midiout.send_message(note_on)
#     time.sleep(0.5)  # Wait for half a second
#     midiout.send_message(note_off)
#     print("Sent!")
#
#
