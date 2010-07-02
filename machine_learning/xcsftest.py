#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import xcsfpython as xp
import time

def main():

    # Init
    from model.muscle import weiwei_muscle_model
    from model.arm import weiwei_arm_model

    weiwei_arm = weiwei_arm_model.ArmModel()
    weiwei_muscle = weiwei_muscle_model.MuscleModel(weiwei_arm)

    # Learn and plot
    learn_fl(weiwei_muscle)


def learn_fl(muscle):
    xcsf = xp.XCSF(host='127.0.0.1', configFilePath='xcsf.ini')
    xcsf.initialize(1, 1)

    # Learn datas ###############
    n = 5000
    for it in range(n):
        lm = np.random.random(1) * 0.6
        fl = muscle.fl(lm)
        xcsf.update(lm, fl)
        print it, '/', n

    # Plot datas ################
    plt.clf()

    # Build datas ###############
    n = 50
    lm = np.linspace(muscle.ml_min, muscle.ml_max, n)
    fl = muscle.fl(lm)

    # XCSF server ne peut prédire qu'un seul exemple à la fois
    pred = []
    for inp in lm:
        pred.append(xcsf.predict(np.array([inp])))
    pred = np.array(pred)

    # Close xcsf
    xcsf.close()

    # Plot data #################
    plt.xlabel('Muscle length (m)')
    plt.ylabel('fl : Force-length relationship')
    plt.title(muscle.name)

    plt.plot(lm, pred, 'k--', lm, fl, 'k')
    plt.legend(('Prediction', 'Actual values'),
               'upper center', shadow=True, fancybox=True)

    plt.savefig('muscle_learn_' + muscle.name + '_fl.png')


if __name__ == '__main__':
    main()

