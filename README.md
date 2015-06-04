# [Pyarm](https://github.com/jeremiedecock/pyarm)

Copyright (c) 2010 Jeremie DECOCK (http://www.jdhp.org)

## Description

Pyarm is a physics simulator which provide an anthropomorphic arm model for
experiments on human like motor control. 

The arm model is described in the following technical report (written in
French): http://download.tuxfamily.org/jdhp/pdf/pyarm.pdf .

Pyarm has been used at the [Institute for Intelligent Systems and Robotics](http://www.isir.upmc.fr/)
for experiments on adaptive systems.
These experiments are described in the following academic paper "Learning
cost-efficient control policies with XCSF: generalization capabilities and
further improvement" by Didier Marin, Jérémie Decock, Lionel Rigoux and Olivier
Sigaud.
This scientific contribution has been published in the "Proceedings of the 13th
annual conference on Genetic and evolutionary computation (GECCO'11)", the main
international conference on genetic and evolutionary computation.
This paper can be downloaded on [www.jdhp.org](http://www.jdhp.org/articles_en.html#XCSF).

## Pyarm dependencies

* Python >=2.5
* Numpy
* Matplotlib >=0.98.1
* Tkinter (Python graphical user interface)
* ffmpeg2theora (screencast) [optional]
* PIL (screencast) [optional]

## Install

Pyarm can be installed with Python Distutils by entering the following command
in a terminal:

```
python setup.py install
```

## Run pyarm

To run Pyarm, simply type in a terminal:

```
pyarm
```

## Usage example

Use the following command to run simulations with graphs and logs using the "Mitrovic" muscle model
described in the [technical report](http://download.tuxfamily.org/jdhp/pdf/pyarm.pdf)
and a "sigmoid" controler: 

```
pyarm -f -l -m mitrovic -d 0.005 -A sigmoid
```

The following command run a simulation with the "sagittal" arm model and the
"kambara" muscle model using a "sigmoid" controller, 

```
pyarm -a sagittal -m kambara -d 0.005 -A sigmoid
```

## Help

A comprehensive list of available options is printed with the following command:

```
pyarm -h
```

## License

Pyarm is distributed under the [MIT License](http://opensource.org/licenses/MIT).
