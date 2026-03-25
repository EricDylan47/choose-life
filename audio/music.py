# -*- coding: utf-8 -*-
"""
Audio/Music module
"""
import subprocess
import os
import sys


# ═══════════════════════════════════════════════════════════════════════════
# 音乐播放
# ═══════════════════════════════════════════════════════════════════════════
class MusicPlayer:
    def __init__(self):
        self.playing = False
        self.process = None

    def play(self, music_file=None):
        if self.playing:
            return
        if music_file and os.path.exists(music_file):
            try:
                self.process = subprocess.Popen(
                    ["afplay", "-v", "0.3", music_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.playing = True
            except:
                pass

    def stop(self):
        if self.process:
            try:
                self.process.terminate()
            except:
                pass
        self.playing = False


music_player = MusicPlayer()
