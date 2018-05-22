# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2018, Galen Curwen-McAdams

def keybindings():
    actions = {}
    # app always handled
    actions["app"] = {}
    actions["app"]["app_exit"] = [["c"], ["ctrl"]]
    actions["app"]["tab_next"] = [["left"], ["ctrl"]]
    actions["app"]["tab_previous"] = [["right"], ["ctrl"]]
    actions["app"]["ingest"] = [["i"], ["ctrl"]]
    # tabs have different actions / bindings
    # handled if tab is currently active / visible
    # maps
    actions["grid"] = {}
    actions["grid"]["jump"] = [["x"], []]
    actions["grid"]["enlarge"] = [["up"], ["ctrl"]]
    actions["grid"]["shrink"] = [["down"], ["ctrl"]]
    actions["grid"]["pan_up_left"] = [["w"], []]
    actions["grid"]["pan_up_right"] = [["r"], []]
    actions["grid"]["pan_down_left"] = [["z"], []]
    actions["grid"]["pan_down_right"] = [["c"], []]
    actions["grid"]["pan_up"] = [["e"], []]
    actions["grid"]["pan_down"] = [["d"], []]
    actions["grid"]["pan_left"] = [["s"], []]
    actions["grid"]["pan_right"] = [["f"], []]


    return actions