from gym.envs.registration import register

register(
    id='connect4env-v0',
    entry_point='connect4env.envs:Connect4Env',
)
