import gymnasium as gym
from gymnasium import spaces
import numpy as np
from flappybird import FlappyBird

class FlappyBirdEnv(gym.Env):
    def __init__(self, render_mode=False):
        super(FlappyBirdEnv, self).__init__()
        self.juego = FlappyBird()
        self.render_mode = render_mode

        self.action_space = spaces.Discrete(2)

        # Limites reales de cada observacion
        self.observation_space = spaces.Box(
            low=np.array( [0.0,  -10.0, 0.0,  100.0], dtype=np.float32),
            high=np.array([600.0, 15.0, 700.0, 450.0], dtype=np.float32),
        )

    def _get_obs(self):
        estado = self.juego.get_state()
        return np.array([
            estado["pajaro_y"],    # 0 a 600
            estado["pajaro_vel"],  # -8 a ~10
            estado["tubo_x"],      # 0 a 700
            estado["tubo_y"],      # 150 a 380
        ], dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.juego.reset()
        return self._get_obs(), {}

    def step(self, action):
        _, recompensa, terminado = self.juego.step(action)
        observacion = self._get_obs()

        if self.render_mode:
            self.juego.render()

        return observacion, recompensa, terminado, False, {}