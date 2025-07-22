# 🎵 BPMorph

**BPMorph** is a Python tool for batch-changing the BPM (Beats Per Minute) of audio files (MP3/WAV) in a folder. It uses `librosa` for BPM detection, `pydub` for audio conversion, and the `rubberband` CLI for high-quality time-stretching, while preserving original metadata.

---

## 🚀 Features

- 🔍 Detects BPM of audio files automatically
- ⚡ Changes BPM or applies a custom stretch factor
- 🎼 Preserves original MP3 metadata
- 🗂️ Batch processes all audio files in a folder
- 🐍 Simple command-line interface

---

## 🛠️ Requirements

- Python 3.8+
- [Rubberband](https://breakfastquay.com/rubberband/) CLI tool installed and available in your PATH

Install Python dependencies:

```bash
    pip install -r requirements.txt
```

---

## 📦 Installation

1. Clone this repository:
```bash
    git clone https://github.com/Sklyvan/BPMorph
    cd BPMorph
```
2. Install dependencies as above.
3. Install `rubberband` with APT:
```bash
    sudo apt install rubberband-cli
```

---

## 🎚️ Usage

Run the tool from the command line:

```bash
    python -m app.main -f <folder_path> -b <target_bpm>
```
`-f`, `--folder`: Path to the folder containing your audio files <br>
`-b`, `--bpm`: Target BPM for all files

**Example:**

```bash
    python -m app.main -f ./music -b 165
```

All MP3 files in `./music` will be processed and new files with the target BPM will be created (e.g., `Song_165BPM.mp3`).

---

## 📝 Notes

- Only one of `bpm` or `factor` can be used at a time (CLI currently supports BPM).
- Temporary WAV files are created and deleted during processing.
- Metadata is copied from the original MP3 to the output.

---

## ❓ Troubleshooting

- Make sure `rubberband` is installed and accessible from your terminal.
- Supported input formats: MP3, WAV (others may work if supported by `pydub`).

---

## 📄 License

See [LICENSE](LICENSE) for details. The project is licensed under the MIT License.
