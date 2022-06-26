from pathlib import Path
from PySide2.QtGui import QIcon

# absolut path of dir resicled
PATH_IMAGES = Path(__file__).resolve().parents[1]

class Icon():
    def __init__(self):
        self.path_images = self.get_path_image()
        self.add = QIcon(self.get_path_image_base('add.png'))
    
    def get_path_image(self) -> str:
        return str(PATH_IMAGES.joinpath('views','images'))
        
    def get_path_image_base(self, filename: str) -> str:
        return str(PATH_IMAGES.joinpath('views','images', 'base', filename))
    