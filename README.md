# ReSICLED

Evaluating the recyclability of electr(on)ic product for improving product design (eco-oriented design end of life).

This plugin is a rewrite of [the website](https://resicled-dev.g-scop.grenoble-inp.fr/ReSICLED-0.1/user/login) developed during the these "**ReSICLED: a new recovery-conscious design method for complex products based on a multicriteria assessment of the recoverability**"[^1]

[^1]: Fabrice Mathieux, Daniel Froelich, Pierre Moszkowicz. ReSICLED: a new recovery-conscious design method for complex products based on a multicriteria assessment of the recoverability. Journal of Cleaner Production, Elsevier, 2008, 2008 (16), pp.277-298. 10.1016/j.clepro.2006.07.026. hal-01206823v3
[Multiline description]

# Building package

```
conda create -n local_dev -c conda-forge -c cmutel -c bsteubing activity-browser-dev
conda activate local_dev
conda remove --force activity-browser-dev
conda activate local_dev
conda install conda-build
```

```
conda-build ../ --python=3.9.13
```
