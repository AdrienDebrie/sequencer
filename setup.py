#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# Copyright (C) Bull S.A.S (2010, 2011)
# Contributor: Pierre Vignéras <pierre.vigneras@bull.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
###############################################################################
import os,sys
import shlex
import subprocess

from glob import glob
from setuptools import setup, find_packages


VERSION_FILE = 'VERSION'
META_FILE = 'lib/sequencer/.metainfo'

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if not os.access('bin/sequencer', os.F_OK):
    os.symlink('sequencer', 'bin/sequencer')

try:
    with open(os.path.join(os.path.dirname(__file__), VERSION_FILE)) as version_file:
        for line in version_file:
            if not line.startswith('#'):
                (key, sep, value) = line.partition('=')
                if key == 'version':
                    version=value.strip()

    # Generate the .version file that contains the version and the last
    # commit
    last_commit_cmd_raw = "git log --pretty=format:'%H %aN %aE %ci'  -1"
    last_commit_cmd = shlex.split(last_commit_cmd_raw)
    try:
        last_commit = subprocess.check_output(last_commit_cmd)
    except subprocess.CalledProcessError as cpe:
        last_commit = "Unknown"
    with open(META_FILE, 'w') as f:
        # Do not change those names unless you also change in commons.py
        f.write("# The content of this file is generated by the packaging\n" + \
                "# process (either setup.py or Makefile)\n" + \
                "# Do not change it manually.\n" + \
                "sequencer.version = %s\n" % version + \
                "sequencer.lastcommit = %s\n" % last_commit)
except IOError as ioe:
    # This means that the META_FILE has already been generated.
    # Get the version from there.
    with open(META_FILE, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                (key, sep, value) = line.partition(' = ')
                print key, sep, value
                if len(key) > 0 and key.endswith('version') and len(value) > 0:
                    version = value.strip()

assert version is not None and len(version) > 0,\
       "Can't fetch version neither from %s nor from %s" % (VERSION_FILE, META_FILE)

setup(name='sequencer',
      version=version,
      package_dir={'': 'lib/'},
      packages=find_packages('lib'),
      package_data={'': ['.metainfo', 'ise/ise.xsd']},
      data_files=[('conf/', ['conf/config']),
                  ('doc/misc', glob('doc/misc/*')),
                  ('doc/man/man1', glob('doc/man/*.1')),
                  ('doc/man/man5', glob('doc/man/*.5'))],
      scripts=['bin/sequencer', 'bin/guesser'],
      author='Pierre Vignéras',
      author_email='pierre.vigneras@bull.net',
      maintainer='Pierre Vignéras',
      maintainer_email='pierre.vigneras@bull.net',
      license='GPL v3',
      url='http://pv-bull.github.com/sequencer',
      download_url = "http://github.com/downloads/pv-bull/sequencer/sequencer-%s.tar.gz" % version,
      platforms=['GNU/Linux', 'BSD', 'MacOSX'],
      keywords=['sequencer', 'executor', 'engine'],
      description='The sequencer is used to execute actions in a specified order (for example power on/off clusters)',
      long_description=read('README'),
      install_requires=['ClusterShell>=1.5', 'python-graph-core>=1.7.0', 'python-graph-dot>=1.7.0', 'pydot', 'lxml>=2.2.3'],
      provides=['sequencer'],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: POSIX :: BSD",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: System :: Clustering",
          "Topic :: System :: Distributed Computing"
      ]
     )

