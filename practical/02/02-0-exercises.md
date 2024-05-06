# Exercises

1. Use Stable Diffusion XL in a Google Colab session to generate an image from the following prompt[^tsds]
   > Students of [insert PhD] enjoying a lecture on [insert meme topic from your PhD] in a classroom with a marvelous view of the Mediterranean Sea. The teacher is wearing an over-the-top clown costume and juggling four-dimensional balls. Surrealist painting in the style of Salvador Dali.

   [This notebook](https://colab.research.google.com/github/wandb/examples/blob/master/colabs/diffusers/sdxl-text-to-image.ipynb) can be a convenient starting point:
    - Try to simplify it as much as you can in order to better understand what's going on. Skip the refinement.
    - Explore what happens if you don't set `variant='fp16', torch_dtype=torch.float16` or, for some reason, you don't use the GPU.
    - Bonus: benchmark/profile/inspect GPU memory and compute usage during inference.

[^tsds]: suggested values for TSDS: "data science" and "PCA"

2. Train Stable Diffusion XL on Google Colab. Just kidding, train any network to do anything (useful or not) on Colab or elsewhere on a GPU or CPU, using PyTorch Lightning.
    - Visualise the training and validation losses in real time using Tensorboard and/or Weights & Biases.
    - Evaluate (predict) the network on some concrete test example, make some kind of plot to demonstrate this and log it to Tensorboard / W&B repeatedly (e.g. every epoch) as the network is training (use a Callback).
    - Save checkpoints; after training, figure out which is the "best" one and load it in another notebook and evaluate your network.
    - Bonus: log your network structure to Tensorboard and/or visualise it.
    - Bonus: log histograms of the network weights during training to W&B.
    - Bonus: publish your super useful network on Huggingface.