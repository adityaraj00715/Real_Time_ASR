import pyaudio
import torch
import numpy as np
import multiprocessing
from collections import deque
from multiprocessing import Queue, Event
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

class RealTimeASR:
    """
    RealTimeASR is a class for performing real-time Automatic Speech Recognition (ASR) using Wav2Vec2 model.

    Attributes:
        CHUNK (int): Number of audio samples per chunk, representing 3 seconds at a 16kHz sample rate.
        FORMAT (int): Audio format, set to 16-bit integer.
        CHANNELS (int): Number of audio channels, set to 1 (mono).
        RATE (int): Audio sample rate, set to 16kHz.
    """
    def __init__(self):

        # PyAudio configuration for audio input
        self.CHUNK = int(16000 * 3)
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

    def filter_redundant_transcription(self, previous_transcription, current_transcription, window_size=3):
        """
        Removes redundant parts of the transcription by comparing the current transcription to the previous one.

        Args:
            previous_transcription (str): The transcription from the previous iteration.
            current_transcription (str): The current transcription generated by the model.
            window_size (int): Number of words to compare for overlapping (default is 3).

        Returns:
            str: The filtered current transcription without overlap.
        """
        previous_words = previous_transcription.split()
        current_words = current_transcription.split()
        max_overlap = 0

        # Identify overlapping words between previous and current transcription
        for i in range(len(previous_words) - window_size + 1):
            window = previous_words[i:i + window_size]
            for j in range(len(current_words) - window_size + 1):
                if current_words[j:j + window_size] == window:
                    max_overlap = max(max_overlap, j + window_size)

        # Return non-overlapping part of the transcription
        return " ".join(current_words[max_overlap:])

    def capture_audio(self, audio_queue, stop_flag):
        """
        Captures live audio using PyAudio and puts audio chunks into a queue for processing.

        Args:
            audio_queue (Queue): The queue for storing audio data to be processed.
            stop_flag (Event): Event to stop the audio capture process.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        print("Recording...")

        while not stop_flag.is_set():
            data = stream.read(self.CHUNK)
            audio_numpy = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            try:
                audio_queue.put(audio_numpy, timeout=1)
            except:
                pass

        # Stop and close the audio stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Stopped recording.")

    def process_audio(self, audio_queue, stop_flag):
        """
        Processes audio data from the queue, performs ASR, and prints transcriptions in real-time. The process audio contains
        models and its do all the necessary steps like defining device and processor require to run the model .


        Args:
            audio_queue (Queue): The queue containing audio data to process.
            stop_flag (Event): Event to stop the audio processing loop.
        """

        model_id = "jonatasgrosman/wav2vec2-large-xlsr-53-english"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize the processor and model, and load to device
        processor = Wav2Vec2Processor.from_pretrained(model_id)
        model = Wav2Vec2ForCTC.from_pretrained(model_id).to(device)
        model.eval()


        audio_buffer = deque(maxlen=2)
        previous_transcription = ""

        while not stop_flag.is_set():
            try:
                audio_numpy = audio_queue.get(timeout=1)
                if audio_numpy is not None:
                    audio_buffer.append(audio_numpy)
                    combined_audio = np.concatenate(list(audio_buffer))

                    # Normalize the combined audio
                    max_abs_value = np.max(np.abs(combined_audio))
                    if max_abs_value > 0:
                        combined_audio = combined_audio / max_abs_value

                    # Prepare audio input features for the model
                    input_features = processor(combined_audio, sampling_rate=self.RATE, return_tensors="pt", padding=True).input_values
                    input_features = input_features.to(device)

                    # Generate ASR prediction using the model
                    with torch.no_grad():
                        logits = model(input_features).logits
                    predicted_ids = torch.argmax(logits, dim=-1)

                    # Decode the predicted transcription
                    current_transcription = processor.batch_decode(predicted_ids)[0]

                    # Filter redundant words based on previous transcription
                    filtered_transcription = self.filter_redundant_transcription(previous_transcription, current_transcription)
                    print(f"{filtered_transcription}", end=" ", flush=True)

                    # Update previous transcription
                    previous_transcription = current_transcription

            except:
                continue

    def start(self):
        """
        Starts the ASR process by initiating audio capture and processing as separate processes.
        """
        audio_queue = Queue(maxsize=2)
        stop_flag = Event()

        # Initialize and start audio capture and processing processes
        capture_process = multiprocessing.Process(target=self.capture_audio, args=(audio_queue, stop_flag))
        process_process = multiprocessing.Process(target=self.process_audio, args=(audio_queue, stop_flag))

        capture_process.start()
        process_process.start()

        try:
            capture_process.join()
            process_process.join()
        except KeyboardInterrupt:
            stop_flag.set()
            print("Processes have been stopped.")