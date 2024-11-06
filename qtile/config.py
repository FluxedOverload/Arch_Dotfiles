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


# __       
#(_)_ __ ___  _ __   ___  _ __| |_ ___ 
#| | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#| | | | | | | |_) | (_) | |  | |_\__ \
#|_|_| |_| |_| .__/ \___/|_|   \__|___/
#            |_|                       

#-----------------------------------------
# qtile-standard
#-----------------------------------------
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
#-----------------------------------------
#Features
#-----------------------------------------

#-----------------------------------------
# qtile-wayland
#-----------------------------------------
from libqtile.backend.wayland import InputConfig
#-----------------------------------------
# qtile-extras
#-----------------------------------------
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.widget.decorations import PowerLineDecoration
#from qtile_extras.layout.decorations import RoundedCorners



# _  __          _     _           _ _                 
#| |/ /___ _   _| |__ (_)_ __   __| (_)_ __   __ _ ___ 
#| ' // _ \ | | | '_ \| | '_ \ / _` | | '_ \ / _` / __|
#| . \  __/ |_| | |_) | | | | | (_| | | | | | (_| \__ \
#|_|\_\___|\__, |_.__/|_|_| |_|\__,_|_|_| |_|\__, |___/
#          |___/                             |___/    

mod = "mod4"
terminal = guess_terminal()
Browser = "firefox"
HTB = "firefox hackthebox"
Mail = "firefox outlook"
FileManager = "thunar"
Music = "spotify-launcher"



keys = [
#----------------------------------------
# Change Focus
#-----------------------------------------
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

#-----------------------------------------
# Move Windows
#-----------------------------------------
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

#-----------------------------------------
# Change Size
#-----------------------------------------
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

#-----------------------------------------
# Terminal
#-----------------------------------------
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack",),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

#-----------------------------------------
# Edit Layout/Window
#-----------------------------------------
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window",),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

#-----------------------------------------
# Rofi
#-----------------------------------------
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launch an application."),
#-----------------------------------------
# Screenshot
#-----------------------------------------
    Key([mod], "s", lazy.spawn("grim - | wl-copy",shell=True), desc="take screen scrennshot"),
    Key([mod, "shift"], "s", lazy.spawn('grim -g "$(slurp)" - | wl-copy', shell=True), desc="take area screenshot"),
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

group_names = '1 2 3 4 5 6 7 8 9'.split()
groups = [Group(name, layout='max') for name in group_names]
for i, name in enumerate(group_names):
    indx = str(i + 1)
    keys += [
        Key([mod], indx, lazy.group[name].toscreen()),
        Key([mod, 'shift'], indx, lazy.window.togroup(name))]

####
#Colors
####


#Normal
color = [
["#232a2e"], # 0  bg_dim
["#2d353b"], # 1  bg0
["#343f44"], # 2  bg1
["#3d484d"], # 3  bg2
["#475258"], # 4  bg3
["#4f585e"], # 5  bg4
["#56635f"], # 6  gb5 
["#d3c6aa"], # 7  Foreground / Text / White
["#e67e80"], # 8  Red
["#e69875"], # 9  Orange
["#dbbc7f"], # 10 Yellow
["#a7c080"], # 11 Green
["#83c092"], # 12 Cyan
["#7fbbb3"], # 13 Blue
["#d699b6"], # 14 Pink
["#859289"], # 15 Grey
]

#Transparent
color_tp = [
["#232a2ef2"], # 0  bg_dim
["#2d353bf2"], # 1  bg0
["#343f44f2"], # 2  bg1
["#3d484df2"], # 3  bg2
["#475258f2"], # 4  bg3
["#4f585ef2"], # 5  bg4
["#56635ff2"], # 6  gb5 
["#d3c6aaf2"], # 7  Foreground / Text / White
["#e67e80f2"], # 8  Red
["#e69875f2"], # 9  Orange
["#dbbc7ff2"], # 10 Yellow
["#a7c080f2"], # 11 Green
["#83c092f2"], # 12 Cyan
["#7fbbb3f2"], # 13 Blue
["#d699b6f2"], # 14 Pink
["#859289f2"], # 15 Grey
]


# _                            _       
#| |    __ _ _   _  ___  _   _| |_ ___ 
#| |   / _` | | | |/ _ \| | | | __/ __|
#| |__| (_| | |_| | (_) | |_| | |_\__ \
#|_____\__,_|\__, |\___/ \__,_|\__|___/
#            |___/                     

layout_theme = {
    "border_focus": color[11],
    "border_normal": '#00000000',
    "border_width":1,
    "margin":8,
    "margin_on_single":8,
}

layouts = [
        layout.RatioTile(**layout_theme),
        layout.MonadThreeCol(**layout_theme),
        layout.MonadTall(**layout_theme),
        layout.MonadWide(**layout_theme),
        layout.Floating(),
]


#__        ___     _            _
#\ \      / (_) __| | __ _  ___| |_ ___
# \ \ /\ / /| |/ _` |/ _` |/ _ \ __/ __|
#  \ V  V / | | (_| | (_| |  __/ |_\__ \
#   \_/\_/  |_|\__,_|\__, |\___|\__|___/
#                    |___/

widget_defaults = dict(
    font="Jetbrains Mono Nerd Bold",
    fontsize=12,
    padding=12,
)
extension_defaults = widget_defaults.copy()

#----------------------------------------
# Decorations
#----------------------------------------
#decor_left = {
#    "decorations": [
#        PowerLineDecoration(
#            # path="arrow_left"
#            path="rounded_left"
#            # path="forward_slash"
#            # path="back_slash"
#        )
#    ],
#}
#
#decor_right = {
#    "decorations": [
#        PowerLineDecoration(
#            # path="arrow_right"
#            path="rounded_right"
#            # path="forward_slash"
#            # path="back_slash"
#        )
#    ],
#}
#
decoration_group = {
    "decorations": [
        RectDecoration(
            colour= color_tp[1],
            radius=10,
            filled=True,
            padding_x=0,
            group=True,
            line_colour=color[9],
            line_width=1.2,
            )
    ],
    "padding": 5,
}

#-----------------------------------------
# Widget List
#-----------------------------------------
widget_list = [
    #widget.Image(
    #    background = '#00000000',
    #    filename = '/usr/share/Icons/Arch.png',
    #    margin = 3,
    #    mouse_callbacks = {"Button1": lazy.spawn(terminal)},
#        **decoration_group
    #),    
    widget.GroupBox(
        background = '#00000000',
        active = color[7],
        inactive = color[6],
        highlight_method='text',
        this_current_screen_border = color[11],
        **decoration_group
    ),
    widget.Prompt(
    ),
#---------------------------------------
widget.Spacer(
        length = 10,
        background = '#00000000'
    ),
widget.Image(
        background = '#00000000',
        filename = '/usr/share/Icons/Mail.png',
        margin_y = 8,
        margin_x = 3,
        mouse_callbacks = {"Button1": lazy.spawn(Mail)},
        **decoration_group
    ),
widget.Image(
        background = '#00000000',
        filename = '/usr/share/Icons/HTB.png',
        margin_y = 8,
        mouse_callbacks = {"Button1": lazy.spawn(HTB)},
        **decoration_group
    ),
widget.Image(
        background = '#00000000',
        filename = '/usr/share/Icons/Music.png',
        margin_y = 8,
        mouse_callbacks = {"Button1": lazy.spawn(Music)},
        **decoration_group
    ),
widget.Image(
        background = '#00000000',
        filename = '/usr/share/Icons/Firefox.png',
        margin_y = 8,
        mouse_callbacks = {"Button1": lazy.spawn(Browser)},
        **decoration_group
    ),
widget.Image(
        background = '#00000000',
        filename = '/usr/share/Icons/Files.png',
        margin_y = 8,
        margin_x = 3,
        mouse_callbacks = {"Button1": lazy.spawn(FileManager)},
        **decoration_group
    ),
#---------------------------------------
    widget.Spacer(
        length = bar.STRETCH,
        background = '#00000000'
    ),
    widget.WindowName(
        background = '#00000000',
        foreground = color[7],
        **decoration_group
    ),
    widget.Spacer(
        length = bar.STRETCH,
        background = '#00000000'
    ),
#---------------------------------------
    widget.WiFiIcon(
        background = '#00000000',
        active_colour = color[7],
        inacitve_colour = color[6],
        disconnected_colour = color[8],
        interface = 'wlp0s20f3',
        padding_y = 10,
        padding_x = 3,
        **decoration_group
    ),
    widget.Volume(
        background = '#00000000',
        foreground = color[7],
        **decoration_group
    ),
    widget.Battery(
        background = '#00000000',
        foreground = color[7],
        format='{char} | {percent:2.0%}',
        charge_char = '+',
        discharge_char = '-',
        empty_char = '±',
        #charge_controller: lambda (0, 90)
        **decoration_group
    ),
    widget.Spacer(
        length = 10,
        background = '#00000000'
    ),
    widget.Clock(
        background = '#00000000',
        foreground = color[7],
        margin = 3,
        format="%a %d.%h.%y | %H:%M",
        **decoration_group
    ),
#    widget.StatusNotifier(),    
]


# ____                               
#/ ___|  ___ _ __ ___  ___ _ __  ___ 
#\___ \ / __| '__/ _ \/ _ \ '_ \/ __|
# ___) | (__| | |  __/  __/ | | \__ \
#|____/ \___|_|  \___|\___|_| |_|___/

screens = [
    Screen(
        top=bar.Bar(
            widget_list,
            35,
            border_width = [10, 8, 2, 8],
            border_color = '#ffffff00',
        ),
        #Set Wallpaper
        wallpaper = "/usr/share/Wallpaper/Forest.jpg",
        wallpaper_mode = 'fill',
    ),
]

# Drag floating layouts.
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
    "*": InputConfig(tap=True, natural_scroll=True), #toupad
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
