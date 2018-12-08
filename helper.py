import numpy as np
import gym
import gym_gridworlds
env = gym.make('WindyGridworld-v0')
env.reset()


def cartesian(arrays, out=None):
    """
    Generate a cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out
	
	
def visualize_path(Q,initial_state = None):
    tot_reward = 0
    if initial_state == None:
        current_state = env.reset()
    else:
        env.S= initial_state
        current_state = initial_state
    cnt = 0 
    #env.S= (3,4)
    #current_state = (3,4)
    path = str(current_state)
    grid = np.zeros([7,10])
    grid_uni =  -1 + np.zeros([7,10])
    for step in range(100):
        #print current_state
        grid[current_state[0],current_state[1]] = 1
        next_action = np.argmax(Q[10 * current_state[0] + current_state[1]])
        next_state,reward,done, info = env.step(next_action)
        grid_uni[current_state[0],current_state[1]] = next_action
        tot_reward = tot_reward + reward
        current_state = next_state
        cnt = cnt + 1
        path = path + " => " + str(current_state)
        #print current_state
        if done:
            #print("Finished after {} timesteps".format(t+1))
            grid_uni[current_state[0],current_state[1]] = -1
            print path
            break
    print tot_reward,cnt
    #print grid
    import sys
    for i in range(7):
        for j in range(10):

            if i == 3 and j == 7:
                    sys.stdout.write(u'\u270c ')
                    continue
            if grid_uni[i][j] == -1:
                sys.stdout.write(u'\u23f9 ')
                continue

            if grid_uni[i][j]==0:
                sys.stdout.write(u'\u2b9d ')
            elif grid_uni[i][j] == 1:
                if i == 3 and j == 0:
                    sys.stdout.write(u'\u2b9e  ')
                else:
                    sys.stdout.write(u'\u2b9e ')
            elif grid_uni[i][j] == 2:
                sys.stdout.write(u'\u2b9f ')
            elif grid_uni[i][j] == 3:
                sys.stdout.write(u'\u2b9c ')
            else:
                sys.stdout.write(u'\u270c ')
        sys.stdout.write("\n")        