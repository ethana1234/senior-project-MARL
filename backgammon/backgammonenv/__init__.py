from gym.envs.registration import register

register(
    id='backgammonenv-v0',
    entry_point='backgammonenv.envs:BackgammonEnv',
)
