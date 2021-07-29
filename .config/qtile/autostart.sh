#!/bin/bash
setxkbmap no &
picom --config ~/.config/picom.conf &
nm-applet &
blueman-applet &
/usr/lib/geoclue-2.0/demos/agent &
redshift-gtk &
dunst &
changeVolume 35% &
