# real_time_asr

## Overview
**real_time_asr** is a Python-based library for performing real-time Automatic Speech Recognition (ASR) using the Wav2Vec2 model. It captures live audio input, processes it in real-time using a pre-trained Wav2Vec2 model, and prints the transcriptions directly to the console. The library supports both CPU and GPU devices and ensures smooth transcription with minimal latency.

This project can be used for applications such as voice-driven commands, real-time transcription, or interactive audio systems.

## Features
- Real-time audio capture from a microphone.
- ASR using the Wav2Vec2 model.
- Smooth transcription with redundancy filtering.
- Support for both CPU and GPU.

## Dependencies
The project requires the following Python libraries:

- **pyaudio**: For real-time audio input.
- **torch**: For running the Wav2Vec2 model.
- **numpy**: For audio data processing.
- **transformers**: For accessing the Wav2Vec2 model and processor.

Install them using the command:

```bash
pip install -r requirements.txt
```

## How to Run the Project

### 1. Install the Package
To get started, install the **real_time_asr** package using `pip`:

```bash
pip install real_time_asr
```

### 2. Create and Run Your Script
You need to create a Python script to use the library. Here's an example script:

```python
from real_time_asr import RealTimeASR

if __name__ == "__main__":
    # Create an instance of your ASR class
    real_time_asr = RealTimeASR()

    # Start real-time ASR
    real_time_asr.start()

```
Save this script as run_asr.py or any other name with a .py extension.

Run the script using the following command:

```bash
python run_asr.py
```

### 3. Output
Once the script is running:

- The program will start capturing audio from your microphone.
- Real-time transcriptions will appear in the console as the audio is processed.
- To stop the program, press `Ctrl + C`.

### Additional Notes
- Ensure that your microphone is connected and functional before running the script.  
- If you're using a GPU, ensure that PyTorch is configured for CUDA for better performance.  
- The transcription process includes redundancy filtering to avoid repeating words unnecessarily by comparing overlaps in previous transcriptions.  

### Contributing
Contributions are welcome! If you'd like to contribute, feel free to:  
1. Fork the repository.  
2. Make your improvements.  
3. Submit a pull request.  

### Documentation
For more info about code click here [click here](https://adityaraj00715.github.io/Real_Time_ASR/real_time_asr/asr.html)

Pypi package link [here](https://pypi.org/project/real-time-asr/)

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.