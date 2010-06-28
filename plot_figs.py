from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

def main():

    # Init
    from model.muscle.forward_dynamics import kambara_muscle_model
    from model.muscle.forward_dynamics import mitrovic_muscle_model
    from model.muscle.forward_dynamics import weiwei_muscle_model

    from model.arm.forward_dynamics import kambara_arm_model
    from model.arm.forward_dynamics import mitrovic_arm_model
    from model.arm.forward_dynamics import weiwei_arm_model

    kambara_arm  = kambara_arm_model.ArmModel()
    mitrovic_arm = mitrovic_arm_model.ArmModel()
    weiwei_arm   = weiwei_arm_model.ArmModel()

    kambara_muscle  = kambara_muscle_model.MuscleModel(kambara_arm.theta)
    mitrovic_muscle = mitrovic_muscle_model.MuscleModel(mitrovic_arm.theta)
    weiwei_muscle   = weiwei_muscle_model.MuscleModel(weiwei_arm.theta)

    # Plot
    plot_lm(kambara_arm, kambara_muscle)
    plot_lm(mitrovic_arm, mitrovic_muscle)

    plot_k(kambara_muscle)
    plot_k(mitrovic_muscle)

    plot_v(kambara_muscle)
    plot_v(mitrovic_muscle)

    plot_lr(kambara_muscle)
    plot_lr(mitrovic_muscle)

    plot_nf(weiwei_muscle)
    plot_fp(weiwei_muscle)
    plot_fl(weiwei_muscle)
    plot_fv(weiwei_muscle)
    plot_fa(weiwei_muscle)

    plot_c_forearm(kambara_arm)
    plot_c_forearm(mitrovic_arm)


def plot_lm(arm, muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    qmin = min(arm.theta_bounds[0]['min'], arm.theta_bounds[1]['min'])
    qmax = max(arm.theta_bounds[0]['max'], arm.theta_bounds[1]['max'])
    q = np.linspace(qmin, qmax, n)

    lm = np.zeros([len(q), 6])
    for i in range(len(q)):
        arm.theta = np.ones(2) * q[i]
        arm.bound_joint_angles()
        lm[i] = muscle.lm(arm.theta)

    # Plot data #################
    plt.xlabel('Angle')
    plt.ylabel('Muscle length')
    plt.title(muscle.name)
    plt.plot(q, lm)
    plt.legend(muscle.legend, loc='best', prop={'size':'x-small'})

    plt.savefig('muscle_' + muscle.name + '_lm.png')

def plot_k(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    u = np.linspace(0, 1, n)

    k = np.zeros([len(u), 6])
    for i in range(len(u)):
        k[i] = muscle.K(np.ones(6) * u[i])

    # Plot data #################
    plt.xlabel('Control signal')
    plt.ylabel('Elastic force')
    plt.title(muscle.name)
    plt.plot(u, k)
    plt.legend(muscle.legend, loc='best', prop={'size':'x-small'})

    plt.savefig('muscle_' + muscle.name + '_k.png')

def plot_v(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    u = np.linspace(0, 1, n)

    v = np.zeros([len(u), 6])
    for i in range(len(u)):
        v[i] = muscle.B(np.ones(6) * u[i])

    # Plot data #################
    plt.xlabel('Control signal')
    plt.ylabel('Viscosity force')
    plt.title(muscle.name)
    plt.plot(u, v)
    plt.legend(muscle.legend, loc='best', prop={'size':'x-small'})

    plt.savefig('muscle_' + muscle.name + '_v.png')

def plot_lr(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    u = np.linspace(0, 1, n)

    lr = np.zeros([len(u), 6])
    for i in range(len(u)):
        lr[i] = muscle.lr(np.ones(6) * u[i])

    # Plot data #################
    plt.xlabel('Control signal')
    plt.ylabel('Rest length')
    plt.title(muscle.name)
    plt.plot(u, lr)
    plt.legend(muscle.legend, loc='best', prop={'size':'x-small'})

    plt.savefig('muscle_' + muscle.name + '_lr.png')

def plot_nf(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    lm = np.linspace(muscle.ml_min, muscle.ml_max, n)

    nf = muscle.nf(lm)

    # Plot data #################
    plt.xlabel('Muscle length (m)')
    plt.ylabel('nf (?)')
    plt.title(muscle.name)
    plt.plot(lm, nf)

    plt.savefig('muscle_' + muscle.name + '_nf.png')

def plot_fp(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    lm = np.linspace(muscle.ml_min, muscle.ml_max, n)

    fe = muscle.fe(lm)

    # Plot data #################
    plt.xlabel('Muscle length (m)')
    plt.ylabel('fe : Elastic force')
    plt.title(muscle.name)
    plt.plot(lm, fe)

    plt.savefig('muscle_' + muscle.name + '_fe.png')

def plot_fl(muscle):
    
    plt.clf()

    # Build datas ###############
    n = 50
    lm = np.linspace(muscle.ml_min, muscle.ml_max, n)

    fl = muscle.fl(lm)

    # Plot data #################
    plt.xlabel('Muscle length (m)')
    plt.ylabel('fl : Force-length relationship')
    plt.title(muscle.name)
    plt.plot(lm, fl)

    plt.savefig('muscle_' + muscle.name + '_fl.png')


def plot_fv(muscle):

    # Build datas ###############
    n = 50
    x = np.linspace(muscle.ml_min, muscle.ml_max, n)
    y = np.linspace(muscle.mv_min, muscle.mv_max, n)

    z = np.zeros([len(x), len(y)])
    for i in range(len(x)):
        for j in range(len(y)):
            # !!! c'est bien z[j, i] et non pas z[i, j] (sinon, c pas en phase ac le meshgrid) !!!
            z[j, i] = muscle.fv(np.ones(6) * x[i], np.ones(6) * y[j])[0]

    x, y = np.meshgrid(x, y)

    # Plot data #################
    fig = plt.figure()
    ax = axes3d.Axes3D(fig)
    ax.plot_wireframe(x, y, z)

    ax.set_xlabel('Muscle length (m)')
    ax.set_ylabel('Muscle velocity (m/s)')
    ax.set_zlabel('fv : Force-velocity relationship')

    plt.savefig('muscle_' + muscle.name + '_fv.png')


def plot_fa(muscle):

    # Build datas ###############
    n = 50
    x = np.linspace(muscle.ml_min, muscle.ml_max, n)
    y = np.linspace(0., 1., n)

    z = np.zeros([len(x), len(y)])
    for i in range(len(x)):
        for j in range(len(y)):
            # !!! c'est bien z[j, i] et non pas z[i, j] (sinon, c pas en phase ac le meshgrid) !!!
            z[j, i] = muscle.fa(x[i], y[j])

    x, y = np.meshgrid(x, y)

    # Plot data #################
    fig = plt.figure()
    ax = axes3d.Axes3D(fig)
    ax.plot_wireframe(x, y, z)

    ax.set_xlabel('Muscle length (m)')
    ax.set_ylabel('Motor signal')
    ax.set_zlabel('fa : Activation-frequency relationship')

    plt.savefig('muscle_' + muscle.name + '_fa.png')


def plot_c_forearm(arm):

    # Build datas ###############
    n = 50
    x = np.linspace(arm.theta_bounds[1]['min'], arm.theta_bounds[1]['max'], n)
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

    plt.savefig('arm_' + arm.name + '_c_forearm.png')

    
def plot_c_upperarm(arm):
    
    # Build datas ###############
    n  = 50
    nf = 10

    o1 = np.linspace(arm.omegamin, arm.omegamax, n)
    o2 = np.linspace(arm.omegamin, arm.omegamax, n)
    t2 = np.linspace(arm.theta_bounds[1]['min'], arm.theta_bounds[1]['max'], nf)

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

if __name__ == '__main__':
    main()


