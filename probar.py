import pygame
from stable_baselines3 import PPO
from flappy_env import FlappyBirdEnv

pygame.init()
clock = pygame.time.Clock()

env = FlappyBirdEnv(render_mode=True)
model = PPO.load("Modelo/best_model")

obs, _ = env.reset()

while True:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _, _ = env.step(action)
    clock.tick(60)
    if done:
        obs, _ = env.reset()