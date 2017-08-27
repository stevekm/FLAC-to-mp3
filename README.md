# FLAC-to-mp3
Script for extracting music from password-protected archives (`p7zip`) and converting FLAC files to mp3 (`ffmpeg`).
Written for & tested under OS X / macOS, but should work on any system with these programs installed

This script will:
- Search the given directory for any `.zip`, `.rar`, or `.7z` files, and try to extract them with the passwords in `passwords.txt`
- Search the given directory for any `.flac` files, and convert them to v0 `.mp3` format

# Setup
- First, clone this repo.

```bash
git clone https://github.com/stevekm/FLAC-to-mp3.git
cd FLAC-to-mp3
```

- Make sure you have `p7zip` and `ffmpeg` installed. On OS X/macOS, you can install it with the following commands with  [Homebrew](https://brew.sh/).

```bash
brew install p7zip
brew install ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-libass --with-libquvi --with-libvorbis --with-libvpx --with-opus --with-x265
brew update && brew upgrade ffmpeg
```

- Put your archive passwords in the file `passwords.txt` (included), one password per line. 

# Usage
Run the script on a directory that contains password-protected archive files (.7z, .rar, .zip) and/or FLAC files. 

```bash
./extract_flac2mp3.sh "path/to/my_music_folder"
```

- NOTE: The path to the directory to process should not be a subdirectory of this repo.

# Software
- 7-Zip [64] 16.02
- ffmpeg version 3.3

