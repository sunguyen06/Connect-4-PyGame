import os

# Game dimensions
WIDTH = 860
HEIGHT = 840
ROWS = 6
COLUMNS = 7
PIECE_SIZE = 100

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (25, 25, 26)
BLUE = (0, 122, 204)
DARK_BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (254, 216, 177)

# Asset paths
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# Image paths
BOARD_IMAGE = os.path.join(IMAGES_DIR, "Board.png")
INSTRUCTIONS_IMAGE = os.path.join(IMAGES_DIR, "Instructions.png")
BLUR_IMAGE = os.path.join(IMAGES_DIR, "Blur.png")

# Sound paths
BUTTON_SOUND = os.path.join(SOUNDS_DIR, "ButtonSound.wav")
PIECE_SOUND = os.path.join(SOUNDS_DIR, "pieceSound.wav")
ERROR_SOUND = os.path.join(SOUNDS_DIR, "Invalid.wav")

# Font paths
FONT_PATH = os.path.join(FONTS_DIR, "telegraphem.otf")

# Game settings
ANIMATION_SPEED = 10
VOLUME = 0.2

# Board positions
PIECE_X = [70, 190, 310, 430, 550, 670, 790]
PIECE_Y = [170, 290, 410, 530, 650, 770] 