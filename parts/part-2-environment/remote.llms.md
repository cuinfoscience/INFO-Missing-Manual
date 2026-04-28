# 13  Remote Computing

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-terminal](#sec-terminal).
>
> **See also:** [sec-git-github](#sec-git-github), [sec-automation](#sec-automation), [sec-collaboration](#sec-collaboration).

## Purpose

![Permission denied (publickey). No further explanation. Somewhere on disk is a key you generated nine months ago and have already forgotten the passphrase to.](../../graphics/memes/remote.png)

Remote computing lets you use resources that are not physically on your laptop: university servers, high-performance clusters, lab machines, and cloud instances. This chapter teaches novices how to connect safely and reliably using [SSH](https://www.openssh.com/manual.html) and [VPNs](https://en.wikipedia.org/wiki/Virtual_private_network), move files, run remote jobs, and use tunneling to access remote services (including [Jupyter](https://jupyter.org/documentation)) as if they were local.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain client/server basics and what “remote computing” means.

2.  Use SSH to connect to a remote machine and run commands interactively.

3.  Use key-based authentication safely (generate keys, protect private keys, manage known hosts).

4.  Transfer files with `scp` or `sftp` (and understand when to use GUI tools).

5.  Use SSH tunneling (local, remote, and dynamic forwarding) for safe access to remote services.

6.  Understand what a VPN does, when it is required, and common pitfalls.

7.  Describe cloud computing at a practical level (instances, regions, networking rules, costs).

8.  Apply baseline security practices: least privilege, MFA, key hygiene, and avoiding data leaks.

## Running theme: remote access is powerful, so make it boring

The goal is not cleverness; it is predictable workflows that minimize risk.

## 13.1 A beginner mental model

The vocabulary here is simpler than it sounds. Your **local machine** is the laptop or desktop in front of you, the one whose keyboard you can touch. A **remote machine** is any other computer you reach over a network connection: a university server, a high-performance cluster login node, a cloud VM, a lab workstation. The **network** between them is whichever path actually connects them — your campus network, your home Wi-Fi, the public internet, or some combination.

Most remote tools use **client/server** language. The **client** is the program you run locally to initiate the connection (an SSH client, a VPN client, your web browser). The **server** is the remote program waiting to accept connections (an SSH server, a web server). The protocol — SSH, HTTPS, whatever — is the rule for how the two halves talk to each other. Once you have that picture in mind, every tool in this chapter is a variant of “run a client locally that talks to a server somewhere else.”

A few details about how connections behave matter in practice. An **SSH session** is a connection plus a shell — when you log out, the shell exits, and any program you started that depends on that shell may also stop. If you want a long-running job to survive your logout, you need a job-control tool like [`tmux`](https://github.com/tmux/tmux/wiki), [`screen`](https://www.gnu.org/software/screen/manual/screen.html), or [`nohup`](https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html). The remote computer also has its **own** filesystem, users, permissions, and installed software, which means a file on the remote machine is not the same as a file with the same path on your laptop, and “I have pandas installed” on your laptop tells you nothing about whether pandas is installed on the server.

Given all that overhead, why use remote computing at all? Four reasons. The first is **resources**: the server has more CPU, more RAM, more disk, or a GPU your laptop does not have. The second is **shared data and licensed software**: some datasets and tools live on a server because they are too large, too sensitive, or too expensive to copy. The third is **reliability**: a server runs continuously and gets backed up, while your laptop closes its lid and dies on Wi-Fi. The fourth is **collaboration**: when several people share a remote environment, everyone runs the same code against the same data with the same library versions, which eliminates an entire category of “works on my machine” bugs.

## 13.2 Prerequisites and safe defaults

Before the first SSH command, gather the information you need and decide on a few baseline habits. Remote computing is a discipline where small mistakes can leak credentials, expose data, or rack up real money on cloud bills, and the best time to develop careful habits is before you have any power to break anything.

### Accounts and credentials

To connect to any remote machine you need three facts: a **username** on that machine, the **host address** (a domain name like `server.cs.example.edu` or a bare IP address like `203.0.113.42`), and an **authentication method** the server will accept. The authentication method is usually either a password or an SSH key; some institutions also require multi-factor authentication on top of either one.

Whenever you have the choice, prefer your institutional identity with MFA plus **key-based SSH** over passwords alone. Institutional identity means the credentials are managed centrally — if your account is ever compromised, IT can revoke it in one place — and MFA means a leaked password alone is not enough to impersonate you. Key-based SSH, covered in detail a few sections below, is both more secure and less annoying day-to-day because you are not retyping a password every time you connect.

Write the three facts down the first time you learn them, somewhere you can find again:

``` text
# Remote: cs.example.edu research cluster
hostname:   server.cs.example.edu
port:       22 (default)
username:   agandler
auth:       SSH key (~/.ssh/id_ed25519) + Duo MFA
vpn:        required from off-campus (CiscoSecureClient → "cs.example.edu")
```

That is the minimum “how do I connect” note. Keep it somewhere accessible but not public; an `ssh_notes.md` inside your private notes repository is fine, a public GitHub gist is not.

### Install and locate your tools

Modern operating systems ship with SSH built in, but the shape of “how to find it” differs.

**macOS.** The built-in Terminal.app has `ssh`, `scp`, and `sftp` installed by default. You do not need to install anything. Open Terminal and type `which ssh`; it should print `/usr/bin/ssh`.

**Linux.** Same story — `ssh` and friends are installed by default on essentially every distribution. If your Linux machine is unusual and does not have them, `sudo apt install openssh-client` (Debian/Ubuntu) or the equivalent gets them.

**Windows.** Modern Windows 10 and 11 ship with an [OpenSSH](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_overview) client that you can use from [PowerShell](https://learn.microsoft.com/en-us/powershell/) or Command Prompt. Confirm it is installed with:

``` powershell
Get-Command ssh
# Should print a path like C:\Windows\System32\OpenSSH\ssh.exe
```

If the command is not found, open Settings → Apps → Optional features, click “Add an optional feature,” search for “OpenSSH Client,” and install it. For more terminal-friendly experience, consider running your remote work from **Windows Terminal** (a tabbed terminal application, free in the Microsoft Store) or from **Windows Subsystem for Linux (WSL)**, which gives you a proper Linux environment on the same machine.

Optionally, install a code editor with remote-development support. [VS Code](https://code.visualstudio.com/docs)’s [**Remote - SSH**](https://code.visualstudio.com/docs/remote/ssh) extension is the most popular — it lets you open a folder on a remote server and edit it as if it were local, with full syntax highlighting, terminal, and debugger running over the SSH connection.

### Golden safety rules

A few non-negotiable habits that should feel automatic before you do anything else in this chapter:

- **Never share passwords or private keys with anyone.** Not your project partner, not your TA, not tech support — nobody legitimate will ever ask for them. A private SSH key is like your house key; sharing it means the other person can be *you* to any server that trusts the key.
- **Never paste secrets into commands, notebooks, or chat messages.** Command history files (`~/.bash_history`, `~/.zsh_history`) record every command you type, and anything that passes through a chat is stored on someone else’s server. If you need to provide a password to a program, use an interactive prompt (`read -s PASSWORD`) or an environment variable loaded from a `.env` file (see [sec-secrets](#sec-secrets)), not a command-line argument.
- **Assume your command history is readable.** Your future self will read it, and on shared servers the administrators technically can too. Anything sensitive — API tokens, personal data, “try this hack” one-liners — should either not be typed at all or should be wrapped in a scripted workflow where the secret comes from an environment variable.
- **Use the minimum access needed, and log out when done.** If a server has `sudo` available, do not live as root; do your normal work as your user account and elevate only for the few commands that actually need it. When your session is over, type `exit` (or `Ctrl+D`) to cleanly terminate it. Idle SSH sessions are both a resource cost and a small security risk.

## 13.3 SSH fundamentals

### What SSH provides

SSH (Secure Shell) is the workhorse protocol for remote computing on Unix-like systems. It does three things, all of them encrypted: it gives you a secure remote login (a shell on a server somewhere), it lets you securely transfer files in and out of that server, and it lets you tunnel other kinds of network traffic through the same connection. The three uses are the same protocol with different command-line shapes, which is why “learn SSH” turns out to be one of the highest-leverage skills in remote work.

### The simplest connection

The most common SSH command is:

``` bash
ssh username@hostname
```

For example, `ssh agandler@server.cs.example.edu`.

![](graphics/PLACEHOLDER-ssh-connected.png)

Figure 13.1: ALT: Terminal showing a successful SSH connection. The prompt has changed from the local hostname to the remote hostname (for example, from `you@laptop` to `agandler@server.cs.example.edu`), signalling that commands now run on the remote machine.

> **WARNING:**
>
> The three common failures each point at a different layer. **“Operation timed out” or “Connection refused”** usually means the network can’t reach the server — are you on the right VPN? On campus Wi-Fi? Try `ping hostname` to confirm you can route to the host at all. **“Permission denied (publickey)”** means the server accepted your connection but rejected your credentials; confirm your key is loaded with `ssh-add -l` and that the public key is installed in the server’s `~/.ssh/authorized_keys`. **“Host key verification failed”** means the server’s identity changed — usually after a server reinstall, occasionally because of a man-in-the-middle attack; if you trust the change, edit `~/.ssh/known_hosts` and remove the stale entry for that hostname.
>
> For any of these, `ssh -v username@hostname` turns on verbose output so you can see which stage is failing. See [sec-asking-questions](#sec-asking-questions) if you need to escalate to your IT department.

If the server is running SSH on a non-standard port (some institutions do this), you add `-p`:

``` bash
ssh -p 2222 username@hostname
```

The first time you connect to a new server, SSH will ask whether you trust the **host fingerprint** — a long string of characters that uniquely identifies the server’s identity. Type `yes` to accept it (this is the moment when you should verify the fingerprint with your instructor or sysadmin if you have any doubt), and SSH will record it in a file called `~/.ssh/known_hosts`. After that, every future connection silently checks that the server still presents the same fingerprint.

### Host identity and `known_hosts`

The reason SSH bothers with fingerprints is to defend against a class of attack called “man-in-the-middle,” where someone impersonates the server you intended to reach and tricks you into typing your password into theirs. Once you have accepted a server’s fingerprint, SSH will refuse to connect if it ever changes — which is what you want. The catch is that fingerprints can also change for benign reasons: the server was rebuilt, the SSH daemon was reinstalled, the keys were rotated. When you see a fingerprint warning, do *not* just accept it because you are in a hurry. Verify the change through a trusted channel (an email from sysadmin, an announcement from your instructor) before you remove the old fingerprint and accept the new one.

### Authentication: passwords vs keys

You can authenticate to an SSH server with a **password** or with a **key**. Passwords are easier to start with and are how most people first encounter SSH, but they are less secure (passwords can be guessed and reused) and many managed servers disable them entirely. **Keys** are the recommended approach. A key pair is two files: a **private key** that stays on your device (and that you should never share with anyone) and a **public key** that is safe to copy onto the servers you want to log into. The server uses the public key to verify, mathematically, that you possess the corresponding private key — which you prove without ever sending the private key over the network. The whole point is that even if someone intercepts your traffic, they cannot impersonate you, because they do not have the private key.

You generate a key pair with `ssh-keygen` and protect the private key with a passphrase, which means that even someone who steals the private key file cannot use it without also knowing your passphrase:

``` bash
ssh-keygen -t ed25519 -C "your.email@example.com"
# When asked for a file path: accept the default (~/.ssh/id_ed25519)
# When asked for a passphrase: pick a strong one
```

After generating, copy the public key (the file ending in `.pub`, never the one without an extension) onto the server’s authorized keys list. On many systems the easy way to do this is `ssh-copy-id username@hostname`, which appends your `id_ed25519.pub` to the right file in one command.

### Generating a key pair (conceptual)

    ssh-keygen

- Choose a strong passphrase.

- Store keys in the default ` /.ssh/` location.

- Keep your private key file permissions restrictive.

### SSH agent (optional but useful)

- An agent holds decrypted keys in memory so you do not type your passphrase repeatedly.

- Treat agent forwarding as advanced; do not enable it by default.

### Quality-of-life: ` /.ssh/config`

- Create short nicknames for hosts.

- Store per-host usernames, ports, and identity files.

- Keep configuration readable; document nonstandard choices.

## 13.4 File transfer: getting data in and out

Moving files between your laptop and a remote server is the second-most-common thing you will do after logging in. SSH provides three complementary tools for this (`scp`, `sftp`, `rsync`), and each has a situation where it is the right choice.

### The basic question: where is the file?

Every file-transfer command involves two paths, and the most common way to get tangled up is to confuse which path is local and which is remote. **Local paths** refer to files on the machine where you are typing the command. **Remote paths** are written with a `username@hostname:` prefix — the `:` is the part that says “this is on the other side.” Everything after the colon is a path *on the remote machine*, not your laptop.

``` text
data/raw/sales.csv                                       ← local path
/home/agandler/projects/sales/data/raw/sales.csv        ← also local unless prefixed
agandler@server.cs.example.edu:~/projects/sales/data/  ← remote path (note the `:`)
```

When in doubt, use **absolute paths** on both sides. Relative paths on the remote side are resolved against the remote home directory — which is convenient but also a frequent source of “where did my file actually land?” confusion. Starting with absolute paths until you are fluent saves a surprising amount of time.

### Secure copy with `scp`

`scp` is the simplest option and has the same mental model as `cp`: source first, destination second. Either side can be local or remote.

``` bash
# Upload a file to the server
scp report.pdf agandler@server.cs.example.edu:~/deliverables/

# Download a file from the server
scp agandler@server.cs.example.edu:~/results/summary.csv ./

# Upload a whole directory tree (note the -r flag)
scp -r data/raw/ agandler@server.cs.example.edu:~/projects/sales/data/

# If you use a non-default port:
scp -P 2222 file.txt user@host:~/
# (note the capital -P for scp, unlike lowercase -p for ssh)
```

Two small footguns to know about. First, `scp` is recursive only with `-r` — without it, trying to copy a directory fails with “not a regular file.” Second, paths with spaces need to be quoted *and* escaped on the remote side, because the remote shell will re-parse them:

``` bash
scp "report draft.pdf" user@host:'~/Dropped\ Reports/'
```

`scp` is perfect for one-shot transfers and for scripting. For anything interactive or any transfer you want to resume after an interruption, reach for `sftp` or `rsync` instead.

### Interactive transfer with `sftp`

`sftp` opens an interactive “FTP-like” session over SSH. Once you are inside, you can navigate the remote filesystem with `cd` and `ls`, navigate the local filesystem with `lcd` and `lls`, and transfer files with `put` (upload) and `get` (download):

``` bash
$ sftp agandler@server.cs.example.edu
Connected to server.cs.example.edu.
sftp> cd projects/sales
sftp> ls
data/  notebooks/  src/  README.md
sftp> lcd ~/Downloads
sftp> put new_data.csv data/raw/
Uploading new_data.csv to /home/agandler/projects/sales/data/raw/new_data.csv
sftp> get notebooks/results.ipynb
Fetching /home/agandler/projects/sales/notebooks/results.ipynb to results.ipynb
sftp> bye
```

`sftp` is most useful when you need to poke around a remote directory, decide what to transfer, and move a few files. It is also the protocol that most GUI file-transfer tools (Cyberduck, FileZilla, Transmit, WinSCP) speak under the hood — if typing interactive commands is not your thing, any of those tools gives you a graphical two-pane view of local and remote files with drag-and-drop, and under the covers they are just driving SFTP.

### `rsync` for large or repeated transfers

For anything bigger than a few files, or anything you will sync repeatedly, `rsync` is the right tool. It is smarter than `scp` in three ways that matter: it can **resume** an interrupted transfer where it left off, it **skips files that are already up to date** on the destination, and it can show an accurate progress indicator.

``` bash
# Upload a project directory, skip files already up to date, show progress
rsync -avz --progress data/raw/ agandler@server.cs.example.edu:~/projects/sales/data/raw/

# -a : archive mode (preserves permissions, timestamps, and recurses)
# -v : verbose
# -z : compress during transfer
```

The trailing slash on the source path matters: `data/raw/` (with slash) copies the *contents* of `data/raw` into the destination, while `data/raw` (without slash) copies the directory itself. Get this wrong once and you will end up with `~/projects/sales/data/raw/raw/` on the destination.

### What not to do

A short list of file-transfer habits that will hurt you:

- **Do not email datasets.** Email attachments are not designed for data movement, and most institutional email servers strip or block large files. Worse, email is often the wrong place for sensitive data — you are handing a copy to every mail server along the route.
- **Do not copy data into unapproved cloud storage.** If your research data has any access rules at all — student records, clinical data, anything covered by an IRB or a data use agreement — uploading it to your personal Google Drive or Dropbox is almost certainly a violation. When in doubt, ask your instructor or data steward before the upload, not after.
- **Do not move large files through an interactive `sftp` session if `rsync` is available.** Interactive sessions cannot resume if the connection drops, so a 90% complete transfer that fails means starting over. `rsync` exists specifically to avoid that.
- **Do not leave datasets in your home directory on shared servers without talking to the admin.** Shared filesystems have quotas, and a surprise 40 GB in your home directory is the kind of thing that earns you an angry email.

## 13.5 Tunneling and port forwarding (making remote services usable)

### Why tunneling exists

- Many services (Jupyter, databases, dashboards) bind to `localhost` on the server for safety.

- A tunnel lets your local machine reach that service through an encrypted channel.

### Local forwarding (most common)

The form you will use ninety percent of the time is **local forwarding**, where you tell SSH “make port X on my laptop behave as if I were connected to port Y on the remote server.” The most common case is starting Jupyter on a server and viewing it in your local browser:

``` bash
ssh -L 8888:localhost:8888 username@hostname
```

Read the `-L` argument as “Local 8888 → remote `localhost:8888`.” After running this, you can open `http://localhost:8888` in your *local* browser and it will be talking to the Jupyter server running on the remote machine, through the encrypted SSH tunnel. If port 8888 is already in use on your laptop (maybe because you have a local Jupyter running too), pick a different local port: `ssh -L 8899:localhost:8888 username@hostname` and then visit `http://localhost:8899`.

### Remote forwarding (advanced)

The mirror image of local forwarding is **remote forwarding** with `-R`, where you tell SSH “make port X on the remote server behave as if I were connecting to port Y on my laptop.” This is much less common and changes the exposure model — you are exposing something on your laptop to the remote machine — so use it cautiously and only when you have a specific reason.

### Dynamic forwarding (SOCKS proxy)

A third variant is **dynamic forwarding** with `-D`, which sets up a SOCKS proxy on a local port that routes arbitrary traffic through the remote machine’s network. This is useful for “browse the web as if I were on the campus network” scenarios, but it interacts with institutional policies in ways you should understand before relying on it. Treat it as advanced territory.

### Tunnel hygiene

A few small habits keep tunnels safe and easy to manage. When you only need a tunnel and not an interactive shell, add `-N` (`ssh -N -L 8888:localhost:8888 username@hostname`) so SSH does not open a shell you do not need. Always bind the local side to `localhost` (the default) rather than `0.0.0.0`, so other users on your network cannot piggyback on your tunnel. And close tunnels when you are done with them — leaving them open consumes resources and leaves an open authenticated path you do not need.

## 13.6 VPN fundamentals

### What a VPN does

A **Virtual Private Network** creates an encrypted tunnel between your device and a gateway somewhere else, and while that tunnel is active, your traffic looks to the rest of the world as if it is originating from the gateway rather than from your laptop. In a university context, that gateway lives on the institutional network, so once you connect the VPN your off-campus laptop behaves *as if* it were plugged into an ethernet jack in the library — with access to the same internal servers, file shares, and licensed resources you could reach from inside the building.

Conceptually, the VPN creates a “virtual” network interface on your machine. Your operating system treats it like any other network connection, and a separate “routing table” decides which traffic goes through the VPN and which does not. This is why VPN clients can sometimes interact oddly with your existing network setup — they are not just wrapping traffic, they are rewiring which network your packets flow through.

### When you need a VPN

Most students encounter VPNs for one of four reasons:

1.  **Off-campus access to university resources.** Your library’s subscription journals, your institution’s software licenses, and protected databases often check where you are connecting from and deny anyone who is not on the campus network. The VPN is how you “get on campus” from your kitchen table.
2.  **SSH to internal-only hosts.** Many research servers and compute clusters are intentionally not reachable from the public internet — you can only `ssh` to them from within the institution’s network. The VPN is the only way to reach them from outside.
3.  **File shares and network printers.** Shared drives (`//fileserver/research/`) and networked printers typically only respond to machines on the campus network.
4.  **Compliance and data access agreements.** Some research data must only be accessed from “managed” connections for privacy or contractual reasons, and the VPN is what counts as a managed connection.

``` bash
# Typical workflow for a VPN-gated server:
# 1. Connect the VPN client (GUI app, look for your institution's name)
# 2. Verify the VPN is up (most clients show a green icon)
# 3. THEN try ssh
ssh agandler@cluster.internal.example.edu
```

Your university’s IT page will have the specific VPN client and credentials to use — most commonly Cisco AnyConnect / Secure Client, GlobalProtect, or OpenVPN. Install the one your institution recommends; do not just grab a generic “free VPN” from the app store, because commercial VPNs connect you to *their* network, not your university’s.

### Common VPN pitfalls

Three gotchas hit students often enough to be worth naming:

**VPN drops kill SSH connections.** If the VPN reconnects or briefly loses its tunnel — say your Wi-Fi hiccups — every SSH session running through it is dropped along with the tunnel. Any long-running job you started in that session stops along with the shell. The fix is to run long jobs inside a detached session manager like `tmux` or `screen`, or to submit them as batch jobs if the system supports that, so that the job survives even if your connection does not.

``` bash
# Start a tmux session; your work survives disconnection
ssh agandler@server.cs.example.edu
tmux new -s work
# ...run long job...
# Detach with Ctrl+b d; connection can now safely drop
# Later, reconnect and run: tmux attach -t work
```

**Split-tunneling vs full-tunneling.** A **full-tunnel** VPN sends every packet through the institution’s network — including your Netflix and your Zoom call — which can be slow and which sometimes triggers usage policies. A **split-tunnel** VPN only routes traffic destined for institutional addresses through the VPN, leaving everything else on your normal internet connection. Most universities use split-tunneling by default because it is faster and more polite, but the behavior varies; if things feel strangely slow or certain websites stop working while the VPN is on, check your client’s settings for the tunneling mode.

**VPNs sometimes break local networking.** A full-tunnel VPN can make local devices — a printer in your apartment, a Raspberry Pi on your home network, a Docker container on your laptop — unreachable because your packets to the local address are being routed through the VPN gateway and back. If a printer or a local development server stops working the moment you connect your VPN, that is almost always the reason. Disconnect the VPN, confirm the local thing works, and look for a split-tunnel option in the client.

### Practical advice

Three habits make VPN workflows smooth:

- **Connect the VPN first, then everything else.** SSH, file transfers, and remote-development editors should be started *after* the VPN is up, not before. Starting them before the VPN is up usually produces a confusing hostname-resolution error that feels unrelated to the VPN.
- **Assume remote processes do not survive a disconnect.** When the VPN drops, treat any running SSH session as dead — even if your terminal window is still open, the connection is gone. Reconnect the VPN, then reopen SSH, and use `tmux attach` to get back to the session you left running.
- **Know where your VPN client shows status and logs.** Every VPN client has a status indicator (green/yellow/red dot) and a log window. Find both the first time you set the client up. The next time something does not work, the log is the first place to look — “Authentication failed,” “Certificate expired,” and “Server unreachable” each point at different problems.

## 13.7 Remote work patterns: from simple to professional

Once you can connect and move files, the question becomes: how do you *work* on a remote machine day-to-day? There is no single right answer — different problems reach for different patterns. The three below cover most of what students encounter.

### Pattern 1: login node plus compute nodes (HPC model)

High-performance computing (HPC) clusters — the kind you find at most research universities — are built around a strict separation between the **login node** and the **compute nodes**. When you SSH in, you land on a login node: a small server whose only job is to let you edit files, submit jobs, and check status. The actual work runs on the compute nodes, which are much bigger machines allocated to you by a **scheduler** (Slurm is by far the most common; you may also encounter PBS, LSF, or SGE).

The single most important rule on these systems is: **do not run heavy work on the login node.** Login nodes are shared by every user logged in at the same time, and a single person running a big pandas job on the login node can slow everyone else to a crawl. The scheduler exists specifically so that heavy work happens on the compute nodes where it cannot hurt anyone else.

A typical Slurm workflow looks like this:

``` bash
# SSH into the login node
ssh agandler@cluster.cs.example.edu

# Write a small submission script
cat > run_analysis.sbatch <<'EOF'
#!/bin/bash
#SBATCH --job-name=sales-analysis
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=logs/%x-%j.out

module load python/3.11
source ~/projects/sales/.venv/bin/activate
cd ~/projects/sales
python scripts/analyze.py
EOF

# Submit the job
sbatch run_analysis.sbatch
# → Submitted batch job 12345

# Check on it later
squeue -u agandler
```

The `#SBATCH` lines tell Slurm what resources you want; the rest of the script is a regular shell script that will run on whichever compute node the scheduler allocates. Your job will start some time later (seconds to hours, depending on queue load), and its output will land in the log file named by the `--output` line. If you are new to a cluster, your institution’s HPC documentation will show the local variations — custom partitions, accounting flags, available software modules — and you should read it before your first submission.

### Pattern 2: remote development with your editor

If you are doing exploratory work rather than batch jobs, the remote-development pattern is usually more pleasant. The idea is to keep your editor on your laptop (where it is fast and familiar) but have it open and run code on the server (where the data and compute live). VS Code’s **Remote - SSH** extension is the canonical implementation: install the extension, press `F1`, run “Remote-SSH: Connect to Host…”, pick your SSH host, and VS Code opens a new window where the file tree, integrated terminal, and Python interpreter are all on the remote machine.

``` text
Local: VS Code window, editor UI
   │
   │  (SSH connection; VS Code ships a small helper process
   │   to the remote server that handles filesystem and terminal)
   │
Remote: file tree, terminal, Python runtime, data files
```

The other common approach is the older “edit locally, sync, run remotely” loop: you edit your project on your laptop, push changes to a Git remote ([sec-git-github](#sec-git-github)), pull them on the server, and run them there. This works and is fully reproducible, but it has a minor latency penalty per edit-run cycle compared to the remote-editor pattern.

The one habit that matters regardless of which pattern you use: **never manage your files by manually copying them back and forth.** Code lives in version control; data lives in a documented location on the server; outputs get regenerated by running code. If you find yourself dragging files to and from the remote server by hand, the project is about to develop a “which copy is the real one?” problem, and the correct fix is to move the project into Git (for the code) and document how to reproduce the data pipeline (for the data).

### Pattern 3: remote Jupyter notebooks

The Jupyter-on-a-server pattern is worth its own section because it is so common and because the naive version is dangerously insecure. The right way to do it has three parts: start Jupyter on the server bound to `localhost`, set up an SSH tunnel from your laptop to the server, and connect your browser through the tunnel.

``` bash
# Terminal 1 — on the server, inside tmux so it survives disconnect
ssh agandler@server.cs.example.edu
tmux new -s jupyter
cd projects/sales
source .venv/bin/activate
jupyter lab --no-browser --ip=127.0.0.1 --port=8888
# Jupyter prints a URL with a token — copy it

# Terminal 2 — on your laptop, tunnel the port
ssh -N -L 8888:localhost:8888 agandler@server.cs.example.edu

# Browser — on your laptop
# Open http://localhost:8888/lab?token=<the token from Jupyter>
```

Three details matter here. First, `--ip=127.0.0.1` (equivalently, `localhost`) tells Jupyter to listen only on the server’s loopback interface, which means no one on the network can reach it directly — only something that is already on the server can. This is the single most important security setting, because Jupyter has full access to your account, and a Jupyter server exposed on `0.0.0.0` is effectively a shell open to the world. Second, the tunnel gives *your* laptop a way to reach the loopback-only Jupyter through the encrypted SSH channel. Third, the `token` in the URL is what authenticates you to Jupyter — do not share URLs that include the token, and treat a leaked token the same as a leaked password.

If the server already has a Jupyter service set up by admins (JupyterHub or similar), use that instead — it handles all of the above for you and is the safer default.

## 13.8 Cloud computing basics (what novices must know)

### What “the cloud” actually is

“The cloud” is a shorthand for renting computing resources from a provider (Amazon Web Services, Google Cloud Platform, Microsoft Azure, DigitalOcean, Linode, and dozens of smaller players) instead of buying and running your own hardware. The resources you rent include **virtual machines** that you SSH into and use like any server, **object storage** for large files, **managed services** (databases, container orchestration, serverless functions) that abstract away the server entirely, and increasingly **GPU instances** for machine-learning work.

The thing that distinguishes the cloud from other forms of remote computing — like a university cluster — is how much control and how much responsibility you have. On a university cluster, the admins pre-install software, enforce policy, and mostly stop you from shooting yourself in the foot. On a cloud account you own, there is no one between you and the controls. You can create resources, modify firewalls, delete data, and — importantly — **spend money**, all with a few clicks. Used well, this is enormously powerful; used carelessly, it is a great way to wake up to a surprise bill.

### Core vocabulary

A few terms come up everywhere and are worth learning once:

- **Instance (or VM, or virtual machine).** A rented computer: you pick its size (CPU, RAM, disk, GPU), an OS image, and a region, and the provider starts it up in a few seconds. You pay for the time it is running, plus usually a smaller amount for the attached disk even when it is stopped.
- **Region and zone.** Cloud providers have datacenters scattered across the world. A **region** is a geographic area (e.g., `us-east-1`, `europe-west2`), and a **zone** is a specific datacenter within that region. You pick a region close to your users and your data, and you stick to one region for a given project to avoid cross-region data-transfer fees.
- **Object storage (buckets).** A place to park files by key: not a filesystem exactly, but a URL-addressable store for large blobs. AWS calls it S3, GCP calls it Cloud Storage, Azure calls it Blob Storage. The access model is “upload a file, get a URL, download it somewhere else.” Very cheap to store, charged by how much you store and how much you download.
- **Attached disks.** A “block device” that mounts inside an instance and behaves like a normal filesystem. You pay for the provisioned size regardless of whether you are using it.
- **Security groups / firewall rules.** The rules that decide which network traffic can reach your instance. By default, most providers lock things down: you explicitly open port 22 for SSH, port 443 for HTTPS, and so on, and you should open them to the smallest source range you can (your laptop’s current IP, not the whole internet).
- **IAM (identity and access management).** The permission system that controls which people and services can do what. This becomes critical as soon as you start using managed services; for a first VM, the defaults are usually fine.

### A safe “first cloud VM” workflow

The walkthrough is almost identical across AWS, GCP, Azure, and DigitalOcean. The specifics of button names change; the shape is always the same.

1.  **Create the instance in a region close to you.** Pick the smallest size that meets your needs — `t3.small` or `e2-micro` is fine for experimentation. An Ubuntu LTS image is the safest default OS choice for data-science work. Note the approximate hourly cost before confirming.
2.  **Attach an SSH key pair, providing your public key.** Paste your `~/.ssh/id_ed25519.pub` (the file ending in `.pub`, *never* the one without the extension) into the instance creation form. The provider will install it on the new machine as an authorized key. If the console offers to generate a new key pair for you, it is usually fine to accept — just download the private key immediately and never lose it.
3.  **Configure inbound access narrowly.** In the firewall / security group settings, allow SSH (port 22) only from your *current* IP address, not from `0.0.0.0/0`. Most cloud consoles show you a “My IP” button that autofills this. Every other port should stay closed unless you have an explicit reason. This one decision is the difference between “safe experimentation” and “compromised server running a cryptominer within the hour.”
4.  **Connect via SSH** using the instance’s public IP. Confirm you can log in, update packages (`sudo apt update && sudo apt upgrade`), and install what you need.
5.  **Stop or terminate the instance when you are done.** “Stop” suspends the VM so you stop paying for compute but keep paying (a smaller amount) for disk; “Terminate” destroys it entirely and stops all charges. For a throwaway experiment, terminate. For a machine you plan to return to tomorrow, stop.

``` bash
# Once the VM is running, connect
ssh -i ~/.ssh/id_ed25519 ubuntu@203.0.113.42

# Inside: update and install your tools
sudo apt update && sudo apt upgrade -y
sudo apt install python3-venv git tmux
```

### Cost and risk: the two surprises to avoid

The first surprise is that cloud resources cost money **while running and sometimes while merely stored**. A stopped VM still bills you for its disk. An unused public IP may cost a small amount per hour. An orphaned storage bucket from a semester-old experiment can quietly accumulate charges for a year before anyone notices. The defense is a habit: **set up billing alerts** the first day you create the account. Every provider lets you set a monthly budget and email you when you cross 50%, 80%, and 100% of it. If your expected monthly spend is five dollars, set the alerts at two, four, and five — you will get a loud signal long before anything becomes expensive.

``` text
# In the cloud console billing settings:
Budget:         $10/month
Alerts:         50% → email
                80% → email
                100% → email + SMS
```

The second surprise is security. A cloud VM with SSH open to the entire internet, running an unpatched OS, will start receiving automated login attempts within minutes and can be compromised within hours. The defenses are boring but they work: use key-based authentication instead of passwords, keep inbound SSH restricted to your current IP, install updates (`sudo apt upgrade`) regularly, do not expose services (databases, Jupyter, web apps) directly to the public internet without thinking hard about it, and do not store credentials or secrets on instances that could be seized by anyone who gets shell access. When in doubt, assume any service exposed to the internet is one misconfiguration away from being the bad day of your academic career.

## 13.9 Security best practices for remote computing

The rules in this section are deliberately boring. That is the point — security practices that feel dramatic and clever are usually the ones that backfire, and the ones that work tend to be tiny habits you do the same way every day.

### Key hygiene

Your SSH private key is the single most sensitive file on your laptop in the context of remote computing. Treat it accordingly.

Always protect it with a **passphrase**, set at the time you generate the key with `ssh-keygen`. A passphrase means that even an attacker who copies the private-key file off your laptop cannot use it without also knowing the passphrase. The SSH agent (which your OS usually runs automatically) decrypts the key once per session, so you type the passphrase at most once a day rather than every time you connect.

Never store private keys in places that are synced or shared: not in a Dropbox folder, not in a GitHub repository (even a private one), not in a `~/Desktop/backup/keys/` directory that you zip up and email to yourself. The correct location is `~/.ssh/` with file permissions set to `600` (read/write for you, no access for anyone else):

``` bash
# Confirm your key permissions are restrictive
ls -l ~/.ssh/id_ed25519
# -rw------- ... id_ed25519   ← this is correct (600)

# If it is wrong, fix it:
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

Avoid “key sprawl.” It is tempting to generate a new key for every laptop, every project, and every cloud account and then forget which goes where. A simpler rule: use one personal key for all your personal work; generate a separate dedicated key only when there is a real reason (a specific service demands it, or you are handed a managed keypair by an employer). When a machine you used is retired, remove the public key from any `authorized_keys` files it was installed on.

If you ever think a private key might have been compromised — you lost the laptop, you accidentally committed the file to a repository, someone else had physical access to your machine — **rotate it immediately**. Rotation means: generate a new key pair, push the new public key to every server and service that trusted the old one, remove the old public key from those servers, and then delete the old private key from your laptop.

### Least privilege and account separation

Most remote machines have some notion of “admin” access (`root` on Linux, `sudo` for users who are allowed to become root temporarily). The rule is: **do your normal work as an ordinary user, and only elevate to root for the specific commands that require it.** This is not paranoia — it is the same logic as not doing daily browsing as a Windows Administrator account. Ordinary users cannot accidentally `rm -rf /`, cannot install system-wide software, and cannot edit files they do not own. Most of the time, that is exactly the protection you want.

``` bash
# Normal work: run as yourself
python analyze.py
pip install --user some-package

# Elevate only for specific commands that need it
sudo apt install postgresql

# NOT this:
sudo -i        # spawning a root shell and living there
```

On the data side, the corresponding principle is “access the data you need and nothing more.” If a project only needs a subset of a database, request read access to just that subset instead of full admin. If a dataset is sensitive, do not copy it to places where the access controls are weaker than the original. See [sec-secrets](#sec-secrets) for how to handle credentials that authorize this kind of access.

### Safe networking defaults

On any server you control — a cloud VM, a lab workstation, a personal server — the default should be “almost nothing is reachable from the network” and you open specific ports only as needed. SSH (port 22) is usually the only port that needs to be reachable from outside; everything else (database, Jupyter, web app) should be either bound to `localhost` on the server and accessed via SSH tunnel, or protected behind a firewall rule that restricts the allowed source IPs.

``` text
Good:  SSH open to "my office IP only"
       Jupyter bound to 127.0.0.1, reached via SSH tunnel
       Database listening on 127.0.0.1 only

Bad:   SSH open to 0.0.0.0/0 (the whole internet)
       Jupyter bound to 0.0.0.0 with no password
       Database with default admin password exposed publicly
```

Keep the software on remote machines patched. On Ubuntu:

``` bash
sudo apt update && sudo apt upgrade -y
```

This should be a monthly habit on any machine you own, more often if the machine is exposed to the internet or handles sensitive data. A forgotten VM running two-year-old packages is a much bigger risk than a forgotten VM running current ones.

### Logging and traceability

For student-level remote work, you do not need a fancy logging infrastructure. You do benefit from a tiny “session log” — a plain text file you keep per server or per project where you jot down what host you are on, what you did, and what changed. The log takes about a minute per session and is invaluable the next time something is broken and you want to reconstruct “what did I do last Tuesday?”

``` markdown
# ~/notes/server-log.md

## 2026-04-08 — cluster.cs.example.edu
- Logged in to check on sales-analysis job
- Job 12345 finished successfully; moved outputs to reports/2026-04-08/
- Noticed free space on /scratch is at 92%; cleaned up old checkpoints

## 2026-04-10 — cluster.cs.example.edu
- Submitted new batch job with updated parameters
- Updated run_analysis.sbatch (committed to git)
```

The bigger point: use **version control for code changes** ([sec-git-github](#sec-git-github)). Every time you edit a script on the server, commit the change. Every time a piece of code produces a result you plan to keep, commit the code that produced it. “What version of the code made this output?” is a question you should always be able to answer, and Git is the only practical way to answer it retroactively.

## 13.10 Troubleshooting and diagnostics

Remote connections fail in a predictable set of ways. The diagnosis almost always comes from running a few small commands — not from staring at an error message hoping it will become more informative.

### Connection failures: work up the stack

When `ssh` fails, work from the bottom of the network stack upward. Check each layer, then move to the next.

**Is your basic internet working?** Open a website, or `ping` something you know responds. If the internet itself is broken, no remote command will work.

``` bash
ping -c 3 google.com
# If this fails, fix your local network first.
```

**Is the VPN up, if you need one?** If the server is behind a VPN, confirm the VPN client shows “connected” and try `ping`ing something on the institutional network. A dropped VPN is the single most common cause of “SSH suddenly stopped working.”

**Does the hostname resolve?** If SSH says “Could not resolve hostname,” DNS itself is broken (or you typed the name wrong):

``` bash
ssh -v agandler@server.cs.example.edu
# The -v flag shows verbose connection steps.
# Look for "Connecting to server.cs.example.edu port 22" — if it never
# reaches that line, hostname resolution is the problem.
```

**Is the server reachable on the expected port?** Even if DNS works, a firewall may be blocking you:

``` bash
# Try the port directly
nc -vz server.cs.example.edu 22
# "succeeded!" → port reachable
# "Connection refused" → server present but not listening on that port
# "Connection timed out" → firewall or network is dropping the packet
```

**Are you using the right username and the right key?** Double-check the username (it is usually not your laptop username), and if you have multiple keys, make sure SSH is offering the right one. You can force a specific key with `-i`:

``` bash
ssh -i ~/.ssh/id_ed25519 -v agandler@server.cs.example.edu
```

The `-v` verbose output shows every key SSH tries, which is the fastest way to diagnose “SSH is authenticating with the wrong key.”

### Host key warnings: never ignore, always verify

A host key warning looks like this and is designed to stop you:

``` text
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
```

The warning means: the server presented a different identity than the one SSH recorded the first time you connected, and SSH refuses to continue. The two possibilities are mutually exclusive: either something legitimate changed on the server (it was rebuilt, the SSH daemon was reinstalled, keys were rotated), or something malicious is happening. Do not just accept the new key because it is in the way of what you wanted to do.

The right response is to **verify through a trusted channel** — an email from sysadmin, a post on an internal wiki, an announcement from your instructor — that the key change is expected. Once you have confirmation, remove the old entry and reconnect:

``` bash
# Remove the old host key entry for that host
ssh-keygen -R server.cs.example.edu
# Then reconnect; SSH will prompt you to accept the new key
ssh agandler@server.cs.example.edu
```

If you cannot verify the change, do not connect. It is much better to miss a connection than to type your password into an attacker’s server.

### Timeouts and unstable connections

If SSH connections drop after a few minutes of inactivity, the cause is usually a NAT or firewall somewhere along the path that is closing idle connections. The standard fix is **TCP keep-alive packets** — small empty packets SSH sends periodically to keep the connection from looking idle. Set it in your `~/.ssh/config`:

``` text
# ~/.ssh/config
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

`ServerAliveInterval 60` sends a keep-alive every 60 seconds; `ServerAliveCountMax 3` means “disconnect if three consecutive keep-alives get no reply.” Together, they keep a live session from timing out while still ending quickly if the server actually becomes unreachable.

For long-running tasks, do not rely on keep-alives — rely on the fact that **the job should not die with the connection in the first place**. Run the job inside `tmux` or `screen`, or submit it to a scheduler, so that your SSH client closing is not fatal:

``` bash
# Attach-detach pattern
tmux new -s longjob
python train.py
# Ctrl+b d to detach; session keeps running
# Later: tmux attach -t longjob
```

### “Permission denied” — the three root causes

`Permission denied (publickey)` or `Permission denied (password,publickey)` is the most common failure after the connection itself succeeds. The cause is almost always one of three things, and you diagnose which by running `ssh -v`:

**Wrong username.** You typed your laptop username instead of your account name on the server. Remember that on cloud VMs the username is often `ubuntu`, `ec2-user`, `debian`, or `root` depending on the OS image; it is almost never your laptop name.

**Wrong key offered or no key loaded.** The SSH client offered a key the server does not recognize, or the agent holds no keys at all. `ssh-add -l` lists the keys your agent currently has; `ssh-add ~/.ssh/id_ed25519` adds one. Verify with `-v` that the client is actually offering the key you expect:

``` bash
ssh -v agandler@server.cs.example.edu 2>&1 | grep -i "offering\|accepted\|publickey"
```

**Server-side access control problem.** Your key is correct but the server has not authorized it — the public key was never added to `~/.ssh/authorized_keys` on the server, the file has the wrong permissions, or your account has been disabled. If you have another way into the server (password login, console access, another working key), fix it there. If not, you need to contact whoever administers the server and ask them to install your public key.

## 13.11 Stakes and politics

Remote computing — SSH into a server, push to a cluster, run a job in the cloud — is the workflow that turns a personal laptop into a professional research instrument. It is also, more sharply than almost anything else in this handbook, a workflow shaped by infrastructure privilege. Three things to notice. First, *what kind of network you have*. The defaults assume broadband: low-latency, unmetered, reliable. SSH over a 200 ms satellite link with intermittent disconnection is technically possible but exhausting; running a Jupyter notebook over a port-forwarded tunnel from a coffee-shop hotspot uses real, paid-for data, and on a small monthly plan it adds up fast.

Second, *who can access shared compute*. University HPC clusters gatekeep by institution and account. Major commercial cloud providers (AWS, GCP, Azure) gatekeep by credit card and, in some cases, by passport — students from sanctioned countries are formally barred from creating accounts. The “free tier” most tutorials assume requires a card on file. Third, *whose machines run your code*. Cloud workloads run on servers in specific physical locations under specific national jurisdictions; data placed there inherits those jurisdictions’ surveillance, subpoena, and disclosure regimes. For most coursework this does not matter. For some research, especially with sensitive or regulated data, it matters a lot.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt to carry forward: when a tutorial says “spin up a server in the cloud,” ask whose card pays the bill, whose laws govern the disk it lands on, and whose network needs to be fast enough to make the workflow usable.

## 13.12 Worked examples

### Your first SSH login

You have an account on a department server and you have never logged in before. Three things to confirm: you know your **username**, the **hostname** of the server, and whether your institution requires a **VPN** connection before you can reach it. If a VPN is required, connect to it first. Then SSH in:

``` bash
$ ssh agandler@server.cs.example.edu
The authenticity of host 'server.cs.example.edu (...)' can't be established.
ED25519 key fingerprint is SHA256:abcdef...
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
agandler@server.cs.example.edu's password:
Last login: Mon Apr  7 09:14:22 2026 from 10.0.0.42
[agandler@server ~]$
```

The first prompt is the host fingerprint check — type `yes` (and ideally verify the fingerprint with sysadmin first). The second is your password. After login you see a banner from the server and a shell prompt. Run a couple of commands to orient yourself:

``` bash
[agandler@server ~]$ hostname
server.cs.example.edu
[agandler@server ~]$ whoami
agandler
[agandler@server ~]$ pwd
/home/agandler
[agandler@server ~]$ ls
projects/  scratch/
[agandler@server ~]$ exit
```

That is the entire arc of a basic interactive session. The remote shell is just a shell — every command you know from your local terminal works the same way here, against the server’s own filesystem instead of your laptop’s.

### Moving a dataset to a server

The simplest way to move files is with `scp` (secure copy), which has the same shape as `cp` but with one side being a remote path. The remote path is written as `username@hostname:/absolute/remote/path`. To upload a single file:

``` bash
scp data/raw/sales.csv agandler@server.cs.example.edu:~/projects/sales/data/raw/
```

To upload a whole directory tree, add `-r` for recursive:

``` bash
scp -r data/raw/ agandler@server.cs.example.edu:~/projects/sales/data/
```

After the transfer, log in and verify it actually arrived and is the right size:

``` bash
ssh agandler@server.cs.example.edu "ls -lh ~/projects/sales/data/raw/"
```

For an interactive session where you want to transfer multiple files without retyping the connection, use `sftp` instead — it gives you a small interactive prompt with `cd`, `ls`, `put`, and `get` commands. For very large transfers (gigabytes or more), `rsync` is the right tool because it can resume interrupted transfers and skip files that are already up to date on the destination.

### Running remote Jupyter via an SSH tunnel

You want to run a Jupyter notebook on the server (which has the data and the GPU) but use the notebook in your laptop’s browser. The recipe is two terminals.

In the first terminal, log into the server and start Jupyter, but bind it to `localhost` so it is not exposed to the internet:

``` bash
$ ssh agandler@server.cs.example.edu
[agandler@server ~]$ cd projects/sales
[agandler@server sales]$ source .venv/bin/activate
(.venv) [agandler@server sales]$ jupyter lab --no-browser --ip=127.0.0.1 --port=8888
[I 12:34:56 ServerApp] http://127.0.0.1:8888/lab?token=abc123def456...
```

Copy that URL with the token. In a *second* local terminal, set up the tunnel:

``` bash
$ ssh -N -L 8888:localhost:8888 agandler@server.cs.example.edu
```

The `-N` means “do not open a remote shell, just maintain the tunnel,” and the `-L` means “forward my local port 8888 to the server’s localhost:8888.” Now paste the URL into your local browser. Jupyter loads as if it were running locally; under the hood every keystroke and every cell execution is going through the encrypted tunnel to the server.

When you are done, hit `Ctrl+C` in the tunnel terminal to close the tunnel, and stop Jupyter on the server.

### Launching and securing a small cloud VM

You need a server for an afternoon — to run a long job your laptop cannot handle, or to try something that requires GPU access — and you decide to rent one from a cloud provider. The general workflow is the same on AWS, GCP, and Azure: create an instance, configure SSH access, do your work, and shut it down.

First, in the provider’s web console, create the instance: pick the smallest size that meets your needs (you are paying by the minute), pick a region that is geographically close, and choose an OS image (Ubuntu LTS is a sensible default for most data work). When the instance creation flow asks about an SSH key, paste your *public* key (`~/.ssh/id_ed25519.pub`) — *never* the private key. Configure the firewall (called “security groups” on AWS) to allow inbound SSH (port 22) only from your current IP address, not from `0.0.0.0/0`. The default of “open SSH to the entire internet” is one of the most common ways small cloud servers get compromised within hours of being created.

Once the instance is running, the console will show you its public IP. Connect:

``` bash
ssh -i ~/.ssh/id_ed25519 ubuntu@203.0.113.42
```

Run your job. When you are done — and this is the part students forget — go back to the cloud console and **terminate** (not just stop) the instance, so that you stop paying for storage too. Confirm in the billing dashboard that no resources are still running. Cloud bills can compound quickly if you forget about a forgotten VM, and the failure mode of “I left it running for a month” is a real and expensive mistake.

## 13.13 Exercises

1.  Generate an SSH key pair with a passphrase and identify where keys are stored.

2.  Create an ` /.ssh/config` entry for a host and connect using the alias.

3.  Transfer a directory of files to a server and verify the transfer.

4.  Create a local port forward and access a remote service in your browser.

5.  Connect to a required campus resource through a VPN and note how your network behavior changes.

6.  Cloud practice (if allowed): launch a VM, SSH in, then shut it down and confirm termination.

## 13.14 One-page checklist

- I know whether I need a VPN before SSH.

- I can state: username, hostname, and authentication method.

- My private key is protected (passphrase, correct permissions, not shared).

- I understand host key prompts and do not ignore warnings.

- I can transfer files securely and verify destination paths.

- I can set up a local SSH tunnel for remote services.

- I restrict network exposure (no unnecessary public ports).

- I log out and terminate cloud resources when finished.

## 13.15 Quick reference: common SSH commands

    ssh username@hostname
    ssh -p 2222 username@hostname
    ssh -i ~/.ssh/my_key username@hostname
    ssh -L 8888:localhost:8888 username@hostname
    scp localfile username@hostname:/remote/path/
    sftp username@hostname

## 13.16 Quick reference: vocabulary

SSH  
Secure Shell protocol for encrypted remote access.

VPN  
Virtual Private Network; encrypted connection to a private network.

Tunnel/Port forward  
Using SSH to carry traffic for another service.

Public key  
Shareable key used by the server to verify the corresponding private key.

Private key  
Secret key that proves your identity; must be protected.

Host key  
Server identity fingerprint stored in `known_hosts`.

Security group/firewall  
Rules controlling allowed inbound/outbound network traffic.

> **NOTE:**
>
> - OpenBSD, [OpenSSH manual pages](https://www.openssh.com/manual.html) — the canonical reference for `ssh`, `sshd`, `scp`, `sftp`, and SSH config files.
> - SSH.COM, [SSH Academy](https://www.ssh.com/academy/ssh) — a tutorial-style introduction to keys, agents, tunneling, and common errors.
> - Microsoft, [VS Code Remote - SSH](https://code.visualstudio.com/docs/remote/ssh) — the official guide to editing remote files as if they were local; one of the highest-leverage workflows for student remote work.
> - Michael W. Lucas, [*SSH Mastery*](https://mwl.io/nonfiction/networking#ssh) — a short, practitioner-focused book on SSH keys, agents, jump hosts, and tunneling; covers the corners the official docs leave out.
> - [Mosh: the mobile shell](https://mosh.org/) — an alternative to SSH that survives flaky networks, sleep/wake, and IP changes; the right tool when you are working from anywhere with intermittent connectivity.
> - DigitalOcean, [Community tutorials on SSH and Linux administration](https://www.digitalocean.com/community/tutorials) — well-edited how-tos on cloud and server topics; useful as a second source when official docs assume too much.
> - DEFCON / EFF, [Surveillance Self-Defense: Choosing the VPN that’s right for you](https://ssd.eff.org/module/choosing-vpn-thats-right-you) — a calm, threat-model-driven walk-through of what VPNs do and do not protect you from.
