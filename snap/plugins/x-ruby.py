import os
import platform
import logging

import snapcraft
from snapcraft import sources


logger = logging.getLogger(__name__)


class RubyPlugin(snapcraft.BasePlugin):
  @classmethod
  def schema(cls):
    schema = super().schema()

    schema['properties']['gems'] = {
      'type': 'array',
      'minitems': 1,
      'uniqueItems': True,
      'items': {
        'type': 'string',
      },
      'default': [],
    }
    schema['properties']['documentation'] = {
      'type': 'boolean',
      'default': False,
    }

    if 'required' in schema:
      del schema['required']

    return schema

  def __init__(self, name, options, project):
    options.stage_packages = ['ruby']
    super().__init__(name, options, project)


  def env(self, root):
    ruby_paths = self.run_output(['ruby', '-e', 'puts $:']).split(os.linesep)
    ruby_paths = ':'.join(['$SNAP' + x for x in ruby_paths])
    gem_paths = self.run_output(['ruby', '-rubygems', '-e', 'puts Gem.path']).split(os.linesep)
    gem_paths = ':'.join(['$SNAP' + x for x in gem_paths])
    return ['GEM_HOME=%s/gems' % root,
            'GEM_PATH=%s' % gem_paths,
            'RUBYLIB=%s' % ruby_paths]

  def build(self):
    super().build()
    cmd = ['gem', 'install', '--env-shebang']
    if not self.options.documenation:
      cmd.append('--no-document')
    self.run(cmd + self.options.gems)

