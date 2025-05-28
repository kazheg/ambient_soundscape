# -*- coding: utf-8 -*-

import os
import json
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QAction, QActionGroup
from aqt import mw, gui_hooks

# --- Add-on Info ---
ADDON_NAME = os.path.basename(os.path.dirname(__file__))
ADDON_FRIENDLY_NAME = "Ambient Soundscapes"

# --- Global Variables ---
player = None
audio_output = None # For Qt6, QMediaPlayer needs an audio output
current_sound_object = None # To keep a reference if needed, though player handles it

# --- Sound Definitions (Customize these to match your files and preferences) ---
SOUND_DEFINITIONS = {
    "rain": {
        "name": "Light Rain",  # Display name in the menu
        "file": "sounds/rain_light.mp3"  # Relative path from __init__.py
    },
    "insects": {
        "name": "Summer Insects",
        "file": "sounds/insects_summer.mp3"
    },
    # Add more sounds here, e.g.:
    # "forest": {
    #    "name": "Forest Ambience",
    #    "file": "sounds/forest_ambience.wav"
    # }
}

VOLUME_LEVELS = {
    "mute": {"name": "Mute", "level": 0.0},
    "low": {"name": "Low", "level": 0.25},
    "medium": {"name": "Medium", "level": 0.5},
    "high": {"name": "High", "level": 0.75}
}

# --- Configuration Management ---
DEFAULT_CONFIG = {
    "master_enabled": False,
    "selected_sound_key": "rain", # Default sound key
    "volume_key": "medium"      # Default volume key
}
config = DEFAULT_CONFIG.copy()

def load_config():
    global config
    loaded_config = mw.addonManager.getConfig(ADDON_NAME)
    if loaded_config:
        config.update(loaded_config)
    # Ensure default sound key exists if selected one is invalid
    if config["selected_sound_key"] not in SOUND_DEFINITIONS:
        config["selected_sound_key"] = next(iter(SOUND_DEFINITIONS)) # Fallback to first available sound
    if config["volume_key"] not in VOLUME_LEVELS:
        config["volume_key"] = "medium" # Fallback to medium volume

def save_config():
    mw.addonManager.writeConfig(ADDON_NAME, config)

# --- Sound Player Functions ---
def init_sound_player():
    global player, audio_output
    if player is None:
        player = QMediaPlayer(mw) # Parent to main window for lifecycle management
        audio_output = QAudioOutput(mw) # Create an audio output
        player.setAudioOutput(audio_output)
        # player.errorOccurred.connect(lambda err, msg: print(f"[{ADDON_FRIENDLY_NAME}] Player Error: {err}, {msg}")) # Optional: for debugging
        print(f"[{ADDON_FRIENDLY_NAME}] Sound player initialized.")

def play_current_sound():
    global player, audio_output, config
    if not config["master_enabled"]:
        stop_sound()
        return

    if player is None:
        init_sound_player()

    sound_key = config["selected_sound_key"]
    volume_key = config["volume_key"]

    if sound_key not in SOUND_DEFINITIONS or volume_key not in VOLUME_LEVELS:
        print(f"[{ADDON_FRIENDLY_NAME}] Error: Sound key '{sound_key}' or volume key '{volume_key}' not found.")
        stop_sound()
        return

    sound_info = SOUND_DEFINITIONS[sound_key]
    volume_info = VOLUME_LEVELS[volume_key]
    
    # Construct absolute path to the sound file
    sound_file_path = os.path.join(os.path.dirname(__file__), sound_info["file"])

    if not os.path.exists(sound_file_path):
        print(f"[{ADDON_FRIENDLY_NAME}] Error: Sound file not found at {sound_file_path}")
        # Optionally, notify user via tooltip
        # from aqt.utils import tooltip
        # tooltip(f"Ambient sound file missing: {sound_info['name']}", period=3000)
        stop_sound()
        return

    print(f"[{ADDON_FRIENDLY_NAME}] Attempting to play '{sound_info['name']}' at volume '{volume_info['name']}'.")
    
    player.stop() # Stop previous sound before playing a new one
    player.setSource(QUrl.fromLocalFile(sound_file_path))
    player.setLoops(QMediaPlayer.Loops.Infinite) # Loop indefinitely
    if audio_output: # For Qt6, volume is on QAudioOutput
         audio_output.setVolume(volume_info["level"])
    # For Qt5, player.setVolume(int(volume_info["level"] * 100)) might be used

    player.play()
    print(f"[{ADDON_FRIENDLY_NAME}] Playing '{sound_info['name']}'. State: {player.playbackState()}")


def stop_sound():
    global player
    if player and player.playbackState() != QMediaPlayer.PlaybackState.StoppedState:
        player.stop()
        print(f"[{ADDON_FRIENDLY_NAME}] Sound stopped.")

def set_volume_level(volume_key_str):
    global config, player, audio_output
    if volume_key_str in VOLUME_LEVELS:
        config["volume_key"] = volume_key_str
        save_config()
        new_volume_float = VOLUME_LEVELS[volume_key_str]["level"]
        if audio_output: # Qt6
            audio_output.setVolume(new_volume_float)
        # if player and player.playbackState() == QMediaPlayer.PlaybackState.PlayingState: # Qt5 might use this
        #     player.setVolume(int(new_volume_float * 100))
        print(f"[{ADDON_FRIENDLY_NAME}] Volume set to '{VOLUME_LEVELS[volume_key_str]['name']}' ({new_volume_float}).")
    else:
        print(f"[{ADDON_FRIENDLY_NAME}] Unknown volume key: {volume_key_str}")

# --- UI Setup ---
ambient_sound_menu = None
master_toggle_action = None
sound_selection_group = None
volume_selection_group = None

def on_master_toggle(checked):
    global config
    config["master_enabled"] = checked
    save_config()
    if checked:
        play_current_sound()
    else:
        stop_sound()
    print(f"[{ADDON_FRIENDLY_NAME}] Master enabled: {checked}")

def on_sound_select(sound_key):
    global config
    config["selected_sound_key"] = sound_key
    save_config()
    print(f"[{ADDON_FRIENDLY_NAME}] Sound selected: {sound_key}")
    if config["master_enabled"]:
        play_current_sound()

def on_volume_select(volume_key):
    set_volume_level(volume_key)
    # No need to call play_current_sound() again if only volume changes,
    # set_volume_level handles adjusting the live player.

def setup_menu():
    global ambient_sound_menu, master_toggle_action, sound_selection_group, volume_selection_group
    
    # Ensure player is ready for initial volume setting if auto-playing
    if config["master_enabled"] and player is None:
        init_sound_player()

    ambient_sound_menu = mw.form.menuTools.addMenu(ADDON_FRIENDLY_NAME)

    # 1. Master Toggle
    master_toggle_action = QAction("Enable Ambient Sound", mw, checkable=True)
    master_toggle_action.setChecked(config["master_enabled"])
    master_toggle_action.triggered.connect(on_master_toggle)
    ambient_sound_menu.addAction(master_toggle_action)

    ambient_sound_menu.addSeparator()

    # 2. Sound Selection
    sound_menu = ambient_sound_menu.addMenu("Select Sound")
    sound_selection_group = QActionGroup(mw) # Group for radio-button like behavior
    sound_selection_group.setExclusive(True)

    for key, sound_info in SOUND_DEFINITIONS.items():
        action = QAction(sound_info["name"], mw, checkable=True)
        action.setData(key) # Store key in action's data
        if key == config["selected_sound_key"]:
            action.setChecked(True)
        action.triggered.connect(lambda checked, k=key: on_sound_select(k) if checked else None)
        sound_menu.addAction(action)
        sound_selection_group.addAction(action)
    
    ambient_sound_menu.addSeparator()

    # 3. Volume Control
    volume_menu = ambient_sound_menu.addMenu("Volume")
    volume_selection_group = QActionGroup(mw)
    volume_selection_group.setExclusive(True)

    for key, volume_info in VOLUME_LEVELS.items():
        action = QAction(volume_info["name"], mw, checkable=True)
        action.setData(key)
        if key == config["volume_key"]:
            action.setChecked(True)
        action.triggered.connect(lambda checked, k=key: on_volume_select(k) if checked else None)
        volume_menu.addAction(action)
        volume_selection_group.addAction(action)
    
    print(f"[{ADDON_FRIENDLY_NAME}] Menu setup complete.")

# --- Anki Hooks ---
def on_profile_loaded():
    print(f"[{ADDON_FRIENDLY_NAME}] Profile loaded.")
    load_config()
    setup_menu() # Setup menu after config is loaded
    if config["master_enabled"]:
        # Small delay to ensure Anki UI is fully up and audio system is stable
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1000, play_current_sound) # Autoplay if was enabled

def on_profile_will_close():
    print(f"[{ADDON_FRIENDLY_NAME}] Profile will close. Stopping sound.")
    stop_sound()
    # QMediaPlayer and QAudioOutput parented to mw should be cleaned up by Qt,
    # but explicit cleanup can be done if issues arise.
    global player, audio_output
    if player:
        # player.setAudioOutput(None) # Disconnect from audio_output
        player.deleteLater() # Request deletion
        player = None
    if audio_output:
        # audio_output.deleteLater() # QAudioOutput might not need explicit deletion if not parented or managed well
        audio_output = None # For now, just nullify
    print(f"[{ADDON_FRIENDLY_NAME}] Player resources released (requested).")


gui_hooks.profile_did_open.append(on_profile_loaded)
gui_hooks.profile_will_close.append(on_profile_will_close)

print(f"[{ADDON_FRIENDLY_NAME}] Add-on initialized and loaded.")