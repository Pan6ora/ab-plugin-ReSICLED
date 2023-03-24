Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[Unreleased]
============

To be fixed
-----------

Upcoming
--------

 - improving updates between tabs
 - PDF Report

Under consideration
-------------------

- make a proper doc (eg. docstrings...)
- lint

[0.3.0] - 2022-03-24
====================

Fixed
-----

- Useless and buggy sngals calls
- Database path (according to pm2.0)
- Log warnings when re-importing plugin

Added
-----

- Signals when database list changed
- Conda build files

Changed
-------

- Update to pm2.0 
- Don't import an already existing database

Removed
-------

- Useless database file

[0.2.0] - 2022-11-16
====================

Fixed
-----

Added
-----

- methods requested by plugin-manager-0.2.0
- methods requested by plugin-manager-0.3.0

Changed
-------

- bw2packages files now follow Brightway2 guidelines
- Database tab moved to left panel
- database importation is now performed in DatabaseManager
- use only one instance of DatabaseManager

Removed
=======

- useless json databases removed
- useless comments removed

[0.1.1] - 2022-07-29
====================

Fixed
-----

 - Some Strange layouts

Added
-----

 - User and tech manuals (md and pdf versions)

Removed
-------

- Command-line ReSICLED version
- Manuals drafts

[0.1.0] - 2022-21-07
====================

Fixed
-----

 - Hotspots calculations
 - Improved tables display

Added
-----

 - Guidelines tab (and database)
