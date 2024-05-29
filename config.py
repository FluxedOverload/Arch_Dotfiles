# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# _                            _       
#(_)_ __ ___  _ __   ___  _ __| |_ ___ 
#| | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#| | | | | | | |_) | (_) | |  | |_\__ \
#|_|_| |_| |_| .__/ \___/|_|   \__|___/
#            |_|                       

import os
import re
import socket
import subprocess
import json
from libqtile import hook
from libqtile import qtile
from typing import List  
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Spacer, Backlight, LaunchBar
from libqtile.widget.image import Image
from libqtile.dgroups import simple_key_binder
from pathlib import Path
from libqtile.log_utils import logger

from libqtile.backend.wayland import InputConfig

#from qtile_extras import widget
#from qtile_extras.widget.decorations import RectDecoration
#from qtile_extras.widget.decorations import PowerLineDecoration


# _  __          _     _           _ _                 
#| |/ /___ _   _| |__ (_)_ __   __| (_)_ __   __ _ ___ 
#| ' // _ \ | | | '_ \| | '_ \ / _` | | '_ \ / _` / __|
#| . \  __/ |_| | |_) | | | | | (_| | | | | | (_| \__ \
#|_|\_\___|\__, |_.__/|_|_| |_|\__,_|_|_| |_|\__, |___/
#          |___/                             |___/     

mod = "mod4"
terminal = guess_terminal()


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
#
## tofi
#
    Key([mod], "r", lazy.spawn("tofi-drun"), desc="Launch an application."),
#
## screenshot
#
    Key([mod], "p", lazy.spawn("grim -o DP-1 - | wl-copy")),
    Key([mod, "control"], "p", lazy.spawn("grim -g '$(slurp)' - | wl-copy")),


]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )
#__        __         _                                  
#\ \      / /__  _ __| | _____ _ __   __ _  ___ ___  ___ 
# \ \ /\ / / _ \| '__| |/ / __| '_ \ / _` |/ __/ _ \/ __|
#  \ V  V / (_) | |  |   <\__ \ |_) | (_| | (_|  __/\__ \
#   \_/\_/ \___/|_|  |_|\_\___/ .__/ \__,_|\___\___||___/
#                             |_|                        


group_names = 'DESK(1) WWW(2) TERM(3) OBSI(4) DC(5) MP3(6) VM(7) RDP(8) VPN(9)'.split()
groups = [Group(name, layout='max') for name in group_names]
for i, name in enumerate(group_names):
    indx = str(i + 1)
    keys += [
        Key([mod], indx, lazy.group[name].toscreen()),
        Key([mod, 'shift'], indx, lazy.window.togroup(name))]


# _                            _       
#| |    __ _ _   _  ___  _   _| |_ ___ 
#| |   / _` | | | |/ _ \| | | | __/ __|
#| |__| (_| | |_| | (_) | |_| | |_\__ \
#|_____\__,_|\__, |\___/ \__,_|\__|___/
#            |___/                     

layout_theme = {
    "border_focus":'#E3DBAB',
    "border_normal":'#8CB7D9',
    "border_width" : 3,
    "margin" : 10,
    "margin_on_single" : 12,
}

layouts = [
        layout.RatioTile(**layout_theme),

]


#__        ___     _            _       
#\ \      / (_) __| | __ _  ___| |_ ___ 
# \ \ /\ / /| |/ _` |/ _` |/ _ \ __/ __|
#  \ V  V / | | (_| | (_| |  __/ |_\__ \
#   \_/\_/  |_|\__,_|\__, |\___|\__|___/
#                    |___/              

widget_defaults = dict(
    font="Roboto Mono",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

#----------------------------------------
#decor_left = {
#    "decorations": [
#        PowerLineDecoration(
#            path="arrow_left"
#            # path="rounded_left"
#            # path="forward_slash"
#            # path="back_slash"
#        )
#    ],
#}
#
#decor_right = {
#    "decorations": [
#        PowerLineDecoration(
#            path="arrow_right"
#            # path="rounded_right"
#            # path="forward_slash"
#            # path="back_slash"
#        )
#    ],
#}
#-----------------------------------------



# ____                               
#/ ___|  ___ _ __ ___  ___ _ __  ___ 
#\___ \ / __| '__/ _ \/ _ \ '_ \/ __|
# ___) | (__| | |  __/  __/ | | \__ \
#|____/ \___|_|  \___|\___|_| |_|___/
                                    

screens = [
#Samsung Left
    Screen(
        top=bar.Bar(
            [ 
                widget.Image(
                    background = '#060D13D9',
                    filename = '~/.config/Icons/Arch_Logo.png',
                    margin = 6,
                    mouse_callbacks = {lazy.spawn("neofetch")},
                    ),
                widget.GroupBox(
                    background = '#060D13D9',
                    inactive = '#C9C29C',
                    active = '#C9C29C',
                    highlight_method='line',
                    highlight_color = '#0000004D',
                    this_current_screen_border = '#C9C29C',
                    this_screen_border = '#106EBC',
                    other_current_screen = '#8CB7D9',
                    other_screen_border = '#8CB7D9',
                    block_highlight_text_color = '#C9C29C',
                    ),
                widget.WindowName(
                    background = '#060D13D9',
                    foreground = '#C9C29C',
                    ),             
                widget.Clock(
                    background = '#060D13D9',
                    foreground = 'C9C29C',
                    margin = 5,
                    format="%a %d.%h.%y | %H:%M",
                    ),               
            ],
            35,
            border_width = [6, 0, 3,0],
            border_color = '#ffffff00'
        ),
        #Set Wallpaper
        wallpaper = "~/.config/Wallpapers/Real_Mount.jpg",
        wallpaper_mode = 'fill',
    ),
#Acer mid
    Screen(
        top=bar.Bar(
            [ 
                widget.Image(
                    background = '#060D13D9',
                    filename = '~/.config/Icons/Arch_Logo.png',
                    margin = 6,
                    mouse_callbacks = {lazy.spawn("neofetch")},
                    ),
                widget.GroupBox(
                    background = '#060D13D9',
                    inactive = '#C9C29C',
                    active = '#C9C29C',
                    highlight_method='line',
                    highlight_color = '#0000004D',
                    this_current_screen_border = '#C9C29C',
                    this_screen_border = '#106EBC',
                    other_current_screen = '#8CB7D9',
                    other_screen_border = '#8CB7D9',
                    block_highlight_text_color = '#C9C29C',
                    ),
                widget.WindowName(
                    background = '#060D13D9',
                    foreground = '#C9C29C',
                    ),             
                widget.Clock(
                    background = '#060D13D9',
                    foreground = 'C9C29C',
                    margin = 5,
                    format="%a %d.%h.%y | %H:%M",
                    ),
                widget.QuickExit(
                    background = '#060D13D9',
                    foreground = '#C9C29C',
                    ),
            ],
            35,
            border_width = [6, 0, 3,0],
            border_color = '#ffffff00'
        ),
        #Set Wallpaper
        wallpaper = "~/.config/Wallpapers/Real_Mount.jpg",
        wallpaper_mode = 'fill',
    ),

#Samsung Rechts
    Screen(
        top=bar.Bar(
            [ 
                widget.Image(
                    background = '#060D13D9',
                    filename = '~/.config/Icons/Arch_Logo.png',
                    margin = 6,
                    mouse_callbacks = {lazy.spawn("neofetch")},
                    ),
                widget.GroupBox(
                    background = '#060D13D9',
                    inactive = '#C9C29C',
                    active = '#C9C29C',
                    highlight_method='line',
                    highlight_color = '#0000004D',
                    this_current_screen_border = '#C9C29C',
                    this_screen_border = '#106EBC',
                    other_current_screen = '#8CB7D9',
                    other_screen_border = '#8CB7D9',
                    block_highlight_text_color = '#C9C29C',
                    ),
                widget.WindowName(
                    background = '#060D13D9',
                    foreground = '#C9C29C',
                    ),             
                widget.Clock(
                    background = '#060D13D9',
                    foreground = 'C9C29C',
                    margin = 5,
                    format="%a %d.%h.%y | %H:%M",
                    ),
            ],
            35,
            border_width = [6, 0, 3,0],
            border_color = '#ffffff00'
        ),
        #Set Wallpaper
        wallpaper = "~/.config/Wallpapers/Real_Mount.jpg",
        wallpaper_mode = 'fill',
    ),
]


# __  __                      
#|  \/  | ___  _   _ ___  ___ 
#| |\/| |/ _ \| | | / __|/ _ \
#| |  | | (_) | |_| \__ \  __/
#|_|  |_|\___/ \__,_|___/\___|
                             
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = {
    "type:keyboard": InputConfig(kb_layout="de"),
}

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# Hooks

# HOOK startup
@hook.subscribe.startup_once
def autostart():
    autostartscript = "~/.config/qtile/autostart.sh"
    home = os.path.expanduser(autostartscript)
    subprocess.Popen([home])

