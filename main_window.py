# improt libs -> the window and 3D rendering (gotta handle mri nii.gz lol)
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
import nibabel as nib  # nii.gz file manager. we hope it works!
import numpy as np

from gl_widget import GLWidget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("BrainyFly - Fly through brain! - MRI flyaround lol")
        self.setGeometry(100, 100, 800, 600)  # not too big

        # Layouts and labels (labels r fun)
        self.label = QLabel('Load MRI (nii.gz) to fly')
        self.label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        # Opengl part insert here
        self.gl_widget = GLWidget(self)
        layout.addWidget(self.gl_widget)

        # Container
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Menu for file loading (it should werk!)
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QtWidgets.QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

    def open_file(self):
        # file dilaog to get MRI file -> is this right? idk :/
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open MRI File", "", "Nii.gz Files (*.nii.gz);;All Files (*)", options=options)

        if file_name:  # check if file chosen
            self.label.setText(f'Loaded: {file_name}')  # telling user we got it
            self.load_mri(file_name)

    def load_mri(self, file_name):
        # loading MRI (hope it's nii.gz otherwise it dies lol)
        mri_img = nib.load(file_name)
        self.mri_data = mri_img.get_fdata()  # woo MRI data! it's numpy now
        self.gl_widget.set_mri_data(self.mri_data)

# run app
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  # app.run but in qt world
