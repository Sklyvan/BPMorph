from numpy import ndarray, dtype
from pydub import AudioSegment
from mutagen.id3 import ID3
from typing import Any

import subprocess
import argparse
import librosa
import os


def copyMetadata(originalFile: str, newFile: str) -> None:
    """
    Copies metadata from the original MP3 file to the new MP3 file.
    :param originalFile: str - Path to the original MP3 file.
    :param newFile: str - Path to the new MP3 file.
    :return: None
    """
    original_tags = ID3(originalFile)
    # Remove existing tags in the new file (if any)
    try:
        new_tags = ID3(newFile)
        new_tags.delete(newFile)
    except Exception:
        pass
    # Save a copy of the original tags to the new file
    original_tags.save(newFile)
    print(f"✅ Metadata copied from {originalFile} to {newFile}")

def detectBPM(filePath: str) -> ndarray[tuple[int, ...], dtype[Any] | Any]:
    """
    Detects the BPM (Beats Per Minute) of an audio file using librosa.
    :param filePath: str - Path to the audio file.
    :return: float - Detected BPM of the audio file.
    """
    y, sr = librosa.load(filePath)
    bpm, _ = librosa.beat.beat_track(y=y, sr=sr)
    return bpm[0]

def convertToWav(inputPath: str, outputPath: str) -> None:
    """
    Converts an audio file to WAV format using pydub.
    :param inputPath: str - Path to the input audio file.
    :param outputPath: str - Path to the output WAV file.
    :return: None
    """
    audio = AudioSegment.from_file(inputPath)
    audio.export(outputPath, format="wav")

def stretchAudioWithRubberband(inputWav: str, outputWav: str, applyFactor: float) -> None:
    """
    Stretches audio using Rubberband with a specified factor.
    :param inputWav: str - Path to the input WAV file.
    :param outputWav: str - Path to the output WAV file.
    :param applyFactor: float - Factor by which to stretch the audio (e.g., 1.0 for no change, 0.5 for half speed).
    :return: None
    """
    subprocess.run([
        "rubberband",
        "-t", str(applyFactor),
        "--pitch", "0",  # No pitch shift
        "--crisp", "5",  # Crispness of the output, this is the best value for electronic music
        inputWav,
        outputWav
    ], check=True)

def changeBPM(inputAudio: str, outputAudio: str, toBPM: float = None, factor: float = None) -> None:
    if not toBPM and not factor:
        raise ValueError("Either 'toBPM' or 'factor' must be provided.")
    if toBPM and factor:
        raise ValueError("Only one of 'toBPM' or 'factor' should be provided.")

    tempInp = "TemporalInp.wav"
    tempOut = "TemporalOut.wav"

    # Convert to WAV
    convertToWav(inputAudio, tempInp)
    print(f"🔄 Converted {inputAudio} to WAV format.")

    if toBPM:
        # Detect original BPM
        originalBPM = detectBPM(tempInp)
        print(f"🎵 Original BPM: {originalBPM:.2f}")

        # Calculate the factor for time-stretching
        factor = originalBPM / toBPM
        print(f"⚙️ Change Factor: {factor:.4f}")

    # Time-stretch con Rubberband
    stretchAudioWithRubberband(tempInp, tempOut, factor)
    print(f"⏳ Stretched Audio {tempOut}")

    # Convert again to MP3 if necessary
    if outputAudio.endswith(".mp3"):
        stretched = AudioSegment.from_wav(tempOut)
        stretched.export(outputAudio, format="mp3")
    else:
        os.rename(tempOut, outputAudio)

    # Remove temporary files
    if os.path.exists(tempInp):
        os.remove(tempInp)
    if os.path.exists(tempOut):
        os.remove(tempOut)

    print(f"✅ Exported to {outputAudio}")


def main(bpm: int, factor: float, inputSong: str) -> None:
    """
    Main function to change the BPM of an audio file.
    :param bpm: int - Target BPM.
    :param factor: float - Factor by which to change the BPM.
    :param inputSong: str - Path to the input audio file.
    :return: None
    """
    print(f"🔍 Loading {inputSong}")
    outputSong = inputSong.replace(".mp3", f"_{bpm}BPM.mp3")

    if factor:
        changeBPM(inputSong, outputSong, factor=factor)
    elif bpm:
        changeBPM(inputSong, outputSong, toBPM=bpm)

    copyMetadata(inputSong, outputSong)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Change BPM of audio files in a folder.")
    parser.add_argument("-f", "--folder", required=True, help="Path to the folder containing audio files")
    parser.add_argument("-b", "--bpm", type=int, required=True, help="Target BPM for audio files")
    args = parser.parse_args()

    folder, bpm = args.folder, args.bpm
    files = os.listdir(folder)
    for file in files:
        filePath = os.path.join(folder, file)
        main(bpm=bpm, factor=None, inputSong=filePath)
