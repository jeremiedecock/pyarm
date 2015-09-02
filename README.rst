======
PyArm_
======

Copyright (c) 2010,2015 Jeremie DECOCK (http://www.jdhp.org)


* Web site: http://www.jdhp.org/projects_en.html#pyarm
* Online documentation: http://pyarm.readthedocs.org
* Source code: https://github.com/jeremiedecock/pyarm
* Issue tracker: https://github.com/jeremiedecock/pyarm/issues
* PyArm on PyPI: https://pypi.python.org/pypi/pyarm


Description
===========

Pyarm_ is a physics simulator which provides an anthropomorphic arm model
for experiments on human like motor control.

The arm model is described in the following technical report (written in
French): http://download.tuxfamily.org/jdhp/pdf/pyarm.pdf .

Pyarm has been used at the `Institute for Intelligent Systems and Robotics`_
for experiments on adaptive systems. These experiments are described in the
following academic paper *Learning cost-efficient control policies with XCSF:
generalization capabilities and further improvement* by Didier Marin, Jérémie
Decock, Lionel Rigoux and Olivier Sigaud. This scientific contribution has been
published in the *Proceedings of the 13th annual conference on Genetic and
evolutionary computation (GECCO'11)*, the main international conference on
genetic and evolutionary computation.

.. The following section briefly describe these experiments.
.. 
.. The full description of these expriments can be downloaded ...
This paper can be downloaded on
`www.jdhp.org <http://www.jdhp.org/articles_en.html#XCSF>`__.

.. ...
.. ---
.. 
.. Mettre ici une partie des slides... The goal ... (schema du bras +
.. schéma avec légende du bras dans pyarm) - forearm - shoulder - elbow -
.. end point effector - target - mussles - ...
.. 
.. First step: the learning phase. Optimal trajectories for several random
.. targets are computed by our solver (QOPS). These trajectories are slow
.. to compute (several minutes per trajectory). Thus this solver cannot be
.. used for real time control of robots... Therefore we will try to use
.. machine learning technics to create a real time controller learned from
.. QOPS solver.
.. 
.. A set of optimal trajectories for several random targets are computed by
.. our solver (QOPS). These trajectories are played and learned by our
.. adaptive controler/system/machine learning system (XCSF)
.. 
.. image des trajectoires apprises
.. 
.. Second step: the generalisation test adaptive system learned several ...
.. we check whether it's capable to generalize what it learned to other
.. targets
.. 
.. image des trajectoires jouées
.. 
.. graph des résultats
.. 
.. conclusion: ok


Dependencies
============

-  Python >= 2.5
-  Numpy_
-  Matplotlib_ >= 0.98.1

.. -  ffmpeg2theora (screencast) [optional]
.. -  PIL (screencast) [optional]

Note:

    If you use ``pip`` to install PyArm, Numpy and Matplotlib will be
    automatically downloaded and installed (see the following install_
    section).


.. _install:

Installation
============

Gnu/Linux
---------

You can install, upgrade, uninstall PyArm with these commands (in a
terminal)::

    pip install --pre pyarm12
    pip install --upgrade pyarm12
    pip uninstall pyarm

Or, if you have downloaded the PyArm source code::

    python3 setup.py install

.. There's also a package for Debian/Ubuntu::
.. 
..     sudo apt-get install pyarm

Windows
-------

Note:

    The following installation procedure has been tested to work with Python
    3.4 under Windows 7.
    It should also work with recent Windows systems.

You can install, upgrade, uninstall PyArm with these commands (in a
`command prompt`_)::

    py -m pip install --pre pyarm
    py -m pip install --upgrade pyarm
    py -m pip uninstall pyarm

Or, if you have downloaded the PyArm source code::

    py setup.py install

MacOSX
-------

Note:

    The following installation procedure has been tested to work with Python
    3.4 under MacOSX 10.6 (*Snow Leopard*).
    It should also work with recent MacOSX systems.

You can install, upgrade, uninstall PyArm with these commands (in a
terminal)::

    pip install --pre pyarm
    pip install --upgrade pyarm
    pip uninstall pyarm

Or, if you have downloaded the PyArm source code::

    python3 setup.py install


Documentation
=============

.. PyArm documentation is available on the following page:
.. 
..     http://pyarm.rtfd.org/

- Online Documentation: http://pyarm.readthedocs.org
- API Documentation: http://pyarm.readthedocs.org/en/latest/api.html


Run pyarm
=========

To run Pyarm, simply type in a terminal::

    pyarm


Usage example
=============

Use the following command to run simulations with graphs and logs using
the *Mitrovic* muscle model described in the `technical report`_ and a
*sigmoid* controler::

    pyarm -f -l -m mitrovic -d 0.005 -A sigmoid

The following command run a simulation with the *sagittal* arm model and
the *kambara* muscle model using a *sigmoid* controller::

    pyarm -a sagittal -m kambara -d 0.005 -A sigmoid


Help
====

A comprehensive list of available options is printed with the following
command::

    pyarm -h


Bug reports
===========

To search for bugs or report them, please use the PyArm Bug Tracker at:

    https://github.com/jeremiedecock/pyarm/issues


License
=======

The ``PyArm`` library is provided under the terms and conditions of the
`MIT License`_.


.. _Pyarm: http://www.jdhp.org/projects_en.html#pyarm
.. _MIT License: http://opensource.org/licenses/MIT
.. _technical report: http://download.tuxfamily.org/jdhp/pdf/pyarm.pdf
.. _Institute for Intelligent Systems and Robotics: http://www.isir.upmc.fr/
.. _Numpy: http://www.numpy.org/
.. _Matplotlib: http://matplotlib.org/

