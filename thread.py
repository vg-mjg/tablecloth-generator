
# thread.py - All Thread functions go here
# Standard python library
import os
import sys
import tempfile
from pathlib import Path
# The __debug__ lines are ignored in the compilation
if __debug__:
    from timeit import default_timer as timer
# Image manipulation libraries
from PIL import Image
# GUI libraries
from PySide6.QtCore import QObject, Signal


# Absolute path to the current folder as constant for easy access
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR))


class GenerateImageThread(QObject):
    finished = Signal()
    update_progress = Signal(int)

    def __init__(self, tablecloth, border, east_id, south_id, west_id, north_id,
        technical_lines=False, save_to=None, bg_image=None, temp_img=False,
        parent=None):
        super().__init__()
        self.tablecloth = tablecloth
        self.border = border
        self.east_id = east_id
        self.south_id = south_id
        self.west_id = west_id
        self.north_id = north_id
        self.technical_lines = technical_lines
        self.save_to_route = save_to
        self.bg_image = bg_image
        self.temp_img = temp_img

    def run(self):
        if __debug__:
            start = timer()

        self.update_progress.emit(10)

        image_east = Image.open(THISDIR + "\\images\\logos\\team%d.png"\
            % self.east_id)
        team_east = image_east.convert("RGBA")

        image_south = Image.open(THISDIR + "\\images\\logos\\team%d.png"\
            % self.south_id)
        team_south = image_south.rotate(90, expand=True).convert("RGBA")
        
        image_west = Image.open(THISDIR + "\\images\\logos\\team%d.png"
            % self.west_id)
        team_west = image_west.rotate(180, expand=True).convert("RGBA")
        
        image_north = Image.open(THISDIR + "\\images\\logos\\team%d.png"
            % self.north_id)
        team_north = image_north.rotate(-90, expand=True).convert("RGBA")

        self.update_progress.emit(40)
        # Let's check the file does not exist first
        if os.path.exists(self.save_to_route+"/Table_Dif.jpg"):
            os.remove(self.save_to_route+"/Table_Dif.jpg")
        if os.path.exists(tempfile.gettempdir()+"/Table_Dif.jpg"):
            os.remove(tempfile.gettempdir()+"/Table_Dif.jpg")

        final_tablecloth = Image.new("RGBA", self.tablecloth.size)
        final_tablecloth.paste(self.tablecloth, (0, 0), self.tablecloth)
        final_tablecloth.paste(self.border, (0, 0), self.border)
        if self.technical_lines:
            tech_lines = Image.open(THISDIR + "\\images\\technical_lines.png")\
                              .convert("RGBA")
            final_tablecloth.paste(tech_lines, (0, 0), tech_lines)
        self.update_progress.emit(50)
        # Check that each image is full or just logo, then submit
        if image_east.size == (1568, 786):
            final_tablecloth.paste(team_east, (240, 1020), team_east)
        else:
            final_tablecloth.paste(team_east.resize((250, 250)), (900, 1325), team_east.resize((250, 250)))
        if image_south.size == (1568, 786):
            final_tablecloth.paste(team_south, (1020, 235), team_south)
        else:
            final_tablecloth.paste(team_south.resize((250, 250)), (1420, 900), team_south.resize((250, 250)))
        if image_west.size == (1568, 786):
            final_tablecloth.paste(team_west, (235, 240), team_west)
        else:
            final_tablecloth.paste(team_west.resize((250, 250)), (890, 370), team_west.resize((250, 250)))
        if image_north.size == (1568, 786):
            final_tablecloth.paste(team_north, (240, 240), team_north)
        else:
            final_tablecloth.paste(team_north.resize((250, 250)), (400, 910), team_north.resize((250, 250)))
        self.update_progress.emit(75)
        if self.temp_img is False:
            final_tablecloth.convert("RGB").save(self.save_to_route\
                                         +"\\Table_Dif.jpg")
        else:
            final_tablecloth.convert("RGB").save(tempfile.gettempdir()\
                                         +"\\Table_Dif.jpg")
        self.update_progress.emit(90)
        # If it exists, it means that the process was successful
        if os.path.exists(self.save_to_route+"/Table_Dif.jpg")\
        or os.path.exists(tempfile.gettempdir()+"\\Table_Dif.jpg"):
            if __debug__:
                end = timer()
                print("This took %d seconds." % (end - start))
            self.update_progress.emit(100)
            self.finished.emit()