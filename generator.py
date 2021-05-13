# Python libraries
import sys
import os
from pathlib import Path
# Image manipulation libraries
import layeredimage.io as li
from PIL import Image
# GUI libraries
from PySide6 import QtCore
from PySide6.QtWidgets import (QWidget, QApplication, QVBoxLayout, QHBoxLayout,
    QComboBox, QLabel, QPushButton, QMessageBox)
from PySide6.QtGui import QIcon, QPixmap

# Absolute path to the current folder as constant for easy access
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR))

def gather_layers():
    # Opens the .pdn file
    get_tablecloth = li.openLayer_PDN(THISDIR + "\\league_tablecloth.pdn")
    # Sets the team dictionary and start the counters
    teams = {}
    team_num = 0
    num_layers = 1
    # Get the three other layers
    sec_layers = get_tablecloth.layers[:3]
    # Ignores the first 3 layers since they are not needed
    layers = get_tablecloth.layers[3:]
    for layer in layers:
        if team_num == 14:
            break # Gotta find a better way to do this
        define_team = "TEAM_%d" % (team_num + 1)
        teams[define_team] = layers[team_num*4:num_layers*4]
        team_num += 1
        num_layers += 1
    
    return get_tablecloth, sec_layers, teams

class TableClothGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.MainUI()

    def MainUI(self):

        # Lists the teams
        self.teams = ["Riichi Dicks Inc.", "U.M.A.", "Riichima Financial",
            "CoolDogz", "Nyakuza", "Kani Kartel", "Ebola Bois",
            "A.U.T.I.S.M.", "Mahjong Musketeers", "天団", "Jantama Judgement",
            "Bandora Bandits", "Akochan's Acolytes", "Freed Jiangshis"]
        # Set up the GUI
        # Top (WEST)
        self.label_top = QLabel(self)
        self.label_top.setText("Top team (WEST)")
        self.label_top.setAlignment(QtCore.Qt.AlignCenter)
        self.image_top = QLabel(self)
        self.image_top.setPixmap(QPixmap("logos/team1.png").scaled(100,100))
        self.image_top.setAlignment(QtCore.Qt.AlignCenter)
        self.image_top.show()
        self.cloth_top = QComboBox()
        self.cloth_top.addItems(self.teams)
        self.cloth_top.activated.connect(
            lambda: self.switchImage(self.cloth_top, self.image_top))
        # Left (NORTH)
        self.label_left = QLabel(self)
        self.label_left.setText("Left team (NORTH)")
        self.label_left.setAlignment(QtCore.Qt.AlignCenter)
        self.image_left = QLabel(self)
        self.image_left.setPixmap(QPixmap("logos/team1.png").scaled(100,100))
        self.image_left.setAlignment(QtCore.Qt.AlignCenter)
        self.image_left.show()
        self.cloth_left = QComboBox()
        self.cloth_left.addItems(self.teams)
        self.cloth_left.activated.connect(
            lambda: self.switchImage(self.cloth_left, self.image_left))
        # Right (SOUTH)
        self.label_right = QLabel(self)
        self.label_right.setText("Right team (SOUTH)")
        self.label_right.setAlignment(QtCore.Qt.AlignCenter)
        self.image_right = QLabel(self)
        self.image_right.setPixmap(QPixmap("logos/team1.png").scaled(100,100))
        self.image_right.setAlignment(QtCore.Qt.AlignCenter)
        self.image_right.show()
        self.cloth_right = QComboBox()
        self.cloth_right.addItems(self.teams)
        self.cloth_right.activated.connect(
            lambda: self.switchImage(self.cloth_right, self.image_right))
        # Bottom (EAST)
        self.label_bottom = QLabel(self)
        self.label_bottom.setText("Bottom team (EAST)")
        self.label_bottom.setAlignment(QtCore.Qt.AlignCenter)
        self.image_bottom = QLabel(self)
        self.image_bottom.setPixmap(QPixmap("logos/team1.png").scaled(100,100))
        self.image_bottom.setAlignment(QtCore.Qt.AlignCenter)
        self.image_bottom.show()
        self.cloth_bottom = QComboBox()
        self.cloth_bottom.addItems(self.teams)
        self.cloth_bottom.activated.connect(
            lambda: self.switchImage(self.cloth_bottom, self.image_bottom))
        # Generate button
        self.generate = QPushButton(self)
        self.generate.setText("Generate Tablecloth")
        self.generate.clicked.connect(self.generateImage)

        # Create the layout
        hbox = QHBoxLayout(self)
        vbox1 = QVBoxLayout(self)
        vbox2 = QVBoxLayout(self)
        vbox1.setAlignment(QtCore.Qt.AlignCenter)
        vbox2.setAlignment(QtCore.Qt.AlignCenter)
        # Vertical layout (Top, Left)
        vbox1.addWidget(self.label_top)
        vbox1.addWidget(self.image_top)
        vbox1.addWidget(self.cloth_top)
        vbox1.addWidget(self.label_left)
        vbox1.addWidget(self.image_left)
        vbox1.addWidget(self.cloth_left)
        # Vertical layout 2 (Right, Bottom)
        vbox2.addWidget(self.label_right)
        vbox2.addWidget(self.image_right)
        vbox2.addWidget(self.cloth_right)
        vbox2.addWidget(self.label_bottom)
        vbox2.addWidget(self.image_bottom)
        vbox2.addWidget(self.cloth_bottom)
        # Add the layouts to be show
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        # Add the generate button
        hbox.addWidget(self.generate)

        # Create the window
        self.resize(200, 300)
        self.setWindowTitle('Tablecloth Generator')
        self.setWindowIcon(QIcon('icon.ico'))

        self.show()

    def switchImage(self, cloth, image):
        team_id = cloth.currentIndex() + 1
        image.setPixmap(QPixmap(
            "logos/team%d.png" % team_id).scaled(100,100))

    def waitingDialog(self):
        mbox = QMessageBox()

        mbox.setWindowTitle("Tablecloth Generator")
        mbox.setText("Generating Tablecloth...")
        mbox.setStandardButtons(QMessageBox.Ok)

        mbox.exec()

    def GeneratedDialog(self):
        mbox = QMessageBox()

        mbox.setWindowTitle("Tablecloth Generator")
        mbox.setText("Tablecloth Generated!")
        mbox.setStandardButtons(QMessageBox.Ok)

        mbox.exec()

    def generateImage(self):
        self.waitingDialog()

        # Brings all the .pdn data
        tablecloth, sec_layers, teams_layers = gather_layers()
        # Makes the top image visible
        top_id = self.cloth_top.currentIndex() + 1
        teams_layers["TEAM_%d" % top_id][1].visible = True
        # Makes the left image visible
        left_id = self.cloth_left.currentIndex() + 1
        teams_layers["TEAM_%d" % left_id][0].visible = True
        # Makes the right image visible
        right_id = self.cloth_right.currentIndex() + 1
        teams_layers["TEAM_%d" % right_id][2].visible = True
        # Makes the bottom image visible
        bottom_id = self.cloth_bottom.currentIndex() + 1
        teams_layers["TEAM_%d" % bottom_id][3].visible = True
        # Compiles all the layers
        layers = []
        # Append all the non-team layers
        for sl in sec_layers:
            layers.append(sl)
        # Now append all the team layers
        for lt in teams_layers.values():
                for il in lt:
                    layers.append(il)

        tablecloth.layers = layers

        # Let's check the file does not exist first
        if os.path.exists(THISDIR+"/Table_Dif.jpg"):
            os.remove(THISDIR+"/Table_Dif.jpg")
        # This is really annoying but thus far the only "easy way"
        # To create the image is to convert it to .png, open it,
        # remove the alpha channel and then save it as .jpg
        tablecloth.getFlattenLayers().save(THISDIR+"/Table_Dif.png")
        new_jpg = Image.open(THISDIR+"/Table_Dif.png")
        final_tablecloth = new_jpg.convert("RGB")
        final_tablecloth.save(THISDIR+"/Table_Dif.jpg")
        # We finally remove the .png since it's useless
        os.remove(THISDIR+"/Table_Dif.png")
        # If it exists, it means that the process was successful
        if os.path.exists(THISDIR+"/Table_Dif.jpg"):
            self.GeneratedDialog()


def main():

    app = QApplication(sys.argv)
    app.setStyle("Material")
    ex = TableClothGenerator()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
