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

## 3. Fun with Slurm

Play around with Slurm and get comfortable with its different command.
In particular, practice:
- `squeue` and its various options to show just a specific queue/user
  - :memo: list pending jobs and the time they're expected to start
- `srun` / `salloc`+`slogin` for interactive work (see also [the Jupyter task](#4-jupyter-on-a-cluster))
- `scontrol`: verifying what resources were allocated to your (interactive) job.
- `sbatch`:
  - launch a multi-task job spread among many nodes (e.g. `--nodes 4 --ntasks-per-node 2`);
  - from each task print out all defined environment variables:
    - you can do that with `printenv` or from Python!
  - redirect the output from each task into a different file named according to the task rank:
    - see the docs on [IO Redirection](https://slurm.schedmd.com/srun.html).
  - Do you see the environment variable =[`SLURM_NTASKS_PER_NODE`](https://slurm.schedmd.com/srun.html#OPT_SLURM_NTASKS_PER_NODE)?!


## 4. Jupyter on a cluster

Connect to a Jupyter notebook running on a compute node with a GPU. This will also serve to verify you have installed your software properly.

1. To make it more concrete, make a [histogram](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html) of the [log-determinants](https://pytorch.org/docs/stable/generated/torch.logdet.html#torch-logdet) of 5000x5000 matrices, randomly sampled from an [LKJCholesky](https://pytorch.org/docs/stable/distributions.html#lkjcholesky) distribution. Use a GPU for the determinants.

2. Alternatively, run your training from [2.](#2-pytorch-lightning) but now on a cluster GPU.
   - I guess you all figured out already that you can run and view [Tensorboard from within a Jupyter notebook](https://www.tensorflow.org/tensorboard/tensorboard_in_notebooks)[^tbnb].
   - But can you set up Tensorboard and forward its ports, so that you can look at the training curves even if you're training from a script?

[^tbnb]: This demonstration/tutorial is ridiculously overcomplicated. You just need to `%load_ext tensorboard` and then `%tensorboard`.

> [!TIP]
> Maybe you can get away with running Tensorboard on the *login* node, so you only need one port forwarded. However, most clusters have stricter rules than Ulysses and will kill processes on the login nodes after e.g. 10 mins. Should be enought though.


## 5. Lightning on a cluster

Scale up your analysis from [2.](#2-pytorch-lightning) to multiple nodes/GPUs. To achieve this, first read through [this](https://lightning.ai/docs/pytorch/stable/accelerators/gpu_intermediate.html#distributed-data-parallel) and [more importanty this](https://lightning.ai/docs/pytorch/stable/clouds/cluster_advanced.html) section of the Lightning docs that I'll now proceed to summarise:
1. Transfer your code from a notebook into a `.py` script.
2. Write a batch script that details the resources to be allocated.
   - You need one task per GPU. It's advisable to take up all GPUs on a node to minimise network latency (especially on Ulysses...).
     - You can ask for [`--exclusive`](https://slurm.schedmd.com/srun.html#OPT_exclusive) access to the nodes.
   - Don't forget to ask for enough memory. If you're taking up whole nodes, you can ask for whole memories ([`--mem=0`](https://slurm.schedmd.com/srun.html#OPT_mem)).
   - Launch your `.py` script using `srun SCRIPT.py`.
     - Think about output redirection to different files (give the `--output` option to the *`srun`*).
3. In your [`Trainer`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer), ask for
   - `strategy='ddp', accelerator='gpu'` (the defaults),
   - ```python
     num_nodes = int(os.environ['SLURM_JOB_NUM_NODES']),
     devices = int(os.environ['SLURM_NTASKS_PER_NODE'])
     ```
     The reason I suggest this way is that Lightning will crash if the values you specify here do not match the environment variables.
4. Submit away and hope.
5. Finally, figure out a way to monitor progress:
   - Set up Tensorboard
   - or simply `tail -f` the output file(s)[^output].
   - Actually, have you thought about what happens with the things you [`LightningModule.log`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.log_dict.params.sync_dist) from each task?!

Deviate from this procedure at your own risk. 

[^output]: Printing out the progress bar happens only from the rank-0 process. 
