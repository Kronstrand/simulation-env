alpha = 0.90
gamma = 0.90

#Q-learning with temporal difference
def Q_learning_TD(Q_value, next_max_Q_value, reward):
    return Q_value + alpha * (reward + gamma * next_max_Q_value - Q_value)

