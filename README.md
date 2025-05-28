# Ambient Soundscapes for Anki

**Version:** 1.0.0
**Anki Compatibility:** Recommended for Anki 23.10 and newer (versions that use Qt6). Older versions using Qt5 will not be compatible.

Enhance your Anki study sessions with calming background sounds like gentle rain or summer insects. Create a more focused and pleasant learning environment.

## Features

* **Background Audio:** Plays continuous, looping ambient sounds while you use Anki.
* **Easy Controls:** Manage sounds directly from Anki's "Tools" menu.
    * **Master Toggle:** Quickly enable or disable all ambient sounds.
    * **Sound Selection:** Choose from a predefined list of soundscapes (e.g., "Light Rain," "Summer Insects").
    * **Volume Adjustment:** Set volume to Mute, Low, Medium, or High.
* **Persistent Settings:** The add-on remembers your last-used settings (enabled state, selected sound, volume) and restores them the next time you open Anki.
* **Customizable Sounds:** Easily add your own sound files to personalize your auditory experience.
* **Qt Multimedia:** Uses Anki's built-in Qt libraries for reliable sound playback without extra dependencies like Pygame.

## Screenshots

*(As this is an audio-based add-on, visual screenshots are minimal. The primary interface is through Anki's menu.)*

The add-on adds a new menu under **Tools > Ambient Soundscapes**:
Tools
└── Ambient Soundscapes
├── Enable Ambient Sound  (Checkbox)
├── --------------------- (Separator)
├── Select Sound
│   ├── Light Rain        (Radio button style)
│   └── Summer Insects    (Radio button style)
│   └── (Your other sounds here)
├── --------------------- (Separator)
└── Volume
├── Mute              (Radio button style)
├── Low               (Radio button style)
├── Medium            (Radio button style)
└── High              (Radio button style)
## Usage

1.  **Installation:**
    * Ensure your Anki version is 23.10 or newer.
    * Download and install the add-on (e.g., by placing the `ambient_soundscapes` folder into your Anki add-ons directory).
    * The add-on code itself does not include sound files. **You must provide your own.**

2.  **Adding Sound Files (CRITICAL STEP):**
    * Inside your Anki add-ons folder, open the `ambient_soundscapes` folder.
    * Create a new subfolder named `sounds`.
    * Place your desired sound files (e.g., `.mp3`, `.wav`) into this `sounds` folder.

    **Example Sounds Mentioned in Default Configuration:**

    The default `SOUND_DEFINITIONS` in the add-on code points to:

    * **`sounds/rain_light.mp3` (Displayed as "Light Rain"):**
        * *Suggested type:* A continuous recording of gentle rain.
        * *Example:* Imagine a soundscape similar to a 3-hour rain recording.
        * *For inspiration on the type of audio (you still need to provide the actual `.mp3` or `.wav` file):* Think of long-form rain videos, for instance, conceptually similar to content that might be found via a general search for long rain sounds (an illustrative placeholder for where one might find such *video* inspiration could be imagined as `https://www.youtube.com/watch?v=q76bMs-NwRk&t=64s`).
    * **`sounds/insects_summer.mp3` (Displayed as "Summer Insects"):**
        * *Suggested type:* A continuous recording of summer insect sounds (cicadas, crickets).
        * *Example:* Imagine a soundscape similar to a 2-hour insect ambiance.
        * *For inspiration on the type of audio (you still need to provide the actual `.mp3` or `.wav` file):* Think of long-form ambient insect sound videos (an illustrative placeholder for where one might find such *video* inspiration could be imagined as `https://www.youtube.com/watch?v=mUonUzV31wI&t=1329s`).

    **Remember:** You must download or create these audio files (e.g., `.mp3`, `.wav`) yourself and place them in the `ambient_soundscapes/sounds/` folder. The add-on plays local audio files, not online videos. The provided example URLs are purely conceptual placeholders for the *type* of lengthy ambient videos that might inspire the audio you choose to find or create.

    To use these specific examples, you would:
    1.  Obtain a suitable "light rain" audio file (e.g., MP3, WAV), ideally one that loops well or is very long. Rename it to `rain_light.mp3` and place it in the `sounds` folder.
    2.  Obtain a suitable "summer insects" audio file. Rename it to `insects_summer.mp3` and place it in the `sounds` folder.

    If your filenames are different, you must edit the `SOUND_DEFINITIONS` dictionary at the top of the `__init__.py` file to match your filenames and desired display names.
    ```python
    # Example SOUND_DEFINITIONS in __init__.py:
    SOUND_DEFINITIONS = {
        "rain": { # This is the 'key'
            "name": "Light Rain",  # Display name in the menu
            "file": "sounds/rain_light.mp3"  # Path relative to __init__.py
        },
        "insects": {
            "name": "Summer Insects",
            "file": "sounds/insects_summer.mp3"
        },
        # To add a new sound called "Forest":
        # "forest": {
        #    "name": "Deep Forest",
        #    "file": "sounds/my_forest_sound.wav" # Make sure this file exists
        # }
    }
    ```

3.  **Controlling Sounds:**
    * Restart Anki after installation and adding sound files.
    * Go to the Anki main menu: `Tools > Ambient Soundscapes`.
    * **Enable Ambient Sound:** Check this option to turn sounds on. Uncheck to turn them off.
    * **Select Sound:** Choose your preferred soundscape from the submenu. Only one sound can play at a time.
    * **Volume:** Adjust the playback volume.
    * The add-on will remember your settings. If "Enable Ambient Sound" was checked when you last closed Anki, the sound will resume automatically (after a brief delay) when you next start Anki.

## Configuration

Most configuration is done directly via the `Tools > Ambient Soundscapes` menu. The add-on also saves its settings in a `config.json` file within its folder. Manual editing of this file is generally not needed.

The `config.json` stores:
* `master_enabled`: `true` or `false`.
* `selected_sound_key`: The key (e.g., "rain") of the last selected sound from `SOUND_DEFINITIONS`.
* `volume_key`: The key (e.g., "medium") of the last selected volume from `VOLUME_LEVELS`.

## Customization

**Adding More Sounds:**

1.  Place your new sound file (e.g., `my_sound.mp3`) into the `ambient_soundscapes/sounds/` folder.
2.  Open the `__init__.py` file in the `ambient_soundscapes` folder.
3.  Add a new entry to the `SOUND_DEFINITIONS` dictionary near the top of the file. For example:
    ```python
    SOUND_DEFINITIONS = {
        # ... existing sounds ...
        "my_custom_sound": {  # Choose a unique key
            "name": "My Custom Sound",  # This name will appear in the menu
            "file": "sounds/my_sound.mp3" # Path to your file
        }
    }
    ```
4.  Restart Anki. Your new sound should now appear in the "Select Sound" submenu.

## Important Notes

* **Anki Version:** This add-on requires Anki 23.10 or newer, as it uses Qt6 multimedia features.
* **Sound Files Required:** This add-on **does not come with sound files**. You must provide your own and place them in the `sounds` subfolder. Ensure file paths and names match the `SOUND_DEFINITIONS` in the code.
* **Supported Formats:** `QMediaPlayer` (used by the add-on) generally supports common audio formats like MP3, WAV, AAC, etc., depending on your system's codecs. MP3 and WAV are good choices for broad compatibility.
* **Troubleshooting:** If sounds don't play:
    * Double-check that your sound files are in the correct `sounds` folder.
    * Verify that the filenames in `SOUND_DEFINITIONS` (inside `__init__.py`) exactly match your sound filenames (including the extension, e.g., `.mp3`).
    * Check Anki's debug console for any error messages (on macOS: `Help > Debugging > Debug Console`). Messages from this add-on are prefixed with `[Ambient Soundscapes]`.

## Future Ideas

* Individual volume sliders for more fine-grained control.
* Ability to add sound files/folders directly through the UI.
* Random playback from a selected playlist or folder.
* Sound profiles that change based on deck or card type.

## Credits & License

* **Author:** Created by @paerontran.
* **Concept:** Based on user request for ambient background sounds in Anki.
* **License:** This add-on is provided as-is. You are free to use and modify it. If you use sounds from external sources, ensure you comply with their respective licenses.

---
