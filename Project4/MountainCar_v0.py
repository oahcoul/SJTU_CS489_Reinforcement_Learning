# MountainCar_v0.py

import gym
import numpy as np
from matplotlib import pyplot as plt
from RL_brain import DeepQNetwork
import time

# Environment
env = gym.make("MountainCar-v0")
# Remove the limits(e.g. step limits) in environment encapsulation
env = env.unwrapped

# Instantiation of DQN
model = DeepQNetwork(n_actions=3, n_features=2, neurons_num=10, learning_rate=0.0001, epsilon_greedy=0.9, replace_target_iter=300,
                     buffer_size=3000, epsilon_greedy_increment=0.0002)


# Step list
step_list = []
# Average action value
action_value = []
# Episode cost list
episode_cost_list = []
# Episode time list
episode_time_list = []


# Plot
def plot_info():
    # Plot step list
    step_list_x = np.arange(len(step_list))
    plt.plot(step_list_x, step_list)
    plt.xlabel("Epochs")
    plt.ylabel("Step of episode")
    plt.savefig("./output/step_list")
    plt.show()

    # Plot average action value
    action_value_x = np.arange(len(action_value))
    plt.plot(action_value_x, action_value)
    plt.xlabel("Epochs")
    plt.ylabel("Average action value")
    plt.savefig("./output/action_value")
    plt.show()

    # Plot episode cost list
    episode_cost_list_x = np.arange(len(episode_cost_list))
    plt.plot(episode_cost_list_x, episode_cost_list)
    plt.xlabel("Epochs")
    plt.ylabel("Episode cost")
    plt.savefig("./output/episode_cost_list")
    plt.show()

    # Plot episode time list
    episode_time_list_x = np.arange(len(episode_time_list))
    plt.plot(episode_time_list_x, episode_time_list)
    plt.xlabel("Epochs")
    plt.ylabel("Episode time")
    plt.savefig("./output/episode_time_list")
    plt.show()

    # Plot step cost
    model.plot_cost_curve()


if __name__ == '__main__':
    # Total episodes
    total_episodes = 200
    # Step counter
    steps_counter = 0

    for i in range(total_episodes):
        # Observation
        observation = env.reset()
        # Total reward in an episode
        episode_reward = 0
        tmp_steps = 0

        # Clear self.episode_cost
        model.episode_cost = 0

        # Time mark
        time_mark = time.time()

        while True:
            # Render the environment
            env.render()
            # Choose action
            action = model.choose_action(observation=observation)
            # Get feedback from environment
            new_observation, reward, done, info = env.step(action)
            # Parse the observation
            position, velocity = new_observation
            # Reward policy: the higher, the better
            reward = abs(position - (-0.5))

            # Store the transition
            model.store_transition(observation, action, reward, new_observation)

            # Learn
            if steps_counter > 1000:
                model.learn()
            # Update reward
            episode_reward += reward

            # If done
            if done:
                message = "| Get" if new_observation[0] >= env.unwrapped.goal_position else "| ----"
                print("Episode:", i, message, "| Episode reward:", round(episode_reward, 3),
                      "| Episode steps:", tmp_steps,
                      "| Episode cost:", round(model.episode_cost, 3),
                      "| Episode time", round(time.time() - time_mark, 3), "seconds")
                break

            # If not done
            # Transform state
            observation = new_observation
            steps_counter += 1
            tmp_steps += 1

        # Update average action value
        action_value.append(float(episode_reward / tmp_steps))
        # Update steps list
        step_list.append(tmp_steps)
        # Update episode cost list
        episode_cost_list.append(model.episode_cost)
        # Update episode time list
        episode_time_list.append(round(time.time() - time_mark))

    # Plot
    plot_info()


