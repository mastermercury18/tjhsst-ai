import random 
import math
import numpy as np

def random_bandits(num_moves, bandit_means):
    total_reward = 0.0
    for move in range(num_moves):
        bandit = random.choice(bandit_means)
        reward = random.normalvariate(bandit, 1)
        total_reward += reward 
    return total_reward

def epsilon_greedy_bandit(bandit_means, epsilon, num_moves):
    num_bandits = len(bandit_means)
    q_vals = [0.0] * num_bandits
    counts = [0.0] * num_bandits
    total_reward = 0.0
    for move in range(num_moves):
        if random.random() < epsilon:
            bandit = random.choice(bandit_means)
        else:
            bandit_pos = np.argmax(q_vals)
            bandit = bandit_means[bandit_pos]
        reward = random.normalvariate(bandit, 1)
        bandit_pos = bandit_means.index(bandit)
        counts[bandit_pos] += 1
        qval = (reward - q_vals[bandit_pos]) / counts[bandit_pos]
        q_vals[bandit_pos] += qval
        total_reward += reward
    return total_reward 

def greedy_ucb_bandit(bandit_means, num_moves):
    num_bandits = len(bandit_means)
    q_vals = [0.0] * num_bandits
    counts = [0] * num_bandits
    total_reward = 0.0
    for move in range(1, num_moves + 1):
        uncertainties = []
        for num in range(num_bandits):
            if counts[num] == 0:
                ucb_val = float('inf')
            else:
                ucb_val = q_vals[num] + math.sqrt((2 * math.log(move)) / counts[num])
            uncertainties.append(ucb_val)
        bandit_pos = np.argmax(uncertainties)
        reward = random.normalvariate(bandit_means[bandit_pos], 1)
        counts[bandit_pos] += 1
        q_val = (reward - q_vals[bandit_pos]) / counts[bandit_pos]
        q_vals[bandit_pos] += q_val
        total_reward += reward
    return total_reward

def epsilon_ucb_bandit(bandit_means, epsilon, num_moves):
    num_bandits = len(bandit_means)
    q_vals = [0.0] * num_bandits
    counts = [0] * num_bandits
    total_reward = 0.0
    for move in range(1, num_moves + 1):
        if random.random() < epsilon:
            bandit_pos = random.randint(0, num_bandits - 1)
        else:
            uncertainties = []
            for i in range(num_bandits):
                if counts[i] == 0:
                    ucb_val = float('inf')
                else:
                    ucb_val = q_vals[i] + math.sqrt((2 * math.log(move)) / counts[i])
                uncertainties.append(ucb_val)
            bandit_pos = np.argmax(uncertainties)
        reward = random.normalvariate(bandit_means[bandit_pos], 1)
        counts[bandit_pos] += 1
        q_val = (reward - q_vals[bandit_pos]) / counts[bandit_pos]
        q_vals[bandit_pos] += q_val
        total_reward += reward
    return total_reward

def run_bandit_simulations():
    num_bandits = 10
    num_games = 200
    num_moves = 2000
    epsilon_values = [0, 0.001, 0.01, 0.1, 0.5, 1]
    num_trials = 1

    all_results = {epsilon: [] for epsilon in epsilon_values}
    ideal_scores = []
    random_results = []
    greedy_ucb_scores = []
    epsilon_ucb_scores = []

    for _ in range(num_trials):
        bandit_means = []
        for i in range(num_bandits):
            bandit_means.append(random.normalvariate(0, 1))
        ideal_score = max(bandit_means) * num_moves
        ideal_scores.append(ideal_score)
        
        for epsilon in epsilon_values:
            game_scores = []
            for _ in range(num_games):
                if epsilon == 1:
                    total_reward = random_bandits(num_moves, bandit_means)
                    random_results.append(total_reward)
                else:
                    total_reward = epsilon_greedy_bandit(bandit_means, epsilon, num_moves)
                game_scores.append(total_reward)
            avg_score = np.mean(game_scores)
            all_results[epsilon].append(avg_score)

        avg_results = {epsilon: np.mean(scores) for epsilon, scores in all_results.items()}
        best_epsilon = max(avg_results, key=avg_results.get)

        greedy_ucb_game_scores = []
        epsilon_ucb_game_scores = []

        for _ in range(num_games):
            total_reward_greedy_ucb = greedy_ucb_bandit(bandit_means, num_moves)
            total_reward_epsilon_ucb = epsilon_ucb_bandit(bandit_means, best_epsilon, num_moves)
            greedy_ucb_game_scores.append(total_reward_greedy_ucb)
            epsilon_ucb_game_scores.append(total_reward_epsilon_ucb)

        greedy_ucb_scores.append(np.mean(greedy_ucb_game_scores))
        epsilon_ucb_scores.append(np.mean(epsilon_ucb_game_scores))

    avg_results = {epsilon: np.mean(scores) for epsilon, scores in all_results.items()}
    avg_ideal_score = np.mean(ideal_scores)
    avg_random_score = np.mean(random_results)
    avg_greedy_ucb_score = np.mean(greedy_ucb_scores)
    avg_epsilon_ucb_score = np.mean(epsilon_ucb_scores)

    return avg_results, avg_ideal_score, avg_greedy_ucb_score, avg_epsilon_ucb_score, avg_random_score

avg_results, avg_ideal_score, avg_greedy_ucb_score, avg_epsilon_ucb_score, avg_random_score = run_bandit_simulations() 
print("Random: " + str(avg_random_score))
print("0.001-greedy: " + str(avg_results[0.001]))
print("0.01-greedy: " + str(avg_results[0.01]))
print("0.1-greedy: " + str(avg_results[0.1]))
print("0.5-greedy: " + str(avg_results[0.5]))
print("Greedy: " + str(avg_results[0]))
print("Greedy w/ UCB: " + str(avg_greedy_ucb_score))
fav_epsilon = max(avg_results, key=lambda k: avg_results[k])
print("Epsilon " + str(fav_epsilon) + "-greedy w/ UCB: " + str(avg_epsilon_ucb_score))
print("Ideal score: " + str(avg_ideal_score))