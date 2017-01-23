#!/bin/bash

# import-sequences.py <proton-path> <admin-key> <layout-id>

set -o nounset
set -o errexit

dir="$HOME/Dropbox/Great Northern Sequencing/Sequencing/Sequence Data"
seq_dir="$dir/Sequences"
audio_dir="$dir/Audio"

declare -a seqs audio

seqs=( \
  "Baba Yaga.vix" \
  "Beethoven 5.vix" \
  "Slavonic Dance.vix" \
  "Lucifer Polka.vix" \
  "Flight of the Bumblebee.vix" \
  "Hora Staccato.vix" \
  "Firebird.vix" \
)

audio=( \
  "Baba Yaga.ogg" \
  "Beethoven 5.ogg" \
  "Slavonic Dance in C major.ogg" \
  "Lucifer Polka.ogg" \
  "Flight of the Bumblebee.ogg" \
  "Hora Staccato.ogg" \
  "Firebird Suite.ogg" \
)

for i in {0..6}; do
  ./converter.py import-sequence "$1" "$2" "$seq_dir/${seqs[$i]}" "$audio_dir/${audio[$i]}" "$3"
done
