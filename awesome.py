from threading import Thread
import Queue
import time
import os
import sys
import random
if sys.platform.startswith("linux"):
  from x11_watcher import KeyboardWatcher
elif sys.platform == "darwin":
  from cocoa_watcher import KeyboardWatcher

path = os.path.abspath(__file__+"/../")

class AwesomeKeyboardClicker(Thread):

    def __init__(self,queue):
        super(AwesomeKeyboardClicker,self).__init__()
        self.sound_files = {
            'clicks' : ["model_m/new_click_2.ogg","model_m/new_click_4.ogg","model_m/new_click_5.ogg","model_m/new_click_6.ogg","model_m/new_click_7.ogg","model_m/new_click_8.ogg"],
            'space' : ["model_m/click_6.ogg","model_m/click_1.ogg","model_m/click_2.ogg","model_m/click_3.ogg"],
            'carriage_returns' : ["model_m/carriage_return_1.ogg","model_m/carriage_return_2.ogg","model_m/carriage_return_3.ogg"],
        }
        if sys.platform == "darwin":
            self.key_roles = {
                (36,) : 'carriage_returns',
                (49,) : 'space',
            }
        else:
            self.key_roles = {
                (36,) : 'carriage_returns',
                (65,) : 'space',
            }
        self.queue = queue

    def run(self):
        import pygame
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        sounds = {}

        for sound_name,filenames in self.sound_files.items():
            sounds[sound_name] = []
            for filename in filenames:
                sound_path = os.path.join(path,'sounds',filename)
                sounds[sound_name].append(pygame.mixer.Sound(sound_path))  #load sound
        current_channel = 0

        print("Using %d channels." % pygame.mixer.get_num_channels())

        clicks_by_keycodes = {}
        while True:
            time.sleep(0.01)
            while not self.queue.empty():
                name,key = self.queue.get()
                played = False
                for keys,sound_name in self.key_roles.items():
                    if key in keys:
                        i = random.randrange(0,len(sounds[sound_name]))
                        sounds[sound_name][i].play()
                        played = True
                        break
                if not played:
                    i = random.randrange(0,len(sounds['clicks']))
                    sounds['clicks'][i].play()
                print(key)


if __name__ == '__main__':
    try:
        event_queue = Queue.Queue()
        awesome = AwesomeKeyboardClicker(event_queue)
        awesome.start()
        watcher = KeyboardWatcher("keyboard_watcher",event_queue)
        watcher.run() #must run in main thread
    except KeyboardInterrupt:
        awesome.terminate()
        exit(0)
