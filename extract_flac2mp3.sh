#!/bin/bash

## USAGE: extract_flac2mp3.sh "path/to/dir"
## EXAMPLE: extract_flac2mp3.sh "FLAC_dir/Rush"
## DESCRIPTION: This script will search a directory for archives to extract,
## Then search for FLAC files to convert to v0 mp3
## Designed for use on OSX / macOS
## Requires pz7ip, and ffmpeg to be installed using Homebrew with these commands
## $ brew install ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-libass --with-libquvi --with-libvorbis --with-libvpx --with-opus --with-x265
## $ brew update && brew upgrade ffmpeg
## $ brew install p7zip

# ~~~~~ CHECK SCRIPT ARGS ~~~~~ #
if (($# != 1)); then
  grep '^##' $0
  exit
fi

# ~~~~~ GET SCRIPT ARGS ~~~~~ #
input_dir="$1"

# file with passwords to try, one per line
password_file="passwords.txt"
divder="---------------------------------"

# ~~~~~ EXTRACT ARCHIVES ~~~~~ #
printf "\n%s\nSearching for archive files in directory:\n%s\n\n" "$divder" "$input_dir"
find "$input_dir" \( -name '*.zip' -o -name '*.rar' -o -name '*.7z' \) | while read item; do
    cat "$password_file" | while read password; do
        if [ ! -z "$password" ]; then
            printf "\nAttempting to extract file:\n%s\n\nUsing password:\n%s\n\n" "$item" "$password"
            7z x "$item" -p${password} -y
        fi
    done
done

# ~~~~~ CONVERT FLAC ~~~~~ #
printf "\n%s\nSearching for FLAC files in directory:\n%s\n\n" "$divder" "$input_dir"
find "$input_dir" -name "*.flac" -print0 | while read -d $'\0' item; do
    (
    output="${item%%.flac}.mp3"
    printf "\n%s\n" "$divder"
    printf "\nINPUT FLAC:\n%s\n\n" "$item"
    printf "\nOUTPUT MP3:\n%s\n\n" "$output"
    ffmpeg -y -i "$item" -aq 0 "$output" < /dev/null
    )
done
