"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from time import sleep
from typing import TYPE_CHECKING
from magicgui import magic_factory
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

if TYPE_CHECKING:
    import napari

# class ExampleQWidget(QWidget):
#     # your QWidget.__init__ can optionally request the napari viewer instance
#     # in one of two ways:
#     # 1. use a parameter called `napari_viewer`, as done here
#     # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
#     def __init__(self, napari_viewer):
#         super().__init__()
#         self.viewer = napari_viewer

#         btn = QPushButton("Click me!")
#         btn.clicked.connect(self._on_click)

#         self.setLayout(QHBoxLayout())
#         self.layout().addWidget(btn)

#     def _on_click(self):
#         print("napari has", len(self.viewer.layers), "layers")


# @magic_factory
# def example_magic_widget(img_layer: "napari.layers.Image"):
#     print(f"you have selected {img_layer}")


# @napari_hook_implementation
# def napari_experimental_provide_dock_widget():
#     # you can return either a single widget, or a sequence of widgets
#     return [ExampleQWidget, example_magic_widget]

def widget_wrapper():
    """Wrap a QWidget to make compatible with napari threading."""
    from napari.qt.threading import thread_worker

    class ExampleQWidget(QWidget):
        def __init__(self, viewer: 'napari.viewer.Viewer') -> None:
            super().__init__()
            self.clicksCount = 0
            self.setupUi()

        def setupUi(self):
            # Create and connect widgets
            self.clicksLabel = QLabel("Counting: 0 clicks", self)
            # self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.stepLabel = QLabel("Long-Running Step: 0")
            # self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.countBtn = QPushButton("Click me!", self)
            self.countBtn.clicked.connect(self.countClicks)
            self.longRunningBtn = QPushButton("Long-Running Task!", self)
            # self.longRunningBtn.clicked.connect(self.runLongTask)
            self.longRunningBtn.clicked.connect(self.runLongTask)
            # Set the layout
            layout = QVBoxLayout()
            self.setLayout(layout)
            layout.addWidget(self.clicksLabel)
            layout.addWidget(self.countBtn)
            layout.addStretch()
            layout.addWidget(self.stepLabel)
            layout.addWidget(self.longRunningBtn)
            layout.addWidget(self.pbar)

        def countClicks(self):
            self.clicksCount += 1
            self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

        def reportProgress(self, n):
            self.stepLabel.setText(f"Long-Running Step: {n}")

        @thread_worker(start_thread=True)
        def runLongTask(self, event):
            """Long-running task in 5 steps."""
            for i in range(5):
                sleep(1)
                self.reportProgress(i + 1)

    return RealPythonExample


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return widget_wrapper()
