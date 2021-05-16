# Python libraries
import sys
import os
from pathlib import Path
# The __debug__ lines are ignored in the compilation
if __debug__:
    from timeit import default_timer as timer
# Image manipulation libraries
import layeredimage.io as li
from PIL import Image
# GUI libraries
from PySide6 import QtCore
from PySide6.QtWidgets import (QWidget, QMainWindow, QApplication, QVBoxLayout,
    QHBoxLayout, QComboBox, QLabel, QPushButton, QMessageBox, QCheckBox,
    QProgressBar, QSplashScreen)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QObject, QRunnable, Qt, QThread, QThreadPool, Signal

# Absolute path to the current folder as constant for easy access
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR))

class Worker(QObject):
    finished = Signal()
    update_progress = Signal(int)

    def __init__(self, tablecloth, sec_layers, teams_layers, top_id, left_id,
      right_id, bottom_id, technical_lines=False, parent=None):
        super().__init__()
        self.tablecloth = tablecloth
        self.sec_layers = sec_layers
        self.teams_layers = teams_layers
        self.top_id = top_id
        self.left_id = left_id
        self.right_id = right_id
        self.bottom_id = bottom_id
        self.technical_lines = technical_lines

    def run(self):
        # Compiles all the layers
        if __debug__:
            start = timer()
        layers = []
        # Make technical lines visible
        if self.technical_lines:
            self.sec_layers[2].visible = True
        # Append all the non-team layers
        for sl in self.sec_layers:
            layers.append(sl)
        self.update_progress.emit(10)

        # Makes the top image visible
        self.top_id += 1
        self.teams_layers["TEAM_%d" % self.top_id][1].visible = True
        layers.append(self.teams_layers["TEAM_%d" % self.top_id][1])
        # Makes the left image visible
        self.left_id += 1
        self.teams_layers["TEAM_%d" % self.left_id][0].visible = True
        layers.append(self.teams_layers["TEAM_%d" % self.left_id][0])
        # Makes the right image visible
        self.right_id += 1
        self.teams_layers["TEAM_%d" % self.right_id][2].visible = True
        layers.append(self.teams_layers["TEAM_%d" % self.right_id])
        # Makes the bottom image visible
        self.bottom_id += 1
        self.teams_layers["TEAM_%d" % self.bottom_id][3].visible = True
        layers.append(self.teams_layers["TEAM_%d" % self.bottom_id][3])

        self.tablecloth.layers = layers

        self.update_progress.emit(40)

        # Let's check the file does not exist first
        if os.path.exists(THISDIR+"/Table_Dif.jpg"):
            os.remove(THISDIR+"/Table_Dif.jpg")

        self.update_progress.emit(50)
        # This is really annoying but thus far the only "easy way"
        # To create the image is to convert it to .png, open it,
        # remove the alpha channel and then save it as .jpg
        self.tablecloth.getFlattenLayers().save(THISDIR+"/Table_Dif.png")
        new_jpg = Image.open(THISDIR+"/Table_Dif.png")
        self.update_progress.emit(75)
        final_tablecloth = new_jpg.convert("RGB")
        final_tablecloth.save(THISDIR+"/Table_Dif.jpg")
        self.update_progress.emit(90)
        # We finally remove the .png since it's useless
        os.remove(THISDIR+"/Table_Dif.png")
        # If it exists, it means that the process was successful
        if os.path.exists(THISDIR+"/Table_Dif.jpg"):
            if __debug__:
                end = timer()
                print("This took %d seconds." % (end - start))
            self.update_progress.emit(100)
            self.finished.emit()

class TableClothGenerator(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)

        # Main UI settings
        self.setWindowTitle('Tablecloth Generator')
        self.setWindowIcon(QIcon('icon.ico'))
        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)
        self.resize(350, 350)

        self.MainUI()

    def MainUI(self):

        # Loading this big ass file at the start to save time
        self.tablecloth = li.openLayer_PDN(THISDIR + "\\league_tablecloth.pdn")
        # Sets the team dictionary and start the counters
        self.teams_layers = {}
        # It goes backwards
        team_ids = 15
        team_num = 0
        num_layers = 1
        # Get the three other layers
        self.sec_layers = self.tablecloth.layers[:3]
        # Ignores the first 3 layers since they are not needed
        layers = self.tablecloth.layers[3:]
        for layer in layers:
            if team_ids == 1:
                break # Gotta find a better way to do this
            define_team = "TEAM_%d" % (team_ids - 1)
            self.teams_layers[define_team] = layers[team_num*4:num_layers*4]
            team_ids -= 1
            team_num += 1
            num_layers += 1

        # Lists the teams
        self.teams = ["Riichi Dicks Inc.", "U.M.A.", "Riichima Financial",
            "CoolDogz", "Nyakuza", "Kani Kartel", "Ebola Bois",
            "A.U.T.I.S.M.", "Mahjong Musketeers", "天団", "Jantama Judgement",
            "Bandora Bandits", "Akochan's Acolytes", "Freed Jiangshis"]
        # Set up the GUI
        self.statusBar().showMessage("Remember: Rig responsibly.")
        # Bottom (EAST)
        self.label_east = QLabel(self)
        self.label_east.setText("Bottom team (EAST)")
        self.label_east.setAlignment(QtCore.Qt.AlignCenter)
        self.image_east = QLabel(self)
        self.image_east.setPixmap(QPixmap("logos/team1.png").scaled(100,100))
        self.image_east.setAlignment(QtCore.Qt.AlignCenter)
        self.image_east.show()
        self.cloth_east = QComboBox()
        self.cloth_east.addItems(self.teams)
        self.cloth_east.activated.connect(
            lambda: self.switchImage(self.cloth_east, self.image_east))
        # Right (SOUTH)
        self.label_south = QLabel(self)
        self.label_south.setText("Right team (SOUTH)")
        self.label_south.setAlignment(QtCore.Qt.AlignCenter)
        self.image_south = QLabel(self)
        self.image_south.setPixmap(QPixmap("logos/team1.png").scaled(100,100))
        self.image_south.setAlignment(QtCore.Qt.AlignCenter)
        self.image_south.show()
        self.cloth_south = QComboBox()
        self.cloth_south.addItems(self.teams)
        self.cloth_south.activated.connect(
            lambda: self.switchImage(self.cloth_south, self.image_south))
        # Top (WEST)
        self.label_west = QLabel(self)
        self.label_west.setText("Top team (WEST)")
        self.label_west.setAlignment(QtCore.Qt.AlignCenter)
        self.image_west = QLabel(self)
        self.image_west.setPixmap(QPixmap("logos/team1.png").scaled(100,100))
        self.image_west.setAlignment(QtCore.Qt.AlignCenter)
        self.image_west.show()
        self.cloth_west = QComboBox()
        self.cloth_west.addItems(self.teams)
        self.cloth_west.activated.connect(
            lambda: self.switchImage(self.cloth_west, self.image_west))
        # Left (NORTH)
        self.label_north = QLabel(self)
        self.label_north.setText("Left team (NORTH)")
        self.label_north.setAlignment(QtCore.Qt.AlignCenter)
        self.image_north = QLabel(self)
        self.image_north.setPixmap(QPixmap("logos/team1.png").scaled(100,100))
        self.image_north.setAlignment(QtCore.Qt.AlignCenter)
        self.image_north.show()
        self.cloth_north = QComboBox()
        self.cloth_north.addItems(self.teams)
        self.cloth_north.activated.connect(
            lambda: self.switchImage(self.cloth_north, self.image_north))
        # Technical lines
        self.technical_lines = QCheckBox("Show Technical lines", self)
        # Generate button
        self.generate = QPushButton(self)
        self.generate.setText("Generate Tablecloth")
        self.generate.clicked.connect(self.ConfirmDialog)

        # Create the layout
        hbox = QHBoxLayout(self)
        self.setLayout(hbox)
        vbox1 = QVBoxLayout(self)
        self.setLayout(vbox1)
        vbox2 = QVBoxLayout(self)
        self.setLayout(vbox2)
        vbox1.setAlignment(QtCore.Qt.AlignCenter)
        vbox2.setAlignment(QtCore.Qt.AlignCenter)
        # Vertical layout (Bottom, right)
        vbox1.addWidget(self.label_east)
        vbox1.addWidget(self.image_east)
        vbox1.addWidget(self.cloth_east)
        vbox1.addWidget(self.label_south)
        vbox1.addWidget(self.image_south)
        vbox1.addWidget(self.cloth_south)
        # Add the option for technical lines
        vbox1.addWidget(self.technical_lines)
        # Vertical layout 2 (Top, left)
        vbox2.addWidget(self.label_west)
        vbox2.addWidget(self.image_west)
        vbox2.addWidget(self.cloth_west)
        vbox2.addWidget(self.label_north)
        vbox2.addWidget(self.image_north)
        vbox2.addWidget(self.cloth_north)
        # Add the generate button
        vbox2.addWidget(self.generate)
        # Add the layouts to be show
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        self.centralWidget.setLayout(hbox)

        # Create the window
        self.show()

    def switchImage(self, cloth, image):
        # It shows you the team logo. No way you can miss those, right?
        team_id = cloth.currentIndex() + 1
        image.setPixmap(QPixmap(
            "logos/team%d.png" % team_id).scaled(100,100))

    def ConfirmDialog(self):
        # Double check for double idiots
        mbox = QMessageBox()

        mbox.setWindowTitle("Tablecloth Generator")
        mbox.setText("Confirm your selection:")
        mbox.setInformativeText("<strong>East:</strong> %s<br> \
            <strong>South:</strong> %s <br> <strong>West:</strong> %s<br> \
            <strong>North:</strong> %s %s" %
            (self.cloth_east.currentText(), self.cloth_south.currentText(),
             self.cloth_west.currentText(), self.cloth_north.currentText(),
             "<br><b>Technical Lines enabled.</b>" if self.technical_lines\
             .isChecked() else ""))
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        result = mbox.exec()
        if result == QMessageBox.Ok:
            # Freeze the program to avoid a dumbass clicking several times
            # and crashing
            self.statusBar().showMessage('Generating image...')
            self.progress_bar = QProgressBar()
            self.progress_bar.minimum = 0
            self.progress_bar.maximum = 100
            self.progress_bar.setValue(0)
            self.progress_bar.setTextVisible(False)
            self.progress_bar.setGeometry(50, 50, 10, 10)
            self.progress_bar.setAlignment(QtCore.Qt.AlignRight)
            self.progress_bar.adjustSize()
            self.statusBar().addPermanentWidget(self.progress_bar)
            self.cloth_east.setEnabled(False)
            self.cloth_south.setEnabled(False)
            self.cloth_west.setEnabled(False)
            self.cloth_north.setEnabled(False)
            self.generate.setEnabled(False)
            # Confirm and go directly to generate the image.
            self.generateImage()

    def GeneratedDialog(self):

        self.statusBar().showMessage('Tablecloth generated. Happy rigging!')
        self.statusBar().removeWidget(self.progress_bar)
        # Now you can go back to rigging
        self.cloth_east.setEnabled(True)
        self.cloth_south.setEnabled(True)
        self.cloth_west.setEnabled(True)
        self.cloth_north.setEnabled(True)
        self.generate.setEnabled(True)

        mbox = QMessageBox()

        mbox.setWindowTitle("Tablecloth Generator")
        mbox.setText("Tablecloth Generated!")
        mbox.setStandardButtons(QMessageBox.Ok)

        mbox.exec()

    def UpdateStatus(self, status):
        self.progress_bar.setValue(status)

    def generateImage(self):

        self.thread = QThread()
        self.worker = Worker(self.tablecloth, self.sec_layers,
           self.teams_layers, self.cloth_west.currentIndex(),
           self.cloth_south.currentIndex(), self.cloth_north.currentIndex(),
           self.cloth_east.currentIndex(), self.technical_lines.isChecked())
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.update_progress.connect(self.UpdateStatus)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.GeneratedDialog)
        self.thread.start()

def main():

    app = QApplication(sys.argv)
    pixmap = QPixmap("icon.ico")
    splash = QSplashScreen(pixmap)
    splash.show()
    if __debug__:
        start = timer()
    ex = TableClothGenerator()
    app.processEvents()
    ex.show()
    splash.finish(ex)
    if __debug__:
        end = timer()
        print("This took %d seconds." % (end - start))
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
