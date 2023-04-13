# Activity Browser plugin: ReSICLED

Evaluating the recyclability of electr(on)ic product for improving product design (eco-oriented design end of life).

This plugin is a rewrite of [the website](https://resicled-dev.g-scop.grenoble-inp.fr/ReSICLED-0.1/user/login) developed during the thesis "_ReSICLED: a new recovery-conscious design method for complex products based on a multicriteria assessment of the recoverability_"[^1]

**Caution: the database used by this software has not been updated since more than 10 years. Default values might not be relevant anymore.**

[^1]: [Fabrice Mathieux, Daniel Froelich, Pierre Moszkowicz. ReSICLED: a new recovery-conscious design method for complex products based on a multicriteria assessment of the recoverability. Journal of Cleaner Production, Elsevier, 2008, 2008 (16), pp.277-298. 10.1016/j.clepro.2006.07.026. hal-01206823v3](https://www.sciencedirect.com/science/article/abs/pii/S0959652606002770)
[Multiline description]

## Activity Browser

[The activity browser](https://github.com/LCA-ActivityBrowser/activity-browser) is an open source software for Life Cycle Assessment (LCA) that builds on top of the [Brightway2](https://brightway.dev) LCA framework.

The plugin system is currently not available on the main Activity Browser version.
See [Quickstart](#QuickStart) for how to get it.

# QuickStart

This section will let you get the modified version of Activity Browser and add the template plugin.

## Get Activity Browser with plugins 

See instructions in [Activity Browser README](https://github.com/Pan6ora/activity-browser).

## Get this plugin

- install the plugin with conda :

```
conda install -c pan6ora ab-plugin-resicled
```

- start Activity Browser
- Select the plugin in plugins list

# Infos

## Contact

If you have questions about this plugin you can contact [Rémy Le Calloch](mailto:remy@lecalloch.net).

## Authors

This plugin was developped at [G-SCOP Laboratory](https://g-scop.grenoble-inp.fr/en/laboratory) by

- Elysee Tchassem Noukimi (elysee.tchassem-noukimi@grenoble-inp.fr)
- Brice Notario Bourgade (brice.notario.bourgade@gmail.com)
- Rémy Le Calloch (remy@lecalloch.net)

## Copyright

- 2023: Grenoble Alpes University - Laboratory G-SCOP

## License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.