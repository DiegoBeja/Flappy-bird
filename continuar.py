from stable_baselines3 import PPO
from flappy_env import FlappyBirdEnv

env = FlappyBirdEnv(render_mode=True)

model = PPO.load("Modelo/ia_flappy_ppo", env=env)
model.learn(total_timesteps=500_000)
model.save("ia_flappy_ppo")

env.close()
print("Listo!")