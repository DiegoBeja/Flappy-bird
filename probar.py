import pygame
from stable_baselines3 import PPO
from flappy_env import FlappyBirdEnv

pygame.init()
clock = pygame.time.Clock()

env = FlappyBirdEnv(render_mode=True)
model = PPO.load("Modelo/best_model")

obs, _ = env.reset()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    action, _ = model.predict(obs, deterministic=True)

    obs, reward, done, _, _ = env.step(action)

    clock.tick(200)

    if done:
        obs, _ = env.reset()