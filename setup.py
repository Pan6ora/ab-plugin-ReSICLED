# -*- coding: utf-8 -*-
import os
from setuptools import setup

######################
# PLUGIN DESCRIPTION #
######################

name='ReSICLED',
version="0.1.0",
author="Rémy Le Calloch, Brice Notario Bourgade, Elysée Tchassem Noukimi",
author_email="remy@lecalloch.net",
url="https://gricad-gitlab.univ-grenoble-alpes.fr/green-scop/ab-plugins/resicled",
description='Evaluate the recyclability of product Electr(on)ic for improving product design',
classifiers=[
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Scientific/Engineering :: Visualization',
]

######################

infos = {
    'name': name,
    'version': version,
    'author': author,
    'author_email': author_email,
    'url': url,
    'description': description
}


packages = []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)
accepted_filetypes = (".html", ".png", ".svg", ".js", ".css")

for dirpath, dirnames, filenames in os.walk('plugin'):
    # Ignore dirnames that start with '.'
    if ('__init__.py' in filenames
            or any(x.endswith(accepted_filetypes) for x in filenames)):
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)

setup(
    name=name,
    version=version,
    packages=packages,
    include_package_data=True,
    author=author,
    author_email=author_email,
    license=open('LICENSE.txt').read(),
    install_requires=[], # dependency management in conda recipe
    url=url,
    long_description=open('README.md').read(),
    description=description,
    classifiers=classifiers,
    )