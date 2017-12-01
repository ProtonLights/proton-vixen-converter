#!/bin/bash

# import-sequences.py <proton-path> <admin-key> <layout-id>

set -o nounset
set -o errexit

dir="$HOME/Dropbox/Light Show 2017/Sequencing/Sequence Data"
seq_dir="$dir/Sequences"
audio_dir="$dir/Audio"
key_dir="$HOME/Documents/2017 Code/proton/proton-cli/testshow2017.pub"

declare -a seqs audio


seqs=( \
  #"1_Aurora_JPProper.vix" \
  #"1_Aurora_KyleKrueger.vix" \
  #"2_Collide_AdamBarsness.vix" \
  #"2_Collide_JoshuaGuldberg.vix" \
  #"3_GalaxyGroove_KellyLarson.vix" \
  #"4_DND_MadisonWieczorek.vix" \
  #"4_DND_JulieWeber.vix" \
  #"5_GlorytotheBells_JessicaChiu.vix" \
  #"5_GlorytotheBells_AshmitaSarma.vix" \
  #"5_GlorytotheBells_JPProper.vix"
  "Dimmer_Test.vix"
)

audio=( \
  #"1_Aurora.ogg" \
  #"1_Aurora.ogg" \
  #"2_Collide.ogg" \
  #"2_Collide.ogg" \
  #"3_GalaxyGroove.ogg" \
  #"4_DNDfinal.ogg" \
  #"4_DNDfinal.ogg" \
  #"5_GlorytotheBells.ogg" \
  #"5_GlorytotheBells.ogg" \
  #"5_GlorytotheBells.ogg"
  "Announce_2MidShow.ogg"
)

for i in {0..0}; do
  ./converter.py import-sequence "$key_dir" "$seq_dir/${seqs[$i]}" "$audio_dir/${audio[$i]}" "2"
done