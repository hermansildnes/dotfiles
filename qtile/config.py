# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.config import EzKey as Key2
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "brave" # My browser of choice

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod, "shift"], "Return",
             lazy.spawn("rofi -show run"),
             desc='Run rofi'
             ),
         Key([mod], "b",
             lazy.spawn(myBrowser),
             desc='brave'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart QtLile'
             ),
         Key([mod, "shift"], "q",
             lazy.spawn("slock"),
             desc='Lock'
             ),
         ### Switch focus to specific monitor (out of two)
         Key([mod], "w",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "e",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall)'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall)'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
         Key2("<XF86AudioRaiseVolume>",
             lazy.spawn("~/scripts/volume.sh +5%"),
             desc="Raise Volume",
             ),
         Key2("<XF86AudioLowerVolume>",
             lazy.spawn("~/scripts/volume.sh -5%"),
             desc="Lower Volume",
             ),
         Key2("<XF86MonBrightnessUp>",
             lazy.spawn("light -A 5"),
             desc="Raise Brightness",
             ),
         Key2("<XF86MonBrightnessDown>",
             lazy.spawn("light -U 5"),
             desc="Lower Brightness",
             ),
         Key2(
             "C-<Return>",
             lazy.spawn("dunstctl close"),
             desc="Close dunst notification",
             ),
         Key2(
             "C-S-<Return>",
             lazy.spawn("dunstctl history-pop"),
             desc="Reopen last dunst notification",
             ),
         ]




backcolor = "#2E3440"
backcolor2 = "#3B4252"
txtcolor = "#ECEFF4"
txtcolor2 = "#E5E9F0"
highlight = "#88C0D0"
highlight2 = "#81A1C1"
red = "#BF616A"
yellow = "#EBCB8B"
green = "#A3BE8C"
purple = "#B48EAD"

groups = [Group("DEV", layout='monadtall'),
          Group("WWW", layout='monadtall'),
          Group("SYS", layout='monadtall'),
          Group("MUS", layout='monadtall'),
          Group("VID", layout='monadtall')]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {
    "border_width": 4,
    "margin": 8,
    "border_focus": highlight,
    "border_normal": backcolor,
}

# Layouts
layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(
        border_width=4, border_normal=backcolor, border_focus=highlight
    )]

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Fira Code Bold",
    fontsize = 20,
    padding = 2,
    background=backcolor,
    foreground=txtcolor2,
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets = [
        widget.Sep(foreground=backcolor, padding=4, linewidth=0),
        widget.GroupBox(
            font="Fira Code",
            fontsize=18,
            margin_y=4,
            margin_x=0,
            padding_y=4,
            padding_x=8,
            borderwidth=4,
            active=txtcolor,
            inactive=txtcolor2,
            rounded=False,
            highlight_color=backcolor,
            highlight_method="line",
            this_current_screen_border=highlight,
            this_screen_border=highlight,
            foreground=txtcolor,
            background=backcolor,
            disable_drag=True,
        ),
        widget.Sep(foreground=highlight, linewidth=2, size_percent=60, padding=15),
        widget.CurrentLayout(
            padding=10,
            foreground=green,
        ),
        widget.Sep(foreground=highlight, linewidth=2, size_percent=60, padding=15),
        widget.WindowName(foreground=highlight2, padding=4),
        widget.Systray(icon_size=25, padding=10),
        widget.Sep(linewidth=0, size_percent=60, padding=6),
        widget.Sep(foreground=highlight, linewidth=2, size_percent=60, padding=8),
        widget.Battery(
            foreground=purple,
            format="{char} {percent:2.0%}",
            update_interval=30,
            discharge_char="↓",
            charge_char="↑",
            full_char="",
            low_foreground=red,
            low_percentage=0.2,
            notify_below=0.15,
            padding=10,
        ),
        widget.Sep(foreground=highlight, linewidth=2, size_percent=60, padding=8),
        widget.Memory(
            padding=6, format="{MemUsed: .0f}M ", foreground=green
        ),
        widget.Sep(foreground=highlight, linewidth=2, size_percent=60, padding=8),
        widget.CPU(foreground=yellow, padding=10),
        widget.Sep(foreground=highlight, linewidth=2, size_percent=60, padding=8),
        widget.Clock(format="%A, %B %d - %H:%M ", padding=10),
        ]
    return widgets

def HDMIConnected():
    output = subprocess.check_output([os.path.expanduser("~/.config/qtile/kernel.sh")]).decode()
    if "\nconnected\n" in output or output.startswith("connected\n"):
        return True
    return False

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[6:7]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=50)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=35))]
    

if HDMIConnected():
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

else:
    screens = [Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=50))]
    widgets_list = init_widgets_list()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.call([home])

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

from libqtile.scripts.main import VERSION
wmname = f"Qtile {VERSION}"
