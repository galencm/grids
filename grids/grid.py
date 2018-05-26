# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2018, Galen Curwen-McAdams

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.vertex_instructions import Line
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from grids import bindings
import argparse
import os
import math
import hashlib
import pathlib
from xdg import (XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME)
from lxml import etree

class BindingsContainer(BoxLayout):
    def __init__(self, actions, **kwargs):
        self.actions = actions
        super(BindingsContainer, self).__init__()

    def setup_bindings(self):
        actions = 0
        for domain, domain_actions in self.actions.items():
            self.add_widget(Label(text=str(domain), height=40))
            for action, action_bindings in domain_actions.items():
                binding_widget = BindingItem(domain, action, action_bindings, self.actions, height=40)
                self.add_widget(binding_widget)
                actions += 1
        self.height = actions * 40

class BindingItem(BoxLayout):
    def __init__(self, domain, action, action_keybindings, actions, **kwargs):
        # self.rows = 1
        # self.cols = None
        self.orientation = "horizontal"
        self.keys = action_keybindings[0]
        self.modifiers = action_keybindings[1]
        self.domain = domain
        self.action = action
        self.actions = actions
        self.action_label = Label(text=str(self.action), height=40)
        self.keys_input = TextInput(text=str(",".join(self.keys)), multiline=False, height=40, size_hint_x=0.2)
        self.keys_input.bind(on_text_validate = lambda widget: self.set_binding())
        self.modifiers_input = TextInput(text=str(",".join(self.modifiers)), multiline=False, height=40, size_hint_x=0.2)
        self.modifiers_input.bind(on_text_validate = lambda widget: self.set_binding())
        super(BindingItem, self).__init__()
        self.add_widget(self.action_label)
        self.add_widget(self.keys_input)
        self.add_widget(self.modifiers_input)

    def set_binding(self):
        self.keys = self.parse_input(self.keys_input.text)
        self.modifiers= self.parse_input(self.modifiers_input.text)
        self.actions[self.domain][self.action] = [self.keys, self.modifiers]

    def parse_input(self, text):
        text = text.strip()
        text = text.replace(" ", "")
        return text.split(",")

class TabItem(TabbedPanelItem):
    def __init__(self, root=None, **kwargs):
        self.root = root
        # use subcontent to handle keybinds for widgets
        # nested somewhere in the tab
        self.sub_content = []
        super(TabItem , self).__init__(**kwargs)

class BgLabel(Label):
    # label with custom background color
    def __init__(self, **kwargs):
        super(BgLabel , self).__init__(**kwargs)

    def on_size(self, *args):
        try:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(.15, .15, .15, 1)
                Rectangle(pos=self.pos, size=self.size)
        except AttributeError:
            pass

class BgGridLayout(GridLayout):
    # grid layout with custom background color
    def __init__(self, **kwargs):
        super(BgGridLayout , self).__init__(**kwargs)

    def on_size(self, *args):
        try:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(.15, .15, .15, 1)
                Rectangle(pos=self.pos, size=self.size)
        except AttributeError:
            pass

class TxtPixel(ScrollView):
    def __init__(self, source=None, source_type=None, **kwargs):
        Window.bind(mouse_pos=self.is_mouse_over)
        self.mouse_above = False
        self.container = None
        self.font_increment = 2
        self.scroll_increment = 0.1
        self.source = source
        self.source_type = source_type
        super(TxtPixel , self).__init__(**kwargs)
        container_height = 4000
        container_width = 4000
        filler_height = 2000
        filler_width = 2000
        grid_container = FloatLayout(
                                   size_hint_y=None,
                                   size_hint_x=None
                                   )
        filler = BgLabel(text=source_text(source, source_type), size=(filler_width, filler_height))
        # set height to None so text will expand with font size
        # container needs to expand too
        # the texture_size shows correct values as font increases / decreases
        filler.text_size = filler_width, None #filler_height
        grid_container.add_widget(filler)
        grid_container.height = container_height
        grid_container.width = container_width
        self.container = grid_container
        self.add_widget(grid_container)
        filler.pos = 0, 0 #(grid_container.width / 2, grid_container.height / 2)

    def is_mouse_over(self, instance, value):
        if self.collide_point(*value):
            self.mouse_above = True
        else:
            self.mouse_above = False

    def enlarge(self):
        if self.mouse_above is True:
            try:
                for c in self.container.children:
                    c.font_size += self.font_increment
                    # print(c.text_size, c.texture_size, c.size)
                    # enlarge container as needed
                    # if too large, label becomes a black rectangle
                    if c.texture_size[0] > self.container.width:
                        self.container.width += c.texture_size[0]
                        self.container.do_layout()
                    if c.texture_size[1] > self.container.height:
                        self.container.height += c.texture_size[1]
                        self.container.do_layout()
            except Exception as ex:
                print(ex)

    def shrink(self):
        if self.mouse_above is True:
            try:
                for c in self.container.children:
                    c.font_size -= self.font_increment
                    # if c.texture_size[0] < self.container.width:
                    #     self.container.width = c.texture_size[0]
                    # if c.texture_size[1] < self.container.height:
                    #     self.container.height = c.texture_size[1]
            except Exception as ex:
                print(ex)

    def jump(self):
        if self.mouse_above is True:
            for c in self.container.children:
                self.scroll_x = c.center[0] / self.container.width
                self.scroll_y = c.center[1] / self.container.height
                with self.container.canvas:
                    self.container.canvas.remove_group("trace")
                    # scale line width with zoom / textsize
                    line_width = 100
                    Color(1, 1, 1, .05)
                    edge_width = c.width / 4
                    edge_height = c.height / 4
                    # print(c.texture_size, c.center)
                    Line(points=(0, 0, c.center[0], c.center[1]), width=line_width, group="trace")
                    Line(points=(self.container.height, 0, c.center[0], c.center[1]), width=line_width, group="trace")
                    Line(points=(self.container.height, self.container.width, c.center[0], c.center[1]), width=line_width, group="trace")
                    Line(points=(0, self.container.width, c.center[0], c.center[1]), width=line_width, group="trace")

    def pan_up_left(self):
        if self.mouse_above is True:
            self.scroll_y += self.scroll_increment
            self.scroll_x -= self.scroll_increment

    def pan_up_right(self):
        if self.mouse_above is True:
            self.scroll_y += self.scroll_increment
            self.scroll_x += self.scroll_increment

    def pan_down_left(self):
        if self.mouse_above is True:
            self.scroll_y -= self.scroll_increment
            self.scroll_x -= self.scroll_increment

    def pan_down_right(self):
        if self.mouse_above is True:
            self.scroll_y -= self.scroll_increment
            self.scroll_x += self.scroll_increment

    def pan_up(self):
        if self.mouse_above is True:
            self.scroll_y += self.scroll_increment

    def pan_down(self):
        if self.mouse_above is True:
            self.scroll_y -= self.scroll_increment

    def pan_left(self):
        if self.mouse_above is True:
            self.scroll_x -= self.scroll_increment

    def pan_right(self):
        if self.mouse_above is True:
            self.scroll_x += self.scroll_increment

class ImgPixel():
    pass

class GridApp(App):
    def __init__(self, *args, **kwargs):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.actions = bindings.keybindings()
        self.data_dir = pathlib.PurePath(XDG_DATA_HOME, "grids")
        self.config_dir = pathlib.PurePath(XDG_CONFIG_HOME, "grids")
        for directory in [self.data_dir, self.config_dir]:
            if not os.path.isdir(directory):
                os.mkdir(directory)
            else:
                print("{} found".format(directory))
        if "files" in kwargs:
            # use abspath for now when loading xml from xdg data dir
            # may revisit to make grids more portable
            self.files = [os.path.abspath(f) for f in kwargs["files"]]
        super(GridApp, self).__init__()

    def _keyboard_closed(self):
        # do not unbind the keyboard because
        # if keyboard is requested by textinput
        # widget, this keyboard used for app keybinds
        # will be unbound and not rebound after
        # defocusing textinput widget
        #
        # self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        # self._keyboard = None
        pass

    def tab_next(self):
        print(self.root.tab_list)
        for i, c in enumerate(self.root.tab_list):
            if c == self.root.current_tab:
                if i > 0:
                    self.root.switch_to(self.root.tab_list[i - 1], do_scroll=True)
                    break
                else:
                    self.root.switch_to(self.root.tab_list[len(self.root.tab_list) - 1], do_scroll=True)
                    break

    def tab_previous(self):
        for i, c in enumerate(self.root.tab_list):
            if c == self.root.current_tab:
                try:
                    self.root.switch_to(self.root.tab_list[i + 1], do_scroll=True)
                    break
                except IndexError as ex:
                    self.root.switch_to(self.root.tab_list[0], do_scroll=True)
                    break

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        for actions in ["app", self.root.current_tab.tab_name]:
            try:
                for k, v in self.actions[actions].items():
                    if keycode[1] in v[0] and not v[1] and not modifiers:
                        try:
                            getattr(self, "{}".format(k))()
                        except Exception as ex:
                            #print(ex)
                            pass
                        # use .content.children for tabs
                        for c in self.root.current_tab.content.children:
                            try:
                                getattr(c, "{}".format(k))()
                            except Exception as ex:
                                print(ex)

                        for lower_widget in self.root.current_tab.sub_content:
                            for c in lower_widget.children:
                                try:
                                    getattr(c, "{}".format(k))()
                                except Exception as ex:
                                    print(ex)

                    elif keycode[1] in v[0] and modifiers:
                        if len(set(v[1]).intersection(set(modifiers))) == len(modifiers):
                            try:
                                getattr(self, "{}".format(k))()
                            except Exception as ex:
                                # print(ex)
                                pass

                            for c in self.root.current_tab.content.children:
                                try:
                                    getattr(c, "{}".format(k))()
                                except Exception as ex:
                                    print(ex)

                            for lower_widget in self.root.current_tab.sub_content:
                                for c in lower_widget.children:
                                    try:
                                        getattr(c, "{}".format(k))()
                                    except Exception as ex:
                                        print(ex)
            except KeyError:
                pass

    @property
    def grid_hash(self):
        return hashlib.sha1("".join(self.files).encode()).hexdigest()

    def grid_thumbnail(self):
        self.grid.export_to_png(str(pathlib.PurePath(self.data_dir, "{}.png".format(self.grid_hash))))

    def grid_save(self):
        root = etree.Element("grid")
        for order, child in enumerate(self.grid.children):
            cell = etree.Element("cell")
            cell.set("source", child.source)
            cell.set("source_type", child.source_type)
            # fov
            cell.set("scroll_x", str(child.scroll_x))
            cell.set("scroll_y", str(child.scroll_y))
            cell.set("position", str(order))
            # zoom / fontsize

            root.append(cell)
        # save to file
        et = etree.ElementTree(root)
        file = str(pathlib.PurePath(self.data_dir, "{}.xml".format(self.grid_hash)))
        et.write(file, pretty_print=True)

    def grid_load(self, file):
        parser = etree.XMLParser()
        file_tree = etree.parse(file, parser)
        file_root = file_tree.getroot()
        cells = []
        for element in file_root.iter("cell"):
            if isinstance(element.tag, str):
                # insert into list to use position when adding widgets
                cells.insert(int(element.attrib["position"]),
                                    TxtPixel(source=element.attrib["source"],
                                             source_type=element.attrib["source_type"],
                                             scroll_x=element.attrib["scroll_x"],
                                             scroll_y=element.attrib["scroll_y"])
                                    )
        self.grid.rows = math.ceil(len(cells) / 2)
        self.grid.cols = math.ceil(len(cells) / 2)

        for cell in reversed(cells):
            self.grid.add_widget(cell)

    def app_exit(self):
        self.grid_thumbnail()
        self.grid_save()
        App.get_running_app().stop()

    def build(self):
        root = TabbedPanel(do_default_tab=False)
        self.root = root

        tab = TabItem(text="grid", root=root)
        tab.tab_name = "grid"
        # testing grid 2x2 with some 
        # filler content
        # could wrap in scrollview too...
        g = BgGridLayout(rows=math.ceil(len(self.files) / 2),
                       cols=math.ceil(len(self.files) / 2))
        self.grid = g
        for file in self.files:
            if file.endswith(".xml"):
                self.grid_load(file)
            else:
                self.grid.add_widget(TxtPixel(source=file, source_type="file"))

        tab.add_widget(g)
        root.add_widget(tab)

        bindings_container = BoxLayout(orientation="vertical",
                                       size_hint_y=None,
                                       )

        actions = 0
        for domain, domain_actions in self.actions.items():
            bindings_container.add_widget(Label(text=str(domain), height=40))
            for action, action_bindings in domain_actions.items():
                binding_widget = BindingItem(domain, action, action_bindings, self.actions, height=40)
                bindings_container.add_widget(binding_widget)
                actions += 1
        # set height for scrollview
        bindings_container.height = actions * 40
        bindings_scroll = ScrollView(bar_width=20)
        bindings_scroll.add_widget(bindings_container)

        tab = TabItem(text="bindings", root=root)
        tab.tab_name = "bindings"
        tab.add_widget(bindings_scroll)
        root.add_widget(tab)

        return root

def source_text(source=None, source_type=None):
    contents = ""
    if source_type == "file" and os.path.isfile(source):
        try:
            with open(source, "r") as f:
                contents = f.read()
        except TypeError:
                pass

    return contents

def main():
    files = []
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    files.extend(args.files)

    app = GridApp(files=files)
    app.run()

if __name__ == "__main__":
    main()
