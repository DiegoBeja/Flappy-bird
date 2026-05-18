from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from flappy_env import FlappyBirdEnv

env = FlappyBirdEnv(render_mode=True)
eval_env = FlappyBirdEnv(render_mode=False)

# Guarda automaticamente el modelo cuando alcanza su mejor reward
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path="./",
    log_path="./logs/",
    eval_freq=10000,
    n_eval_episodes=5,
    deterministic=True,
    verbose=1
)

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate=0.00015,
    n_steps=4096,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    policy_kwargs=dict(net_arch=[128, 128]),
)

model.learn(total_timesteps=1_000_000, callback=eval_callback)
env.close()
eval_env.close()
print("Listo! Mejor modelo guardado como 'best_model.zip'")