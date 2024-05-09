# Scaling up
> or *Swimming with the Mermaids*


Here's what ChatGPT says was required to deliver the impressive AI results we take for granted today:

> - GPT-3 (Generative Pre-trained Transformer 3)
>   - GPUs: Thousands (exact number not publicly disclosed, estimated to be in the hundreds or thousands)
>   - Time: Several weeks to train initially, with ongoing fine-tuning and updates.
> - AlphaFold
>   - GPUs: Hundreds to thousands
>   - Time: Around a week for training, but the development process spanned several years.
> - DALL-E
>   - GPUs: Hundreds
>   - Time: Not publicly disclosed, but likely several weeks to train on a large dataset.

So maybe taking up 4 nodes x 2 GPUs for 12 hours (Ulysses's GPU resource limit) isn't so bad, if it will allow us to do cutting-edge science.[^spoiler]

[^spoiler]: Spoiler alert, it won't.

First steps first: make sure you're familiar at least with the [official Ulysses help page](https://www.itcs.sissa.it/services/computing/hpc). If you have also read through the unofficial [guide to surviving the mermaids](https://ulysses.readthedocs.io/), you can probably skip the first part

## Part -1: [Ulysses](https://en.wikipedia.org/wiki/Ulysses_(novel))

### Login

`frontend1.hpc.sissa.it`, `frontend2.hpc.sissa.it` with your SISSA credentials; 

> [!TIP]
> For convenience, you can [set up public key authentication](https://www.ssh.com/academy/ssh/public-key-authentication#setting-up-public-key-authentication-for-ssh) to skip the password.

> [!NOTE]
> From outside SISSA's network, you'll need the [SISSA VPN](https://www.itcs.sissa.it/services/computing/networkaccess#vpn).

> [!WARNING]
> Other clusters like Leonardo have [way more complicated](https://wiki.u-gov.it/confluence/display/SCAIUS/How+to+connect+via+2FA) login procedures.

### Available resources

:memo: Examine the available resources using [`sinfo`](https://slurm.schedmd.com/sinfo.html). A useful query may be
```shell
sinfo --Format="Partition:10,Memory:10,Sockets:8,CPUs:5,Threads:8,GRES:10,Features:20,Size:10,MaxCPUsPerNode,Time,NodeAIOT,NodeList"
```

### [Storage](https://www.itcs.sissa.it/services/computing/hpc#filesystem_usage_and_backup_policy)

You should understand the cluster's file storage options. Here are some terms:
- "Home" is a usually comparably small area that is accessible from login and compute nodes. It is usually backed up, so it is a good place to put your scripts, notebooks, results... It may be where you install your software environment since it's accessible from everywhere.
  - On Ulysses: `/home/$USER`, 200 GB, backed up daily.
  - :memo: Verify this using the Unix commands you've learned.
- "Scratch" is usually fast and large but temporary storage. Sometimes, it's only accessible from compute nodes and may be regularly deleted. Use this for storing data that is repeatedly accessed in your code, e.g. NN training data. In this scenario, your script will begin by downloading your data onto scratch from a more permanent storage. You can also write to scratch, but remember to transfer the results at the end of the script.[^danger]
- "Scratch" on Ulysses:
  - `/scratch/$USER`, 5 TB, no backup, no purges
  - ***The same as Home but bigger and no backup***. That is, it can be used for general storage (e.g. your environment), is accessible from everywhere and provides no speedup over Home.
- On other clusters, there can be storage partitions like "Work", "Project", etc. that provide various combinations of speed, size, and accessibility to collaborators.

[^danger]: Mermaid number 1: scratch is dangerous. What happens to your scratches if your script fails or is interrupted by the time limit?!

## Part 0: Environment

Using your favourite package / environment manager, set up a ML/DL stack on the cluster. I recommend Miniforge and wrote a whole lecture note about it. 

This should be done from a login node because

> [!IMPORTANT]
> The compute nodes have no access to the Internet...
> (for security reasons).

## Part 1: Jupyter on a cluster

Jupyter is a web application that runs a server on the machine you'd like to use for your computations. In the present case, that's a compute node on a cluster, so in order to use Jupyter, you need two things:
1. Running `jupyter` on a compute node. I recommend the following strategy:
   1. Log in to the login node.
   2. [`salloc`](https://slurm.schedmd.com/salloc.html) a node. Here, you should provide command-line options detailing the resources you wish to allocate: e.g. `-n NODES -c CPUS -G GPUs --mem MEMORY`, and the time limit `-t TIME`[^time]

      This find you the resources, reserve them for you, and return, printing the job id.
      - Now you can [view details about the allocation](https://slurm.schedmd.com/scontrol.html#OPT_show) using
        ```shell
        scontrol show job JOBID
        ```
        This way, you can verify you got what you wanted.
      - You can also `ssh`/[`slogin`](https://www.computerhope.com/unix/slogin.htm)[^slogin] into the compute node you got to verify with `nvidia-smi` what kind of GPU you got. Note that `slogout` (joking, it's `exit` or `logout`) of the compute node will *not* relinquish the job allocation, unlike interactive `srun`.
   3. Log out of the cluster. Your resources are still reserved for you.
   4. Run the following hacky command:[^hack]
      ```shell
      ssh USER@CLUSTER -L LOCAL:localhost:TUNNEL -t ssh NODE -L TUNNEL:localhost:REMOTE -t jupyter notebook --port=REMOTE
      ```
      - `NODE`: the address/name of the compute node. You can find that using `scontrol show job JOBID` or with [`squeue -u USER`](https://slurm.schedmd.com/squeue.html);
      - `REMOTE`: a port (by default `8888`) that the Jupyter server runs on;
      - `LOCAL`: the port on your local machine that you'll use to connect;
      - `TUNNEL`: any port that's not in use on the cluster login node: this will be used for *tunnelling* the connection.

      Then open a browser on `localhost:LOCAL` and enjoy Jupyter in its full glory.

> [!TIP]
> For `LOCAL`, you can choose `8888` again, but that may interfere with a local Jupyter. My suggestion is to pick different local ports for all the clusters you use: this way, you can bookmark them in your browser, save passwords, etc.

[^time]: I didn't tell you this, but just request the maximum time if you intend to be using Jupyter... Supposedly, the partition is not busy; otherwise, it's not too interactive, eh?

[^slogin]: No particular reason for using `slogin` over `ssh` except that it sounds like it's part of the slurm suite. It's not.

[^hack]: These are actually *three* commands:
    - `ssh USER@CLUSTER -L LOCAL:localhost:TUNNEL -t ...` connects to the login node and forwards your `LOCAL` port to its `TUNNEL` port. Then, it executes whatever follows the `-t` *on the login node*:
    - `ssh NODE -L TUNNEL:localhost:REMOTE -t ...` connects to the compute node from the login and forwards its `TUNNEL` port to the compute node's `REMOTE` port. Then, it executes whatever follows the `-t` *on the compute node*:
    - `jupyter notebook --port=REMOTE` starts Jupyter on the `REMOTE` port.

## Part 2: Distributed training with Pytorch Lightning

See the exercise in `0-exercises`.
