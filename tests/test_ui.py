# test_ui.py - This tests the interface and sees if it does everything
# properly from start to finish.
# Standard Python libraries
import os
import sys
import json
# GUI libraries
import pytest
from PySide6 import QtCore
from PySide6.QtWidgets import (QWidget, QComboBox, QLabel, QPushButton, 
    QMessageBox, QCheckBox, QProgressBar, QLineEdit, QFileDialog,
    QMenu, QMenuBar, QListWidget)
# Programme libraries
from generator import THISDIR, TableClothGenerator


@pytest.fixture
def app(qtbot):
    tblc_app = TableClothGenerator()
    qtbot.addWidget(tblc_app)

    return tblc_app

def test_config_is_clean(qtbot):

    fp_config = open(THISDIR + "\\config\\config.json", "r",
                            encoding="utf-8")
    config_json = json.loads(fp_config.read())

    assert config_json["save_route"] == None
    assert config_json["image_route"] == None
    assert config_json["teams_file"] == "teams.json"
    assert config_json["total_teams"] == 0

def test_teams_is_clean(qtbot):

    fp_teams = open(THISDIR + "\\config\\teams.json", "r",
                            encoding="utf-8")
    teams_json = json.loads(fp_teams.read())

    assert len(teams_json["teams"]) == 0
    assert len(teams_json["players"]) == 0

def test_app_opens(app, qtbot):

    assert app.isVisible()
    app.close()

def test_app_first_config_opens(app, qtbot):

    assert app.no_config.isVisible
