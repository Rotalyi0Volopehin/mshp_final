import pygame
import glob
import sys


class SoundPlayer:
    sounds = { }
    volume = 0.5

    @staticmethod
    def load():
        SoundPlayer.sounds = { }
        if sys.platform == "linux":
            slash = '/'
        else:
            slash = '\\'
        for sound_path in glob.glob("sounds{}*.wav".format(slash)):
            sound_name = sound_path[sound_path.rfind(slash) + 1: sound_path.rfind('.')]
            SoundPlayer.sounds[sound_name] = pygame.mixer.Sound(sound_path)

    @staticmethod
    def play_sound(name):
        if SoundPlayer.volume > 0.01:
            sound = SoundPlayer.sounds[name]
            sound.set_volume(SoundPlayer.volume)
            sound.play()
