import logging
import subprocess
from pathlib import Path

from src.config import ConfigWatcher, config
from src.enums import ConfigEvent, Modes

logger = logging.getLogger(__name__)
TIMER_PATH = str(Path.home()) + '/.local/share/systemd/user/yin_yang.timer'


def run_command(command, **kwargs):
    return subprocess.run(['systemctl', '--user', command, 'yin_yang.timer'], **kwargs)


class SaveWatcher(ConfigWatcher):
    def notify(self, event: ConfigEvent, values):
        if config.mode.value == Modes.MANUAL.value:
            run_command('stop')
            logger.debug('Stopping systemd timer')
            return

        logger.debug('Updating systemd timer')
        # update timer times
        with open(TIMER_PATH, 'r') as file:
            lines = file.readlines()

        time_light, time_dark = config.times
        lines[4] = f'OnCalendar={time_light.isoformat()}\n'
        lines[5] = f'OnCalendar={time_dark.isoformat()}\n'

        with open(TIMER_PATH, 'w') as file:
            file.writelines(lines)

        subprocess.run(['systemctl', '--user', 'daemon-reload'])
        run_command('start')


watcher = SaveWatcher()
