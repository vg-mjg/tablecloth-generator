# Python libraries
import sys
import os
import json
import tempfile
import webbrowser
import urllib.request
from pathlib import Path

from zipfile import ZipFile, is_zipfile
# The __debug__ lines are ignored in the compilation
if __debug__:
    from timeit import default_timer as timer
# Image manipulation libraries
from PIL import Image
# GUI libraries
from PySide6 import QtCore
from PySide6.QtWidgets import (QWidget, QMainWindow, QApplication, QVBoxLayout,
    QHBoxLayout, QComboBox, QLabel, QPushButton, QMessageBox, QCheckBox,
    QProgressBar, QSplashScreen, QCompleter, QLineEdit, QFileDialog,
    QGridLayout, QMenu, QMenuBar, QListWidget)
from PySide6.QtGui import QIcon, QPixmap, QScreen
from PySide6.QtCore import QThread
# Custom libraries
from thread import GenerateImageThread
from widgets import EditionWidget

# Absolute path to the current folder as constant for easy access
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR))

VERSION = "v1.0"


class TableClothGenerator(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)

        # Main UI settings
        self.setWindowTitle('Tablecloth Generator')
        self.setWindowIcon(QIcon('icon.ico'))
        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)
        self.resize(350, 350)
        self.center()

        self._createMenuBar()

        self.MainUI()

    def MainUI(self):

        # Obtain the configs
        fp_config = open(THISDIR + "\\config\\config.json", "r",
                            encoding="utf-8")
        self.config = json.loads(fp_config.read())
        fp_config.close()

        # Obtain and List the teams
        fp_teams = open(THISDIR + "\\config\\teams.json", "r",
                            encoding="utf-8")
        conf_teams = json.loads(fp_teams.read())
        fp_teams.close()
        self.teams = conf_teams["teams"]
        self.players = conf_teams["players"]

        # Obtain all images needed to create the tablecloth
        self.background = Image.open(THISDIR + "\\images\\mat.png")
        self.table_border = Image.open(THISDIR + "\\images\\table_border.png")
        self.tech_lines = Image.open(THISDIR + "\\images\\technical_lines.png")

        # Check if there's no configuration set up
        # and prompt to create/import one
        if self.config["total_teams"] == 0:
            no_config = QMessageBox()
            no_config.setWindowTitle("No configuration")
            no_config.setText("No configuration has been found."\
                " Do you wish to set up a new one?")
            no_config.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            new_config = no_config.exec()

            if new_config == QMessageBox.Yes:
                self.CreateTeamsWindow()

        self.bg_image = self.config["image_route"]
        self.players_combobox = QComboBox()
        self.UpdatePlayersList()
        self.players_combobox.setEditable(True)
        self.players_combobox.completer()\
                             .setCompletionMode(QCompleter.PopupCompletion)
        self.players_combobox.setInsertPolicy(QComboBox.NoInsert)

        # Set up the GUI
        self.statusBar().showMessage("Remember: Rig responsibly.")
        # Bottom (EAST)
        self.label_east = QLabel(self)
        self.label_east.setText("<h1>East Seat</h1>")
        self.label_east.setAlignment(QtCore.Qt.AlignCenter)
        self.image_east = QLabel(self)
        self.image_east.setPixmap(QPixmap("images/logos/team1.png")\
                                  .scaled(100,100))
        self.image_east.setAlignment(QtCore.Qt.AlignCenter)
        self.search_east = QLineEdit()
        self.search_east.setAlignment(QtCore.Qt.AlignCenter)
        self.search_east.editingFinished.connect(
            lambda: self.searchPlayer(self.search_east.text(),
                                      self.cloth_east))
        self.cloth_east = QComboBox()
        self.cloth_east.setModel(self.players_combobox.model())
        self.cloth_east.currentIndexChanged.connect(
            lambda: self.SwitchImage(self.cloth_east, self.image_east))
        # Right (SOUTH)
        self.label_south = QLabel(self)
        self.label_south.setText("<h1>South Seat</h1>")
        self.label_south.setAlignment(QtCore.Qt.AlignCenter)
        self.image_south = QLabel(self)
        self.image_south.setPixmap(QPixmap("images/logos/team1.png")\
                                   .scaled(100,100))
        self.image_south.setAlignment(QtCore.Qt.AlignCenter)
        self.image_south.show()
        self.search_south = QLineEdit()
        self.search_south.setAlignment(QtCore.Qt.AlignCenter)
        self.search_south.editingFinished.connect(
            lambda: self.searchPlayer(self.search_south.text(),
                                      self.cloth_south))
        self.cloth_south = QComboBox()
        self.cloth_south.setModel(self.players_combobox.model())
        self.cloth_south.currentIndexChanged.connect(
            lambda: self.SwitchImage(self.cloth_south, self.image_south))
        # Top (WEST)
        self.label_west = QLabel(self)
        self.label_west.setText("<h1>West Seat</h1>")
        self.label_west.setAlignment(QtCore.Qt.AlignCenter)
        self.image_west = QLabel(self)
        self.image_west.setPixmap(QPixmap("images/logos/team1.png")\
                                  .scaled(100,100))
        self.image_west.setAlignment(QtCore.Qt.AlignCenter)
        self.image_west.show()
        self.cloth_west = QComboBox()
        self.search_west = QLineEdit()
        self.search_west.setAlignment(QtCore.Qt.AlignCenter)
        self.search_west.editingFinished.connect(
            lambda: self.searchPlayer(self.search_west.text(),
                                      self.cloth_west))
        self.cloth_west.setModel(self.players_combobox.model())
        self.cloth_west.currentIndexChanged.connect(
            lambda: self.SwitchImage(self.cloth_west, self.image_west))
        # Left (NORTH)
        self.label_north = QLabel(self)
        self.label_north.setText("<h1>North Seat</h1>")
        self.label_north.setAlignment(QtCore.Qt.AlignCenter)
        self.image_north = QLabel(self)
        self.image_north.setPixmap(QPixmap("images/logos/team1.png")\
                                   .scaled(100,100))
        self.image_north.setAlignment(QtCore.Qt.AlignCenter)
        self.image_north.show()
        self.cloth_north = QComboBox()
        self.search_north = QLineEdit()
        self.search_north.setAlignment(QtCore.Qt.AlignCenter)
        self.search_north.editingFinished.connect(
            lambda: self.searchPlayer(self.search_north.text(),
                                      self.cloth_north))
        self.cloth_north.setModel(self.players_combobox.model())
        self.cloth_north.currentIndexChanged.connect(
            lambda: self.SwitchImage(self.cloth_north, self.image_north))
        # Technical lines
        self.technical_lines = QCheckBox("Show Technical lines", self)
        # Generate button
        self.generate = QPushButton(self)
        self.generate.setText("Generate Tablecloth")
        self.generate.clicked.connect(self.GeneratePreview)
        # Add custom mat
        self.custom_mat = QPushButton(self)
        self.custom_mat.setText("Add Mat")
        self.custom_mat.clicked.connect(self.MatDialog)

        # Create the layout
        grid_layout = QGridLayout()
        grid_layout.setAlignment(QtCore.Qt.AlignCenter)
        grid_layout.setAlignment(QtCore.Qt.AlignTop)
        # Labels East, West
        grid_layout.addWidget(self.label_east, 1, 1)
        grid_layout.addWidget(self.label_west, 1, 2)
        # Image preview East, West
        grid_layout.addWidget(self.image_east, 2, 1)
        grid_layout.addWidget(self.image_west, 2, 2)
        # Search player East, West
        grid_layout.addWidget(self.search_east, 3, 1)
        grid_layout.addWidget(self.search_west, 3, 2)
        # Player combobox East, West
        grid_layout.addWidget(self.cloth_east, 4, 1)
        grid_layout.addWidget(self.cloth_west, 4, 2)
        # Labes South, North
        grid_layout.addWidget(self.label_south, 5, 1)
        grid_layout.addWidget(self.label_north, 5, 2)
        # Image preview South, North
        grid_layout.addWidget(self.image_south, 6, 1)
        grid_layout.addWidget(self.image_north, 6, 2)
        # Search player South, North
        grid_layout.addWidget(self.search_south, 7, 1)
        grid_layout.addWidget(self.search_north, 7, 2)
        # Player combobox South, North
        grid_layout.addWidget(self.cloth_south, 8, 1)
        grid_layout.addWidget(self.cloth_north, 8, 2)
        # Technical lines
        grid_layout.addWidget(self.technical_lines, 9, 1)
        # Custom mat/bg
        grid_layout.addWidget(self.custom_mat, 10, 1)
        # Generate
        grid_layout.addWidget(self.generate, 10, 2)

        self.centralWidget.setLayout(grid_layout)

        # Create the window
        self.show()

    def _createMenuBar(self):

        # Settings and stuff for the toolbar
        menubar = QMenuBar(self)

        file_menu = QMenu("&File", self)
        file_menu.addAction("Create Team(s)", self.CreateTeamsWindow)
        file_menu.addAction("Edit Team(s)", self.EditTeamsWindow)
        file_menu.addAction("Exit", self.close)
        settings_menu = QMenu("&Settings", self)
        settings_menu.addAction("Version", self.SeeVersion)
        settings_menu.addAction("Help", self.GetHelp)

        menubar.addMenu(file_menu)
        menubar.addMenu(settings_menu)

        self.setMenuBar(menubar)

    def _createProgressBar(self):

        self.progress_bar = QProgressBar()
        self.progress_bar.minimum = 0
        self.progress_bar.maximum = 100
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setGeometry(50, 50, 10, 10)
        self.progress_bar.setAlignment(QtCore.Qt.AlignRight)
        self.progress_bar.adjustSize()
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.ChangeAppStatus(False)

    def SwitchImage(self, cloth, image):
        # It shows you the team logo. No way you can miss those, right?
        team_id = self.SearchTeamID(cloth, True)
        image.setPixmap(QPixmap(
            "images/logos/team%d.png" % team_id).scaled(100,100))

    def searchPlayer(self, text, combobox):
        # It even searches the player for you. What more could you want?
        search_index = combobox.findText(text, QtCore.Qt.MatchContains)
        if search_index == -1:
            QMessageBox.warning(self, "Error", "No player found")
        else:
            combobox.setCurrentIndex(search_index)

    def CreateTeamsWindow(self):

        self.teamcreation_wid = EditionWidget()
        self.teamcreation_wid.resize(400, 200)
        self.teamcreation_wid.setWindowTitle("First configuration")

        self.new_config = {}

        id_label = QLabel(self)
        id_label.setText("Team ID: ")
        self.num_id = QLabel(self)
        current_id = str(self.config["total_teams"] + 1)
        self.num_id.setText(current_id)
        name_label = QLabel(self)
        name_label.setText("Team Name:")
        name_label.setFocus()
        self.name_input = QLineEdit(self)
        members_label = QLabel(self)
        members_label.setText("Members (write and press enter):")
        members_input = QLineEdit(self)
        members_input.editingFinished.connect(
            lambda: self.AddMember(members_input))
        self.members_list = QListWidget(self)

        import_image = QPushButton(self)
        import_image.setText("Import Team Image")
        import_image.clicked.connect(self.ImportTeamImage)

        add_team = QPushButton(self)
        add_team.setText("Add Team")
        add_team.clicked.connect(
            lambda: self.addTeamFunction(self.name_input.text(),
                self.members_list))
        import_config = QPushButton(self)
        import_config.setText("Import configuration")
        import_config.clicked.connect(self.importTeamFunction)

        config_lay = QGridLayout()
        config_lay.addWidget(id_label, 1, 0)
        config_lay.addWidget(self.num_id, 1, 1)
        config_lay.addWidget(name_label, 2, 0)
        config_lay.addWidget(self.name_input, 2, 1)
        config_lay.addWidget(members_label, 3, 0)
        config_lay.addWidget(members_input, 3, 1)
        config_lay.addWidget(self.members_list, 4, 0, 2, 2)
        config_lay.addWidget(add_team, 6, 0)
        config_lay.addWidget(import_image, 6, 1)
        config_lay.addWidget(import_config, 7, 0, 1, 2)
        self.teamcreation_wid.setLayout(config_lay)

        self.teamcreation_wid.setWindowModality(QtCore.Qt.ApplicationModal)
        self.teamcreation_wid.activateWindow()
        self.teamcreation_wid.raise_()
        self.teamcreation_wid.show()

    def addTeamFunction(self, name, members):
        fp_teams = open(THISDIR + "\\config\\teams.json", "r",
                            encoding="utf-8")
        current_teams = json.loads(fp_teams.read())
        fp_teams.close()
        team = {}
        current_teams['teams'].append(name)
        current_teams['players'][name] = [members.itemText(i) for i in\
                                                        range(members.count())]
        new_team = open(THISDIR + "\\config\\teams.json", "w+",
                            encoding="utf-8")
        add_config = open(THISDIR + "\\config\\config.json", "w+",
                            encoding="utf-8")
        self.config["total_teams"] += 1
        new_id = self.config["total_teams"] + 1
        self.num_id.setText(str(new_id))
        add_config.write(json.dumps(self.config, indent=4))
        new_team.write(json.dumps(current_teams, indent=4))
        new_team.close()

        self.name_input.clear()

        self.members_list.clear()

    def ImportTeamImage(self):

        image_dialog = QFileDialog(self)
        image_dialog = QFileDialog.getOpenFileName(filter="Images (*.png)",
            selectedFilter="Images (*.png)")

        if image_dialog[0] != "":
            new_team_logo = Image.open(image_dialog[0]).convert("RGBA")
            if new_team_logo.size != (250, 250):
                new_team_logo.resize((250, 250))
            new_team_logo.save(THISDIR+"\\images\\logos\\team%s.png"\
                % self.num_id.text())

            QMessageBox.information(self, "Team Image", "Team image added.")

    def importTeamFunction(self):
        file_dialog = QFileDialog(self)
        file_dialog = QFileDialog.getOpenFileName(
                                    filter="Team Files (*.json *.zip)",
                                    selectedFilter="Team Files (*.json *.zip)")

        if file_dialog[0] != "":
            if is_zipfile(file_dialog[0]):
                with ZipFile(file_dialog[0]) as zip_import:
                    list_of_files = zip_import.namelist()
                    for fimp in list_of_files:
                        if fimp.startswith('logos'):
                            zip_import.extract(fimp, path=THISDIR+'\\images\\')
                    imported_teams = zip_import.read('teams.json')
                    imported_teams = imported_teams.decode('utf-8')
            else:
                imported_teams = open(file_dialog[0], "r",
                                encoding="utf-8").read()
            json_teams = json.loads(imported_teams)
            self.teams = json_teams["teams"]
            self.players = json_teams["players"]

            new_teams = open(THISDIR + "\\config\\teams.json", "w+",
                            encoding="utf-8")
            new_teams.write(json.dumps(json_teams, indent=4))
            new_teams.close()

            old_config = open(THISDIR + "\\config\\config.json", "r",
                                encoding="utf-8").read()
            old_config = json.loads(old_config)
            old_config["total_teams"] = len(json_teams["teams"])
            self.config = old_config
            new_config = open(THISDIR + "\\config\\config.json", "w+",
                                encoding="utf-8")
            new_config.write(json.dumps(self.config, indent=4))
            new_config.close()

            self.UpdatePlayersList()

            self.image_east.setPixmap(QPixmap("images/logos/team1.png")\
                                       .scaled(100,100))
            self.cloth_east.setModel(self.players_combobox.model())
            self.image_south.setPixmap(QPixmap("images/logos/team1.png")\
                                       .scaled(100,100))
            self.cloth_south.setModel(self.players_combobox.model())
            self.image_west.setPixmap(QPixmap("images/logos/team1.png")\
                                       .scaled(100,100))
            self.cloth_west.setModel(self.players_combobox.model())
            self.image_north.setPixmap(QPixmap("images/logos/team1.png")\
                                       .scaled(100,100))
            self.cloth_north.setModel(self.players_combobox.model())
            self.statusBar().showMessage("Teams imported successfully.")
            self.teamcreation_wid.close()


    def AddMember(self, member):
        self.members_list.addItem(member.text())
        member.clear()

    def EditTeamsWindow(self):

        self.teamedit_wid = EditionWidget()
        self.teamedit_wid.resize(400, 320)
        self.teamedit_wid.setWindowTitle("Edit Teams")

        self.teams_list = QComboBox(self)
        self.teams_list.addItem("--- Select a team ---")
        for team in self.teams:
            self.teams_list.addItem(team)
        self.teams_list.currentIndexChanged.connect(self.UpdateTeamInfo)

        team_id_label = QLabel(self)
        team_id_label.setText("Team ID: ")
        self.config_team_id = QLabel(self)
        team_name_label = QLabel(self)
        team_name_label.setText("Team name: ")
        self.config_team_name = QLabel(self)
        team_members_label = QLabel(self)
        team_members_label.setText("Team members: ")
        self.config_team_members = QListWidget(self)
        add_member_label = QLabel(self)
        add_member_label.setText("Add new member: ")
        add_member_input = QLineEdit(self)
        add_member_input.editingFinished.connect(self.AddNewMember)

        delete_member = QPushButton(self)
        delete_member.setText("Delete member")
        delete_member.clicked.connect(self.DeleteMember)
        delete_team = QPushButton(self)
        delete_team.setText("Delete Team")
        delete_team.clicked.connect(self.DeleteTeam)
        save_changes = QPushButton(self)
        save_changes.setText("Save changes")
        save_changes.clicked.connect(self.SaveEdits)

        config_lay = QGridLayout()
        config_lay.addWidget(self.teams_list, 1, 0)
        config_lay.addWidget(team_id_label, 2, 0)
        config_lay.addWidget(self.config_team_id, 2, 1)
        config_lay.addWidget(team_name_label, 3, 0)
        config_lay.addWidget(self.config_team_name, 3, 1, 1, 2)
        config_lay.addWidget(team_members_label, 4, 0)
        config_lay.addWidget(self.config_team_members, 5, 0)
        config_lay.addWidget(delete_member, 5, 1, 1, 2)
        config_lay.addWidget(add_member_label, 6, 0)
        config_lay.addWidget(add_member_input, 6, 1, 1, 2)
        config_lay.addWidget(delete_team, 7, 0)
        config_lay.addWidget(save_changes, 7, 1, 1, 2)

        self.teamedit_wid.setLayout(config_lay)
        self.teamedit_wid.setWindowModality(QtCore.Qt.ApplicationModal)
        self.teamedit_wid.activateWindow()
        self.teamedit_wid.raise_()
        self.teamedit_wid.show()

    def UpdateTeamInfo(self):

        sender = self.sender()
        if sender.currentIndex() > 0:
            team_id = sender.currentIndex()
            self.config_team_id.setText(str(team_id))
            self.config_team_name.setText(sender.currentText())
            if self.config_team_members.count() > 0:
                self.config_team_members.clear()
            self.config_team_members.addItems(
                self.players[sender.currentText()])

    def AddNewMember(self):

        sender = self.sender()
        self.config_team_members.addItem(sender.text())
        sender.clear()

    def DeleteMember(self):

        list_members = self.config_team_members.selectedItems()
        if len(list_members) == 0:
            QMessageBox.warning(self, "Error", "No player selected")
        else:
            for member in list_members:
                self.config_team_members.takeItem(
                                           self.config_team_members.row(member))

    def DeleteTeam(self):
        team_id = int(self.config_team_id.text())
        is_last_item = self.teams[self.teams.index(
            self.config_team_name.text())] == (self.teams[len(self.teams)-1])
        self.teams.pop(self.teams.index(self.config_team_name.text()))
        self.players.pop(self.config_team_name.text())
        new_teamlist = {}
        new_teamlist["teams"] = self.teams
        new_teamlist["players"] = self.players
        current_teams = open(THISDIR + "\\config\\teams.json", "w+",
                        encoding="utf-8")
        current_teams.write(json.dumps(new_teamlist, indent=4))
        current_teams.close()

        if is_last_item == True:
            self.teams_list.setCurrentIndex(1)
        else:
            self.teams_list.setCurrentIndex(team_id+1)
        self.teams_list.removeItem(team_id)
        self.UpdatePlayersList()
        self.cloth_east.setModel(self.players_combobox.model())
        self.cloth_south.setModel(self.players_combobox.model())
        self.cloth_west.setModel(self.players_combobox.model())
        self.cloth_north.setModel(self.players_combobox.model())

    def SaveEdits(self):

        list_members = [str(self.config_team_members.item(i).text()) for i in \
                                        range(self.config_team_members.count())]
        self.players[self.config_team_name.text()] = list_members
        new_teamlist = {}
        new_teamlist["teams"] = self.teams
        new_teamlist["players"] = self.players
        current_teams = open(THISDIR + "\\config\\teams.json", "w+",
                        encoding="utf-8")
        current_teams.write(json.dumps(new_teamlist, indent=4))
        current_teams.close()
        self.teamedit_wid.close()
        self.statusBar().showMessage("Settings saved.")

    def MatDialog(self):

        mat_dialog = QFileDialog(self)
        mat_dialog = QFileDialog.getOpenFileName(filter="Images (*.png *.jpg)",
            selectedFilter="Images (*.png *.jpg)")

        if mat_dialog[0] != "":
            self.GenerateMat(mat_dialog[0])

    def GenerateMat(self, image):

        self.background = image
        background = Image.open(self.background).resize((2048,2048))\
                                                .convert("RGBA")

        self.mat_thread = QThread()
        east_id = self.SearchTeamID(self.cloth_east, True)
        south_id = self.SearchTeamID(self.cloth_south, True)
        west_id = self.SearchTeamID(self.cloth_west, True)
        north_id = self.SearchTeamID(self.cloth_north, True)

        if self.config["save_route"] is None:
            save_to_route = THISDIR
        else:
            save_to_route = self.config["save_route"]
        self._createProgressBar()

        self.mat_worker = GenerateImageThread(background, self.table_border,
            east_id, south_id, west_id, north_id,
            self.technical_lines.isChecked(), save_to_route,
            self.bg_image, True)
        self.mat_worker.moveToThread(self.mat_thread)
        self.mat_thread.started.connect(self.mat_worker.run)
        self.mat_worker.update_progress.connect(self.UpdateStatus)
        self.mat_worker.finished.connect(self.mat_thread.quit)
        self.mat_worker.finished.connect(self.mat_worker.deleteLater)
        self.mat_thread.finished.connect(self.mat_thread.deleteLater)
        self.mat_thread.finished.connect(self.MatPreviewWindow)
        self.mat_thread.start()


    def MatPreviewWindow(self):

        self.statusBar().showMessage('Mat preview generated.')
        self.statusBar().removeWidget(self.progress_bar)
        # Now you can go back to rigging
        self.ChangeAppStatus(True)

        self.mat_wid = QWidget()
        self.mat_wid.resize(600, 600)
        self.mat_wid.setWindowTitle("Background preview")

        mat_preview_title = QLabel(self)
        mat_preview_title.setText("Selected image (1/4 scale)")
        mat_preview = QLabel(self)
        mat_preview.setPixmap(QPixmap(tempfile.gettempdir()+"\\Table_Dif.jpg")\
                                .scaled(512,512))
        confirm = QPushButton(self)
        confirm.setText("Confirm")
        confirm.clicked.connect(
            lambda: self.ChangeMatImage(self.background))

        vbox = QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(mat_preview_title)
        vbox.addWidget(mat_preview)
        vbox.addWidget(confirm)
        self.mat_wid.setLayout(vbox)

        self.mat_wid.setWindowModality(QtCore.Qt.ApplicationModal)
        self.mat_wid.activateWindow()
        self.mat_wid.raise_()
        self.mat_wid.show()

    def ChangeMatImage(self, image):

        new_bg = Image.open(image)

        if new_bg.size != (2048, 2048):
            new_bg = new_bg.resize((2048, 2048))
        if new_bg.mode != "RGBA":
            new_bg = new_bg.convert("RGBA")

        if self.config["save_route"] is not None:
            new_bg.save(self.config["save_route"]+"\\images\\mat.png")
            self.bg_image = self.config["save_route"]+"\\images\\mat.png"
        else:
            new_bg.save(THISDIR+"\\images\\mat.png")
            self.bg_image = THISDIR+"\\images\\mat.png"

        self.background = new_bg
        self.config["image_route"] = self.bg_image

        new_file = open(THISDIR + "\\config\\config.json", "w+",
                                        encoding="utf-8")
        new_file.write(json.dumps(self.config, indent=4))
        new_file.close()

        self.statusBar().showMessage('New background added.')
        self.statusBar().removeWidget(self.progress_bar)
        self.ChangeAppStatus(True)

        self.mat_wid.close()

    def GeneratePreview(self):

        self.preview_thread = QThread()
        east_id = self.SearchTeamID(self.cloth_east, True)
        south_id = self.SearchTeamID(self.cloth_south, True)
        west_id = self.SearchTeamID(self.cloth_west, True)
        north_id = self.SearchTeamID(self.cloth_north, True)

        if self.config["save_route"] is None:
            save_to_route = THISDIR
        else:
            save_to_route = self.config["save_route"]
        self._createProgressBar()

        self.preview_worker = GenerateImageThread(self.background,
            self.table_border, east_id, south_id, west_id, north_id,
            self.technical_lines.isChecked(), save_to_route,
            self.bg_image, True)
        self.preview_worker.moveToThread(self.preview_thread)
        self.preview_thread.started.connect(self.preview_worker.run)
        self.preview_worker.update_progress.connect(self.UpdateStatus)
        self.preview_worker.finished.connect(self.preview_thread.quit)
        self.preview_worker.finished.connect(self.preview_worker.deleteLater)
        self.preview_thread.finished.connect(self.preview_thread.deleteLater)
        self.preview_thread.finished.connect(self.PreviewWindow)
        self.preview_thread.start()

    def PreviewWindow(self):

        self.statusBar().showMessage('Tablecloth preview generated.')
        self.statusBar().removeWidget(self.progress_bar)
        # Now you can go back to rigging
        self.ChangeAppStatus(True)

        self.preview_wid = QWidget()
        self.preview_wid.resize(600, 600)
        self.preview_wid.setWindowTitle("Tablecloth preview")

        tablecloth = QPixmap(tempfile.gettempdir()+"\\Table_Dif.jpg")

        tablecloth_preview_title = QLabel(self)
        tablecloth_preview_title.setText("Tablecloth preview (1/4 scale)")
        tablecloth_preview = QLabel(self)
        tablecloth_preview.setPixmap(tablecloth.scaled(512,512))
        confirm = QPushButton(self)
        confirm.setText("Confirm")
        confirm.clicked.connect(self.GenerateImage)
        confirm.clicked.connect(self.preview_wid.close)

        vbox = QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(tablecloth_preview_title)
        vbox.addWidget(tablecloth_preview)
        vbox.addWidget(confirm)
        self.preview_wid.setLayout(vbox)

        self.preview_wid.setWindowModality(QtCore.Qt.ApplicationModal)
        self.preview_wid.activateWindow()
        self.preview_wid.raise_()
        self.preview_wid.show()

    def GeneratedDialog(self):

        self.statusBar().showMessage('Tablecloth generated. Happy rigging!')
        self.statusBar().removeWidget(self.progress_bar)
        # Now you can go back to rigging
        self.ChangeAppStatus(True)

        mbox = QMessageBox()

        mbox.setWindowTitle("Tablecloth Generator")
        mbox.setText("Tablecloth Generated!")
        mbox.setStandardButtons(QMessageBox.Ok)

        mbox.exec()

    def UpdateStatus(self, status):
        self.progress_bar.setValue(status)

    def GenerateImage(self):

        self.statusBar().showMessage('Generating image...')
        self._createProgressBar()

        if self.config["save_route"] is None:
            self.config["save_route"] = THISDIR

        save_to_route = QFileDialog.getExistingDirectory(self,
            "Where to save the image", self.config["save_route"],
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        if self.config["save_route"] != save_to_route:
            temp_file = open(THISDIR + "\\config\\config.json", "r",
                                            encoding="utf-8")
            fp_teams = json.loads(temp_file.read())
            fp_teams["save_route"] = save_to_route
            fp_teams["image_route"] = self.bg_image
            new_file = open(THISDIR + "\\config\\config.json", "w+",
                                            encoding="utf-8")
            new_file.write(json.dumps(fp_teams, indent=4))
            new_file.close()

        self.background = Image.open(THISDIR + "\\images\\mat.png")
        self.table_border = Image.open(THISDIR + "\\images\\table_border.png")
        self.tech_lines = Image.open(THISDIR + "\\images\\technical_lines.png")

        self.thread = QThread()
        east_id = self.SearchTeamID(self.cloth_east, True)
        south_id = self.SearchTeamID(self.cloth_south, True)
        west_id = self.SearchTeamID(self.cloth_west, True)
        north_id = self.SearchTeamID(self.cloth_north, True)
        self.worker = GenerateImageThread(self.background, self.table_border,
            east_id, south_id, west_id, north_id,
            self.technical_lines.isChecked(), save_to_route, self.bg_image)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.update_progress.connect(self.UpdateStatus)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.GeneratedDialog)
        self.thread.start()

    def ChangeAppStatus(self, status):
        # True for enable, False for disable.
        self.cloth_east.setEnabled(status)
        self.search_east.setEnabled(status)
        self.cloth_south.setEnabled(status)
        self.search_south.setEnabled(status)
        self.cloth_west.setEnabled(status)
        self.search_west.setEnabled(status)
        self.cloth_north.setEnabled(status)
        self.search_north.setEnabled(status)
        self.generate.setEnabled(status)

    def SearchTeamID(self, cloth, plus_one=False):
        team_id = self.teams.index(cloth.itemData(cloth.currentIndex()))
        if plus_one:
            team_id += 1
        return team_id

    def UpdatePlayersList(self):
        for team, members in self.players.items():
            for member in members:
                self.players_combobox.addItem(member, team)

    def center(self):
        qr = self.frameGeometry()
        cp = QScreen().availableGeometry().center()
        qr.moveCenter(cp)

    def SeeVersion(self):

        git_url = "https://raw.githubusercontent.com/vg-mjg/tablecloth-"
        git_url += "generator/main/version.txt"
        with urllib.request.urlopen(git_url) as response:
            url_version = response.read().decode("utf-8")

        version = "Your version is up to date!"
        if url_version != VERSION:
            version = "Your version is outdated."
            version += "Please check the <a href='https://github.com/vg-mjg/"
            version += "tablecloth-generator/releases'>Github page</a>"
            version +=" for updates."
        version_message = QMessageBox(self)
        version_message.setWindowTitle("Checking version")
        version_message.setText("""<h1>Tablecloth generator</h1>
            <br>
            <b>Current Version:</b> %s<br>
            <b>Your Version:</b> %s<br>
            <i>%s</i>
            """ % (url_version, VERSION, version))

        version_message.exec()

    def GetHelp(self):
        webbrowser.open("https://github.com/vg-mjg/tablecloth-generator/wiki")

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
