# Exercises

## 1. Google Colab

Use Stable Diffusion XL in a Google Colab session to generate an image from the following prompt[^tsds]
    > Students of [insert PhD] enjoying a lecture on [insert meme topic from your PhD] in a classroom with a marvelous view of the Mediterranean Sea. The teacher is wearing an over-the-top clown costume and juggling four-dimensional balls. Surrealist painting in the style of Salvador Dali.

    [This notebook](https://colab.research.google.com/github/wandb/examples/blob/master/colabs/diffusers/sdxl-text-to-image.ipynb) can be a convenient starting point:
    - Try to simplify it as much as you can in order to better understand what's going on. Skip the refinement.
    - Explore what happens if you don't set `variant='fp16', torch_dtype=torch.float16` or, for some reason, you don't use the GPU.
    - Bonus: benchmark/profile/inspect GPU memory and compute usage during inference.

[^tsds]: suggested values for TSDS: "data science" and "PCA"

## 2. PyTorch Lightning

Train Stable Diffusion XL on Google Colab.

Just kidding, train any network to do anything (useful or not) on Colab or elsewhere on a GPU or CPU, using PyTorch Lightning.
- Visualise the training and validation losses in real time using Tensorboard and/or Weights & Biases.
- Evaluate (predict) the network on some concrete test example, make some kind of plot to demonstrate this and log it to Tensorboard / W&B repeatedly (e.g. every epoch) as the network is training (use a Callback).
- Save checkpoints; after training, figure out which is the "best" one and load it in another notebook and evaluate your network.
- Bonus: [log your network architecture](https://pytorch.org/docs/stable/tensorboard.html#torch.utils.tensorboard.writer.SummaryWriter.add_graph) to Tensorboard and/or visualise it.
- Bonus: [log gradients and histograms](https://docs.wandb.ai/ref/python/watch) of the network weights during training to W&B.
- Bonus: [publish](https://huggingface.co/docs/hub/en/models-uploading) your super useful network on [Huggingface](https://huggingface.co/).

---

Here are a few suggestions:
- image classification:
  - [MNIST](https://pytorch.org/vision/stable/generated/torchvision.datasets.MNIST.html), if you really want to cover your basics;
  - [Imagenette](https://pytorch.org/vision/stable/generated/torchvision.datasets.Imagenette.html) is similar but less basic;
   - [Imagewoof](https://github.com/fastai/imagenette?tab=readme-ov-file#imagewoof) if that's too easy for you;
  - [Galaxy Zoo](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge/data) if you want something "sciency".

  For this task, you can whip up anything from a fully connected network, through a relatively deep custom convolutional NN (using [`torch.nn.Conv2d`](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html) layers), to an off-the-shelf [ResNet](https://pytorch.org/vision/main/models/resnet.html) or a fancy [vision transformer](https://github.com/google-research/maxvit).
- regression:
  - Detect dark energy by ingesting [this state-of-the-art data release](https://github.com/PantheonPlusSH0ES/DataRelease/blob/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat) and regressing the `m_b_corr` column against `zCMB`
    - for added realism regress `mB` versus `zCMB` and as many of `x1`, `c`, `HOST_LOGMASS`, `HOST_ANGSEP`, `VPEC` as you can bear

  This is a small data set (by deep-learning standards), so use a correspondingly tiny network. Two layers, no more. Show me when it starts overfitting. Here you can make some nice prediction plots to show the network snap onto what we hope is the distance modulus relation.

  - Discover (Emulate) Newton's law from [NASA observations](https://ssd.jpl.nasa.gov/horizons/) with a graph neural network as in [this paper](https://arxiv.org/abs/2202.02306).

- bonus suggestion: train a network to detect the number and location of broccoli in a photo using [this groundbreaking data set](https://lcas.lincoln.ac.uk/nextcloud/shared/agritech-datasets/broccoli/broccoli_datasets.html).