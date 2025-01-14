import unittest

from src.config import config
from src.plugins import plugins
from src.plugins._plugin import Plugin


class PluginsTest(unittest.TestCase):
    def test_setup(self):
        for pl in plugins:
            with self.subTest(plugin=pl.name):
                self.assertIsInstance(pl, Plugin,
                                      'Every plugin should extend the Plugin class')
                self.assertTrue(pl.name != '',
                                'Every plugin needs a name for the config and the gui.')
                if pl.available:
                    self.assertIsInstance(pl.available_themes, dict,
                                          'Available themes always should be a dict.')

    def test_set_empty_theme(self):
        for pl in plugins:
            with self.subTest(plugin=pl):
                try:
                    pl.set_theme('')
                except ValueError as e:
                    self.assertEqual('Theme \"\" is invalid', str(e),
                                     'set_theme() should throw an exception if the theme is empty')
                    return

                self.assertTrue(False,
                                'set_theme() should throw an exception if the theme is empty!')
                # try to return to previous theme
                pl.set_theme(config.get(pl.name + config.get('theme').title() + 'Theme'))

    def test_set_theme_invalid_state(self):
        for pl in plugins:
            with self.subTest(plugin=pl):
                if pl.enabled:
                    pl.enabled = False

                self.assertFalse(pl.set_theme('dark'),
                                 'set_theme() should not be successful if the plugin is disabled')

    # NOTE if you want to test that your theme changes, set this value to true
    @unittest.skipUnless(False, 'test_theme_changes is disabled')
    def test_set_theme_works(self):
        # FIXME the path in the wallpaper plugin is relative, therefore it is not testable
        for pl in [pl for pl in plugins if pl.name != 'Wallpaper']:
            if pl.enabled:
                with self.subTest('Changing the theme should be successful', plugin=pl.name):
                    theme = config[str(pl) + ('Dark' if config['theme'] == 'dark' else 'Light') + 'Theme']

                    self.assertEqual(theme, pl.set_theme(theme),
                                     'set_theme() should return the name of the theme to indicate it was successful')
                    self.assertTrue(pl.set_mode(config['theme'] == 'dark'),
                                    'set_mode() should be true, indication that it was successful')


if __name__ == '__main__':
    unittest.main()
