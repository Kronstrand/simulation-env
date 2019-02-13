import env

saved_Q_table = dict()

#train
for i in range(100):
    saved_Q_table = env.run(Q_table=saved_Q_table, render=False, learn=True, playable=False)

#run
env.run(Q_table=saved_Q_table, render=True, learn=False, playable=False)

