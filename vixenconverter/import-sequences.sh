#!/bin/bash

# import-sequences.py <proton-path> <admin-key> <layout-id>

set -o nounset
set -o errexit

dir="$HOME/Dropbox/Light Show 2017/Sequencing/Sequence Data"
seq_dir="$dir/Sequences/Show 2017 DO_NOT_EDIT"
audio_dir="$dir/Audio"
key_dir="$HOME/Documents/2017 Code/proton/proton-cli/show2017.pub"

declare -a seqs audio


seqs=( \
  "1_Aurora.vix" \
  "2_Collide.vix" \
  "3_GalaxyGroove.vix" \
  "4_DnD.vix" \
  "5_GlorytotheBells.vix" \
)

audio=( \
  "1_Aurora.ogg" \
  "2_Collide.ogg" \
  "3_GalaxyGroove.ogg" \
  "4_DNDfinal.ogg" \
  "5_GlorytotheBells.ogg" \
)

for i in {0..4}; do
  ./converter.py import-sequence "$key_dir" "$seq_dir/${seqs[$i]}" "$audio_dir/${audio[$i]}" "2"
done
