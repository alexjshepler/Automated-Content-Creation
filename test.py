import piper

# Initialize the TTS engine
engine = piper.TTS()

# Define the text to speak
text = "Hello, this is a test."

# Generate speech and save it to a file
engine.synthesize_to_file(text, "output.wav")

print("Speech saved to output.wav")
