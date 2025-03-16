from __future__ import annotations
import sys
import json
from typing import TypedDict, Literal, Any
from collections.abc import Callable
from pathlib import Path
import os

from nbtlib.tag import String, Byte, Int

from level_dat_bedrock import BedrockLevelFile

class LevelDatUpdaterError(Exception):
    pass

def print_red(text: str):
    '''Prints text in red.'''
    for t in text.split('\n'):
        print("\033[91m {}\033[00m".format(t))

def nice_get_property(
        obj: dict,
        key: str,
        dict_name: str,
        type_condition: Callable[[Any], bool] | type,
        property_type_name: str | None = None
    ) -> Any:
    '''
    Gets a property from a dictionary and validates it. If it fails, it raises
    a LevelDatUpdaterError with a nice message.

    :param obj: The dictionary to get the property from.
    :param key: The key of the property.
    :param dict_name: The name of the dictionary. Used in the error message.
    :param type_condition: The type of the property or a function that returns
        True if the property is valid.
    :param property_type_name: The name of the type of the property. Used in
        the error message. If not specified, it will be the name of the type
        specified in type_condition unless type_condition is a function. This
        property is not optional if type_condition is a function.
    '''
    if isinstance(type_condition, type):
        if property_type_name is None:
            property_type_name = f"'{type_condition.__name__}'"
        condition = lambda v: isinstance(v, type_condition)
    else:
        if property_type_name is None:
            ValueError(
                "property_type_name must be specified if type_condition is a "
                "function.")
        condition = type_condition
    try:
        val = obj[key]
        if not condition(val):
            raise LevelDatUpdaterError(
                f"The '{key}' property of {dict_name} must be a "
                f"{property_type_name}.")
        return val
    except (KeyError, TypeError):
        raise LevelDatUpdaterError(
            f"Failed to load '{key}' from {dict_name}.")

class Settings(TypedDict):
    '''
    The settings property of the filter in the 'filters' list in the
    config.json file of the Regolith project (accessed via the sys.argv[1]).
    '''
    level_dat_path: Path
    release_config_path: Path
    paths_relative_to_config_json: bool

def load_settings() -> Settings:
    '''
    Loads the settings of the filter from sys.argv[1].
    '''
    # Load the data to a dictionary.
    try:
        settings = json.loads(sys.argv[1])
    except (IndexError, json.JSONDecodeError):
        raise LevelDatUpdaterError(
            "Failed to load the 'settings' property of the filter.")

    # Validate the data
    try:
        level_dat_path = Path(settings['level_dat_path'])
    except (KeyError, TypeError):
        raise LevelDatUpdaterError(
            "Failed to load 'level_dat_path' from settings.")
    try:
        release_config_path = Path(settings['release_config_path'])
    except (KeyError, TypeError):
        raise LevelDatUpdaterError(
            "Failed to load 'release_config_path' from settings.")
    try:
        levelname_path = Path(settings['levelname_path'])
    except (KeyError, TypeError):
        raise LevelDatUpdaterError(
            "Failed to load 'levelname_path' from settings.")


    paths_relative_to_config_json = settings.get(
        'paths_relative_to_config_json', True)
    if not isinstance(paths_relative_to_config_json, bool):
        raise LevelDatUpdaterError(
            "'paths_relative_to_config_json' must be a boolean.")

    # Update the paths if they are relative to the config.json file.
    if paths_relative_to_config_json:
        try:
            root_dir = os.environ['ROOT_DIR']
        except KeyError:
            raise LevelDatUpdaterError(
                "Failed to load 'ROOT_DIR' from environment variables.")
        root_dir = Path(root_dir)
        level_dat_path = root_dir / level_dat_path
        levelname_path = root_dir / levelname_path
        release_config_path = root_dir / release_config_path

    return Settings(
        level_dat_path=level_dat_path,
        levelname_path=levelname_path,
        release_config_path=release_config_path,
        paths_relative_to_config_json=paths_relative_to_config_json)

class ReleaseConfig(TypedDict):
    '''
    The release_config.json file data. The structure of the object is slightly
    different from the actual file. The 'settings' property is flattened and
    added to the root of the object.
    '''
    product_name: str
    '''Translates to the 'LevelName' tag in the level.dat file.'''

    multiplayer: bool
    '''
    Controlls the 'MultiplayerGameIntent' and 'XBLBroadcastIntent' tags in the
    level.dat file.

    If True, MultiplayerGameIntent is set to 1 and XBLBroadcastIntent is set
    to 1 (Friends of Friends).

    If False, MultiplayerGameIntent is set to 0 and XBLBroadcastIntent is set
    to 3 (Invite Only).
    '''

    cheats: bool
    '''Translates to the 'commandsEnabled' tag in the level.dat file.'''

    send_command_feedback: bool
    '''Translates to the 'sendcommandfeedback' tag in the level.dat file.'''
    
    commandblockoutput: bool
    '''Translates to 'commandblockoutput' tag in the level.dat file.'''

    do_day_light_cycle: bool
    '''Translates to 'dodaylightcycle' tag in the level.dat file.'''

    do_mob_spawning: bool
    '''Translates to the 'domobspawning' tag in the level.dat file.'''

    difficulty: Literal['peaceful', 'easy', 'normal', 'hard']
    '''Translates to the 'Difficulty' tag in the level.dat file as an integer (0-3).'''

    default_gamemode: Literal['survival', 'creative', 'adventure']
    '''Translates to the 'GameType' tag in the level.dat file as an integer (0-2).'''

def load_release_config(release_config_path: Path) -> ReleaseConfig:
    '''
    Loads the release_config.json file.
    '''
    # Load the data to a dictionary.
    try:
        with release_config_path.open('r', encoding='utf8') as f:
            release_config = json.load(f)
    except (json.JSONDecodeError, OSError):
        raise LevelDatUpdaterError(
            f"Failed to load release config file at "
            f"'{release_config_path.as_posix()}'.")

    # Get and validate the data.
    product_name: str = nice_get_property(
        release_config,
        'product_name',
        dict_name='the release config file',
        type_condition=str
    )
    settings: dict = nice_get_property(
        release_config,
        'settings',
        dict_name='the release config file',
        type_condition=dict
    )
    multiplayer: bool = nice_get_property(
        settings,
        'multiplayer',
        dict_name="'settings' in the release config file",
        type_condition=bool
    )
    cheats: bool = nice_get_property(
        settings,
        'cheats',
        dict_name="'settings' in the release config file",
        type_condition=bool
    )
    send_command_feedback: bool = nice_get_property(
        settings,
        'sendCommandFeedback',
        dict_name="'settings' in the release config file",
        type_condition=bool
    )
    commandblockoutput: bool = nice_get_property(
        settings,
        'commandBlockOutput',
        dict_name="'settings' in the release config file",
        type_condition=bool
    )
    do_day_light_cycle: bool = nice_get_property(
        settings,
        'doDayLightCycle',
        dict_name="'settings' in the release config file",
        type_condition=bool
    )
    do_mob_spawning: bool = nice_get_property(
        settings,
        'doMobSpawning',
        dict_name="'settings' in the release config file",
        type_condition=bool
    )
    difficulty: Literal['peaceful', 'easy', 'normal', 'hard'] = nice_get_property(
        settings,
        'difficulty',
        dict_name="'settings' in the release config file",
        type_condition=lambda x: x in ['peaceful', 'easy', 'normal', 'hard'],
        property_type_name="one of: 'peaceful', 'easy', 'normal', 'hard'"
    )
    default_gamemode: Literal['survival', 'creative', 'adventure'] = nice_get_property(
        settings,
        'defaultGamemode',
        dict_name="'settings' in the release config file",
        type_condition=lambda x: x in ['survival', 'creative', 'adventure'],
        property_type_name="one of: 'survival', 'creative', 'adventure'"
    )
    return ReleaseConfig(
        product_name=product_name,
        multiplayer=multiplayer,
        cheats=cheats,
        send_command_feedback=send_command_feedback,
        commandblockoutput=commandblockoutput,
        do_day_light_cycle=do_day_light_cycle,
        do_mob_spawning=do_mob_spawning,
        difficulty=difficulty,
        default_gamemode=default_gamemode
    )


def update_level_dat(level_dat_path: Path, release_config: ReleaseConfig, levelname_path: Path):
    '''
    Updates the level.dat file.
    '''
    try:
        if release_config['multiplayer']:
            multiplayer_game_intent = Byte(1)
            xbl_broadcast_intent = Int(3)
        else:
            multiplayer_game_intent = Byte(0)
            xbl_broadcast_intent = Int(1)

        with BedrockLevelFile.load(level_dat_path) as level_data:
            level_data['LevelName'] = String(release_config['product_name'])
            level_data['MultiplayerGameIntent'] = multiplayer_game_intent
            level_data['XBLBroadcastIntent'] = xbl_broadcast_intent
            level_data['commandsEnabled'] = Byte(release_config['cheats'])
            level_data['sendcommandfeedback'] = Byte(release_config['send_command_feedback'])
            level_data['commandblockoutput'] = Byte(release_config['commandblockoutput'])
            level_data['dodaylightcycle'] = Byte(release_config['do_day_light_cycle'])
            level_data['domobspawning'] = Byte(release_config['do_mob_spawning'])
            level_data['Difficulty'] = Int(
                {
                    'peaceful': 0,
                    'easy': 1,
                    'normal': 2,
                    'hard': 3
                }[release_config['difficulty']]
            )
            level_data['GameType'] = Int(
                {
                    'survival': 0,
                    'creative': 1,
                    'adventure': 2
                }[release_config['default_gamemode']]
            )
        # Update Levelname file
        if not levelname_path.exists():
            levelname_path.touch()

        levelname_path.write_text(release_config['product_name'])

    except OSError:
        raise LevelDatUpdaterError(
            f"Failed to load level.dat file at "
            f"'{level_dat_path.as_posix()}'.")

def main():
    settings = load_settings()
    # A hint for the user in the error based on the
    # 'paths_relative_to_config_json' setting.
    if settings['paths_relative_to_config_json']:
        hint = (
            "Did you forget to set 'paths_relative_to_config_json' to 'true'?")
    else:
        hint = (
            "Did you forget to set 'paths_relative_to_config_json' to 'false'?")

    # Check if important files exist.
    if not settings['level_dat_path'].exists():
        raise LevelDatUpdaterError(
            f"Level.dat file does not exist at "
            f"'{settings['level_dat_path']}'.\n"
            f"{hint}")
    if not settings['release_config_path'].exists():
        raise LevelDatUpdaterError(
            f"Release config file does not exist at "
            f"'{settings['release_config_path']}'.\n"
            f"{hint}")

    # Load the data from the release_config.json file.
    release_config = load_release_config(settings['release_config_path'])

    # Update the level.dat file.
    update_level_dat(settings['level_dat_path'],
                     release_config, settings['levelname_path'])

if __name__ == "__main__":
    try:
        main()
    except LevelDatUpdaterError as e:
        print_red(str(e))
        sys.exit(1)
