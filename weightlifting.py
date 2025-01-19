import numpy as np
import random

# Actuator ID mappings
ACTUATOR_NAME_TO_ID = {
    "left_shoulder_yaw": 11,
    "left_shoulder_pitch": 12,
    "left_elbow_yaw": 13,
    "left_gripper": 14,
    "right_shoulder_yaw": 21,
    "right_shoulder_pitch": 22,
    "right_elbow_yaw": 23,
    "right_gripper": 24,
    "left_hip_yaw": 31,
    "left_hip_roll": 32,
    "left_hip_pitch": 33,
    "left_knee_pitch": 34,
    "left_ankle_pitch": 35,
    "right_hip_yaw": 41,
    "right_hip_roll": 42,
    "right_hip_pitch": 43,
    "right_knee_pitch": 44,
    "right_ankle_pitch": 45,
}
ACTUATOR_ID_TO_NAME = {v: k for k, v in ACTUATOR_NAME_TO_ID.items()}

# Fitness function to evaluate configurations
def fitness_function(parameters):
    """
    Evaluate the weight lifted based on robot's joint parameters.
    Parameters: Array of joint angles/torques (18 elements).
    Returns: A fitness score (higher is better).
    """
    # Placeholder: Replace with the actual function that computes weight-lifting capability.
    weight_lifted = sum(parameters)  # Simplified example
    constraints = np.all((parameters >= -1.0) & (parameters <= 1.0))  # Joint angle limits
    return weight_lifted if constraints else -np.inf

# MCMC Parameters
n_joints = 18  # Number of joints to optimize
n_iterations = 10000  # Number of MCMC iterations
proposal_stddev = 0.1  # Standard deviation for proposal distribution

# Initialize parameters randomly within valid range
current_params = np.random.uniform(-1.0, 1.0, n_joints)
current_fitness = fitness_function(current_params)
best_params = current_params.copy()
best_fitness = current_fitness

# MCMC Sampling
for iteration in range(n_iterations):
    # Propose new parameters by adding Gaussian noise
    proposed_params = current_params + np.random.normal(0, proposal_stddev, n_joints)
    proposed_fitness = fitness_function(proposed_params)
    
    # Metropolis-Hastings acceptance criterion
    acceptance_probability = min(1, np.exp(proposed_fitness - current_fitness))
    if random.uniform(0, 1) < acceptance_probability:
        current_params = proposed_params
        current_fitness = proposed_fitness
    
    # Track the best solution
    if current_fitness > best_fitness:
        best_params = current_params
        best_fitness = current_fitness
    
    # Print progress occasionally
    if iteration % 1000 == 0:
        print(f"Iteration {iteration}: Best Fitness = {best_fitness}")

# Output results
print("Optimized Joint Parameters (IDs):", dict(zip(ACTUATOR_NAME_TO_ID.keys(), best_params)))
print("Maximum Weight Lifted (Fitness):", best_fitness)
