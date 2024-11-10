from setuptools import setup, find_packages

setup(
    name="real_time_asr",
    version="0.1.0",
    description="Real-time ASR using Wav2Vec2 model with PyAudio",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aditya Raj",
    author_email="adityaraj0071506@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pyaudio",
        "torch",
        "numpy",
        "transformers",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
