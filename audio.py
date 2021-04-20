import base64

class AudioProcessing:    
    @staticmethod
    def audio_to_str_bytes(file_path) -> str:
        byte_content = open(file_path, "rb").read()
        base64_bytes = base64.b64encode(byte_content)
        base64_string = base64_bytes.decode("utf-8")
        return base64_string
  
    @staticmethod
    def str_bytes_to_audio(base64_string, result_filename):
        base64_bytes = base64_string.encode("utf-8")        
        with open(result_filename, 'wb') as wav_file:
            byte_content = base64.decodebytes(base64_bytes)
            wav_file.write(byte_content)