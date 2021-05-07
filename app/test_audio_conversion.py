from .audio import AudioProcessing as ap

audio_path = "audio_input.wav"
result_filename = 'audio_result.wav'

base64_string = ap.audio_to_str_bytes(audio_path) #wav audio to base64str
ap.str_bytes_to_audio(base64_string, result_filename) #base64str to wav audio

#Write bytes in a file for experiments
with open("audio_bytes.txt", "w") as file:
    file.write(base64_string)

with open("audio_bytes.txt", "r") as file:
    data = file.read()