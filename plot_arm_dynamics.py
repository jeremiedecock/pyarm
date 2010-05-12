from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

def plot_C(arm):
    plot_C_forearm(arm)
    plot_C_upperarm(arm)

def plot_C_forearm(arm):

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

    plt.savefig('c_forearm.png')
    plt.show()

    
def plot_C_upperarm(arm):
    
    # Build datas ###############
    n  = 50
    nf = 10

    o1 = np.linspace(arm.omegamin, arm.omegamax, n)
    o2 = np.linspace(arm.omegamin, arm.omegamax, n)
    t2 = np.linspace(arm.theta_limit[1]['min'], arm.theta_limit[1]['max'], nf)

    o1_, o2_ = np.meshgrid(o1, o2)

    for t in range(len(t2)):
        z = np.zeros([len(o1), len(o2)])
        for i in range(len(o1)):
            for j in range(len(o2)):
                z[j, i] = arm.C(np.array([0, t2[t]]), np.array([o1[i], o2[j]]))[0]

        # Plot data #################
        fig = plt.figure()
        ax = axes3d.Axes3D(fig)
        ax.cla()

        ax.plot_wireframe(o1_, o2_, z)

        ax.set_xlabel('Elbow joint angle (rad)')
        ax.set_ylabel('Shoulder velocity (rad/s)')
        ax.set_zlabel('Centrifugal, coriolis and friction forces applied on forearm')

        #plt.savefig('c_upperarm_' + str(t) + '.png')
        plt.clf()
        fig.clf()


