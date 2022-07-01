from pathlib import Path
from PySide2.QtGui import QIcon,QPixmap

# absolut path of dir resicled
PATH_IMAGES = Path(__file__).resolve().parents[1]

class Icon():
    def __init__(self):
        self.path_images = self.get_path_image()
        self.add = QIcon(self.get_path_image_base('add.png'))
        self.delete = QIcon(self.get_path_image_base('delete.png'))
        self.edit = QIcon(self.get_path_image_base('edit.png'))
        #get logo
        self.logo = QPixmap(self.get_path_image_logo('logo_resicled.png'))
    
    def get_path_image(self) -> str:
        return str(PATH_IMAGES.joinpath('views','images'))
        
    def get_path_image_base(self, filename: str) -> str:
        return str(PATH_IMAGES.joinpath('views','images', 'base', filename))
    
    def get_path_image_logo(self, filename: str) -> str:
        return str(PATH_IMAGES.joinpath('views','images', 'logo', filename))
    
    
    