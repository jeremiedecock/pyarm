from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

def plotC(arm):

    # Build datas ###############

    n = 50
    x = np.linspace(arm.theta_limit[1]['min'], arm.theta_limit[1]['max'], n)
    y = np.linspace(arm.omegamin, arm.omegamax, n)

    z = np.zeros([len(x), len(y)])
    for i in range(len(x)):
        for j in range(len(y)):
            # !!! c'est bien z[j, i] et non pas z[i, j] (sinon, c pas en phase ac le meshgrid) !!!
            z[j, i] = arm.C(np.array([0, x[i]]), np.array([y[j], 0]))[1]

    x, y = np.meshgrid(x, y)

    # Plot data #################

    fig = plt.figure()
    ax = axes3d.Axes3D(fig)
    ax.plot_wireframe(x, y, z)

    ax.set_xlabel('Elbow joint angle (rad)')
    ax.set_ylabel('Shoulder velocity (rad/s)')
    ax.set_zlabel('Centrifugal, coriolis and friction forces applied on forearm')

    plt.show()