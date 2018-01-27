"""Common utils for notebooks."""
import os
import ipywidgets as widgets
from IPython.display import display, Javascript


def selectdata(directory="/tmp/datavmware"):
    explorers = []
    if os.path.isdir(directory):
        for f in os.listdir(directory):
            if f.startswith("RVTools_"):
                if os.path.isdir(os.path.join(directory, f)):
                    explorers.append(os.path.join(directory, f))
    return explorers


def run_all_below(ev):
    display(Javascript('IPython.notebook.execute_cells_below()'))


class ExplorersSelection(object):
    """Browse path to search csv files."""
    def __init__(self, csvname ,explorers):
        self.csvname = csvname
        self.explorers = sorted([os.path.join(explorer, self.csvname) for explorer in explorers ])
        self._selected_explorer = None
        self._update_selected()


    def _update_selected(self):
        self._selected_explorer = self._selected_explorer

    def widget(self):
        box = widgets.VBox()
        self._update(box)
        return box

    @property
    def selected_explorers(self):
        return self._selected_explorer

    @selected_explorers.setter
    def selected_explorers(self, value):
        self._selected_explorer = value

    def _update(self, box):

        def on_click(b):
            """Update files and box for buttons."""
            if b.description == self._selected_explorer:
                self._selected_explorer = None
            else:
                if not self._selected_explorer:
                    self._selected_explorer = b.description
            self._update_selected()
            self._update(box)

        buttons = []
        for f in self.explorers:
            button = widgets.Button(description=f, button_style='primary',
                                    layout=widgets.Layout(min_width='70%', height='25px'))
            button.on_click(on_click)
            buttons.append(button)
        box.children = tuple([widgets.HTML("<h4>%s</h4>" % (self._selected_explorer,))] + buttons)


def human_size(nbytes):
    """Just a function to change sizes to human readable for return values."""

    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
