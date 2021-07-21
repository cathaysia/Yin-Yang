import os
import json
import logging
from os.path import isdir
from pathlib import Path
from typing import Optional

from ._plugin import Plugin, get_stuff_in_dir


logger = logging.getLogger(__name__)


def write_new_settings(settings, path):
    # simple adds a new field to the settings
    settings["workbench.colorTheme"] = "Default"
    with open(path, 'w') as conf:
        json.dump(settings, conf, indent=4)


class Vscode(Plugin):
    name = 'VS Code'

    def set_theme(self, theme: str) -> Optional[str]:
        if not theme:
            raise ValueError(f'Theme \"{theme}\" is invalid')

        if not (self.available and self.enabled):
            return

        path = str(Path.home()) + "/.config/"

        possible_editors = [
            "VSCodium",
            "Code - OSS",
            "Code",
            "Code - Insiders",
        ]

        for editor in possible_editors:
            editor = path + editor + '/User/settings.json'
            if os.path.isfile(editor):
                # load the settings
                with open(editor, "r") as sett:
                    try:
                        settings = json.load(sett)
                        settings['workbench.colorTheme'] = theme
                    except json.decoder.JSONDecodeError as e:
                        # check if the file is completely empty
                        sett.seek(0)
                        first_char: str = sett.read(1)
                        if not first_char:
                            # file is empty
                            print('File is empty')
                            settings = {"workbench.colorTheme": theme}
                        else:
                            # settings file is malformed
                            raise e

                # write changed settings into the file
                with open(editor, 'w') as sett:
                    json.dump(settings, sett)

                return theme

        raise FileNotFoundError('No config file found. '
                                'If you see this error, try to set a custom theme manually once and try again.')

    @property
    def available_themes(self) -> dict:
        paths = ['/usr/lib/code/extensions',
                 str(Path.home()) + '/.vscode-oss/extensions']
        themes_dict = {}
        if not self.available:
            return themes_dict

        for path in paths:
            extension_dirs = get_stuff_in_dir(path, type='dir')
            # filter for a dir that doesnt seem to be an extension
            # since it has no manifest
            if 'node_modules' in extension_dirs:
                extension_dirs.pop(extension_dirs.index('node_modules'))

            for extension_dir in extension_dirs:
                try:
                    with open(f'{path}/{extension_dir}/package.json', 'r') as file:
                        manifest = json.load(file)

                    try:
                        if 'Themes' not in manifest['categories']:
                            continue
                    except KeyError:
                        pass
                    try:
                        if 'themes' not in manifest['contributes']:
                            continue
                    except KeyError:
                        pass

                    try:
                        themes: list = manifest['contributes']['themes']

                        for theme in themes:
                            if 'id' in theme:
                                themes_dict[theme['id']] = theme['id']
                            else:
                                themes_dict[theme['label']] = theme['label']
                    except KeyError as e:
                        logger.error(str(e))
                        continue

                except FileNotFoundError as e:
                    logger.error(str(e))
                    themes_dict = {}
                    break

        assert themes_dict != {}, 'No themes found'
        return themes_dict

    def __str__(self):
        # for backwards compatibility
        return 'code'

    @property
    def available(self) -> bool:
        return isdir('/usr/lib/code/extensions')