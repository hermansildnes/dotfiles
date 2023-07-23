from libqtile.command import lazy
from typing import List  # noqa: F401
from libqtile import bar, layout, widget, hook
from libqtile.config import (
    Click,
    Drag,
    Group,
    Screen,
    Key,
    Match,
    Rule,
    DropDown,
)
from libqtile.config import EzKey as Key2
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess

mod = "mod4"
terminal = "alacritty"
browser = "brave"
file_manager = "pcmanfm"  # I mostly use dired inside emacs for file management, but this exists as a gui file manager in case I need it
music_player = "spotify"
run_launcher = "rofi -show run"

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


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.call([home])


keys = [
    Key2(
        "A-S-<Tab>", lazy.layout.down(), desc="Move focus down in stack pane"
    ),
    Key2("A-<Tab>", lazy.layout.up(), desc="Move focus up in stack pane"),
    Key2(
        "S-A-k",
        lazy.layout.shuffle_down(),
        desc="Move window down in current stack ",
    ),
    Key2(
        "S-A-j",
        lazy.layout.shuffle_up(),
        desc="Move window down in current stack ",
    ),
    Key2("S-A-h", lazy.layout.shrink()),
    Key2("S-A-l", lazy.layout.grow()),
    Key2("M-<space>", lazy.next_layout(), desc="Toggle between layouts"),
    Key2("M-S-f", lazy.window.toggle_floating(), desc="Toggle Floating"),
    Key2("M-S-c", lazy.window.kill(), desc="Kill focused window"),
    Key2("M-S-r", lazy.restart(), desc="Restart qtile"),
    Key2("M-S-q", lazy.shutdown(), desc="Shutdown qtile"),
    Key2("M-<Return>", lazy.spawn(terminal), desc="Launch terminal"),
    Key2(
        "M-S-<Return>",
        lazy.spawn(run_launcher),
        desc="Spawn a command using a prompt widget",
    ),
    Key2("M-b", lazy.spawn(browser), desc="Launch main browser"),
    Key2("M-f", lazy.spawn(file_manager), desc="Launch file manager"),
    Key2(
        "<XF86AudioRaiseVolume>",
        lazy.spawn("changeVolume -5%"),
        desc="Raise Volume",
    ),
    Key2(
        "<XF86AudioLowerVolume>",
        lazy.spawn("changeVolume +5%"),
        desc="Lower Volume",
    ),
    Key2(
        "<XF86MonBrightnessUp>",
        lazy.spawn("light -A 5"),
        desc="Raise Brightness",
    ),
    Key2(
        "<XF86MonBrightnessDown>",
        lazy.spawn("light -U 5"),
        desc="Lower Brightness",
    ),
    Key2(
        "M-l",
        lazy.spawn("slock"),
        desc="Lock screen usin slock",
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

group_names = [
    ("", {"layout": "monadtall"}),
    ("", {"layout": "monadtall"}),
    ("", {"layout": "monadtall"}),
    ("", {"layout": "monadtall"}),
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(
        Key([mod], str(i), lazy.group[name].toscreen())
    )  # Switch to another group
    keys.append(
        Key([mod, "shift"], str(i), lazy.window.togroup(name))
    )  # Send current window to another group

layout_theme = {
    "border_width": 4,
    "margin": 8,
    "border_focus": highlight,
    "border_normal": backcolor,
}

# Layouts
layouts = [
    layout.MonadTall(**layout_theme),
    # layout.Columns(),
    # layout.Bsp(),
    layout.Max(**layout_theme),
    layout.Floating(
        border_width=4, border_normal=backcolor, border_focus=highlight
    ),
    # layout.Stack(**layout_theme),
    # layout.Matrix(),
    # layout.MonadWide(border_focus="#5e497c", border_normal="#002525"),
    # layout.RatioTile(),
    # layout.Tile(border_focus = "#005858", border_normal = "#002525", border_width ="2"),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Fira Code Bold",
    fontsize=14,
    padding=2,
    background=backcolor,
    foreground=txtcolor2,
)
extension_defaults = widget_defaults.copy()

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
        fontsize=16,
        font="Fira Code Bold",
        foreground=purple,
        format="{char} {percent:2.0%}",
        update_interval=30,
        background=backcolor,
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
        padding=6, fontsize=16, format="{MemUsed: .0f}M ", foreground=green
    ),
    widget.Sep(foreground=highlight, linewidth=2, size_percent=60, padding=8),
    widget.CPU(foreground=yellow, padding=10),
    widget.Sep(foreground=highlight, linewidth=2, size_percent=60, padding=8),
    widget.Clock(format="%A, %B %d - %H:%M ", padding=10),
]

screens = [
    Screen(
        top=bar.Bar(
            widgets,
            size=30,
        ),
    )
]

mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
