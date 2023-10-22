import pygame
from pygame import mixer

def request_text():
    return [
    "On a chilling Halloween night beneath the eerie",
    # "moonlight friends gathered by a wickedly grinning",
    # "pumpkin. They exchanged terrifying tales of ghosts",
    # "sending shivers down their spines. Suddenly a rustle",
    # "in the bushes made them jump. But it was not a",
    # "ghost it was their mischievous zombie friend clad",
    # "in tattered clothes. The night was filled with",
    # "laughter scares and the warmth of pumpkin-spiced",
    # "treats as they celebrated Halloween in all its scary glory."
]


class Text:
    font = pygame.freetype.Font("assets/fonts/griffy.ttf", 50)
    font.origin = True
    font_height = font.get_sized_height()
    M_ADV_X = 4

    def __init__(self, gameDisplay: pygame.Surface, text: [str]) -> None:
        self.gameDisplay = gameDisplay
        self.texts = text
        self.letter_index = 0
        self.text_index = 0

        self.update_stuff()

    def update_stuff(self):
        self.text_surf_rect = self.font.get_rect(self.current_text())
        self.baseline = self.text_surf_rect.y
        self.text_surf = pygame.Surface(self.text_surf_rect.size)
        self.text_surf_rect.center = self.gameDisplay.get_rect().center
        self.metrics = self.font.get_metrics(self.current_text())

    def current_text(self) -> str:
        return self.texts[self.text_index]

    def next_text(self) -> None:
        self.text_index += 1
        if self.text_index >= len(self.texts):
            mixer.music.load("assets/audio/scream.mp3")
            mixer.music.set_volume(2)
            mixer.music.play() 
            self.text_index = 0

        self.update_stuff()

    def current_letter(self) -> None:
        return self.texts[self.text_index][self.letter_index].lower()

    def next_letter(self) -> None:
        self.letter_index += 1
        if self.letter_index >= len(self.current_text()):
            self.letter_index = 0
            self.next_text()
