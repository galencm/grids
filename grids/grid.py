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
from kivy.graphics import Color
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from grids import bindings

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

class TxtPixel(ScrollView):
    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self.is_mouse_over)
        self.mouse_above = False
        self.container = None
        self.font_increment = 2
        self.scroll_increment = 0.1
        super(TxtPixel , self).__init__(**kwargs)
        container_height = 4000
        container_width = 4000
        filler_height = 2000
        filler_width = 2000
        grid_container = FloatLayout(
                                   size_hint_y=None,
                                   size_hint_x=None
                                   )
        filler = Label(text=file_text(), size=(filler_width, filler_height))
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

    def app_exit(self):
        App.get_running_app().stop()

    def build(self):
        root = TabbedPanel(do_default_tab=False)
        self.root = root

        tab = TabItem(text="grid", root=root)
        tab.tab_name = "grid"
        # testing grid 2x2 with some 
        # filler content
        # could wrap in scrollview too...
        g = GridLayout(rows=2, cols=2)
        g.add_widget(TxtPixel())
        g.add_widget(TxtPixel())
        g.add_widget(TxtPixel())
        g.add_widget(TxtPixel())
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

def file_text(file=None, pad_lines=0):
    contents = ""

    try:
        with open(file, "r") as f:
            contents = f.read()
    except TypeError:
            pass

    if pad_lines:
        longest_line = len(max(contents.split("\n")))
        for _ in range(pad_lines):
            contents += "{}\n".format("_" * longest_line)

    return contents

def main():
    app = GridApp()
    app.run()

if __name__ == "__main__":
    main()
