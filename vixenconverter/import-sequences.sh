#!/bin/bash

# import-sequences.py <proton-path> <admin-key> <layout-id>

set -o nounset
set -o errexit

dir="$HOME/Dropbox/Sequencing 2016/Sequencing/Sequence Data"
seq_dir="$dir/Sequences"
audio_dir="$dir/Audio"

declare -a seqs audio

seqs=( \
  "(1) Jingle Breaks.vix" \
  "(2) Feel Good.vix" \
  "(3) Collide.vix" \
  "(4) Unicorn Adventure.vix" \
  "(5) Glory to the Bells.vix" \
  "Preshow.vix" \
  "Midshow.vix" \
)

audio=( \
  "(1) Jingle Breaks.ogg" \
  "(2) Feel Good.ogg" \
  "(3) Collide.ogg" \
  "(4) Unicorn Adventure_Master.ogg" \
  "(5) Glory to the Bells.ogg" \
  "Preshow.ogg" \
  "Midshow.ogg" \
)

for i in {0..6}; do
  ./converter.py import-sequence "$1" "$2" "$seq_dir/${seqs[$i]}" "$audio_dir/${audio[$i]}" "$3"
done
