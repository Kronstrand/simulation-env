alpha = 0.1
gamma = 0.95

#Q-learning with temporal difference
def Q_learning_TD(Q_value, next_max_Q_value, reward):
    return Q_value + alpha * (reward + gamma * next_max_Q_value - Q_value)