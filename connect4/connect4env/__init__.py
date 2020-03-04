from gym.envs.registration import register

register(
    id='tttenv-v0',
    entry_point='tttenv.envs:TicTacToeEnv',
)
