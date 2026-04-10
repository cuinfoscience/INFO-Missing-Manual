# 12  Remote Computing

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-terminal](#sec-terminal).
>
> **See also:** [sec-git-github](#sec-git-github), [sec-automation](#sec-automation), [sec-collaboration](#sec-collaboration).

## Purpose

Remote computing lets you use resources that are not physically on your laptop: university servers, high-performance clusters, lab machines, and cloud instances. This chapter teaches novices how to connect safely and reliably using SSH and VPNs, move files, run remote jobs, and use tunneling to access remote services (including Jupyter) as if they were local.

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

## 12.1 A beginner mental model

### Local vs remote

- **Local machine:** your laptop/desktop.

- **Remote machine:** a computer you access over the network.

- **Network:** the path between them (campus, home Wi-Fi, internet).

### Client/server language

- **Client:** the tool you run locally (SSH client, VPN client, browser).

- **Server:** the remote service or machine you connect to (SSH server, web server).

### Sessions, processes, and persistence

- A remote **SSH session** is a connection + a shell.

- Programs you start remotely may stop when your session ends unless you use job control tools.

- Remote computers have their own file system, users, permissions, and installed software.

### Why remote computing exists

- Access to more CPU/RAM/GPU.

- Access to shared datasets and licensed tools.

- Reliability (servers run longer than laptops).

- Collaboration (shared environments).

## 12.2 Prerequisites and safe defaults

### Accounts and credentials

- You need: a username, a host address, and an authentication method.

- Prefer: institutional identity + MFA, and key-based SSH.

### Install/locate your tools

- **macOS:** Terminal includes `ssh`, `scp`, `sftp`.

- **Windows:** OpenSSH client is commonly available; otherwise enable/install it.

- Optional: a code editor that supports remote development.

### Golden safety rules

- Never share passwords or private keys.

- Never paste secrets into commands or notebooks.

- Assume your command history is readable by future you (and sometimes by administrators).

- Use the minimum access needed; log out when done.

## 12.3 SSH fundamentals

### What SSH provides

- Encrypted remote login.

- Secure file transfer.

- Secure tunneling of other network traffic.

### The simplest connection

    ssh username@hostname

- You may need `-p <port>` if SSH uses a nonstandard port.

- The first time you connect, SSH will ask about the host fingerprint.

### Host identity and `known_hosts`

- SSH remembers server fingerprints to prevent “man-in-the-middle” attacks.

- Warning: a changed fingerprint may be benign (server rebuilt) or dangerous (impersonation).

- Best practice: verify changes via a trusted channel (course staff / sysadmin).

### Authentication: passwords vs keys

- **Password:** easy to start, less secure, often disabled on managed servers.

- **Keys:** recommended; a private key stays on your device and proves identity.

### Key-based authentication basics

- A key pair: **private key** (secret) + **public key** (shareable).

- The public key is added to the server’s authorized keys list.

- Protect the private key with a passphrase.

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

## 12.4 File transfer: getting data in and out

### The basic question: where is the file?

- ‘Local path’’ (your computer) vs ‘remote path’’ (server).

- Use absolute paths if you are unsure.

### Secure copy (`scp`)

- Good for quick transfers and scripts.

- Learn directory copies (recursive) and quoting paths with spaces.

### SFTP (`sftp`)

- Interactive file transfer session.

- Many GUI tools use SFTP under the hood.

### What not to do

- Do not email datasets or copy them into unapproved cloud storage.

- Do not move large files through a slow interactive session if a better transfer method exists.

## 12.5 Tunneling and port forwarding (making remote services usable)

### Why tunneling exists

- Many services (Jupyter, databases, dashboards) bind to `localhost` on the server for safety.

- A tunnel lets your local machine reach that service through an encrypted channel.

### Local forwarding (most common)

- Scenario: remote server runs a service on `127.0.0.1:8888`; you want to open it in your local browser.

&nbsp;

    ssh -L 8888:localhost:8888 username@hostname

- Then visit `[http://localhost:8888`\](http://localhost:8888) in your local browser.

- If `8888` is taken locally, choose another local port (e.g., 8899).

### Remote forwarding (advanced)

- Scenario: you need the remote machine to reach a service running locally.

- Use cautiously; it changes the exposure model.

### Dynamic forwarding (SOCKS proxy)

- Scenario: route a browser or tool through the remote network.

- Use only when you understand policies and implications.

### Tunnel hygiene

- Use `-N` when you only need forwarding (no remote shell).

- Prefer binding to `localhost` on your machine to avoid exposing ports to others.

- Close tunnels when you are done.

## 12.6 VPN fundamentals

### What a VPN does (student-relevant)

- Creates a secure network path to a private network (campus/lab).

- Makes your device behave as if it is “on campus” for protected resources.

- Often required to reach SSH hosts that are not publicly reachable.

### When you need a VPN

- Accessing university resources from off campus.

- Using internal-only hosts, file shares, or licensed services.

- Connecting to a protected cluster login node.

### Common VPN pitfalls

- VPN drops cause SSH disconnections.

- Split-tunneling vs full-tunneling changes which traffic goes through the VPN.

- Some VPNs interfere with local networking (printers, local dev servers).

### Practical advice

- Connect VPN first, then SSH.

- If you lose connection, reconnect VPN and re-establish SSH; do not assume remote processes survived.

- Learn where your VPN client shows connection status and logs.

## 12.7 Remote work patterns: from simple to professional

### Pattern 1: login node + compute node (HPC concept)

- You SSH into a **login node** for editing and job submission.

- Actual computation runs on separate nodes via a scheduler.

- Rule: do not run heavy jobs on login nodes.

### Pattern 2: remote development

- Edit locally and run remotely, or edit remotely using a remote extension.

- Keep projects in version control; avoid manual copying back and forth.

### Pattern 3: notebooks on servers

- Start Jupyter remotely.

- Use SSH local port forwarding to access it.

- Prefer passwords/tokens and binding to `localhost`.

## 12.8 Cloud computing basics (what novices must know)

### What “the cloud” is

- Renting computing resources (virtual machines, storage, managed services).

- You control enough to break things, including security.

### Core terms

Instance/VM  
A rented computer.

Region/zone  
Where the machine physically resides.

Storage  
Object storage (buckets) vs attached disks.

Networking rules  
Firewalls/security groups controlling inbound/outbound.

### A safe “first cloud VM” workflow

1.  Create the instance in a region.

2.  Create or choose an SSH key pair.

3.  Configure inbound access: allow SSH only from your IP (not from the whole internet).

4.  Connect via SSH.

5.  Shut down/terminate when finished to control cost.

### Cost and risk

- Cloud resources cost money while running (and sometimes while stored).

- Set budget alerts if available.

- Do not expose services publicly unless required and reviewed.

## 12.9 Security best practices for remote computing

### Key hygiene

- Use passphrases; do not store private keys in shared folders.

- Avoid key sprawl: use separate keys per purpose if required, and retire unused keys.

- If a key might be compromised, rotate it immediately.

### Least privilege and separation

- Use non-admin accounts for daily work.

- Use sudo/admin only when necessary.

- Keep data access minimal and policy-compliant.

### Safe networking defaults

- Restrict inbound ports (SSH only; no public databases).

- Prefer tunnels over opening ports.

- Keep software patched on remote machines.

### Logging and traceability (student level)

- Keep a small “remote session log”: what host, what you did, what changed.

- Use version control for code changes.

## 12.10 Troubleshooting and diagnostics

### Connection failures

- Check: internet, VPN status, host name, username.

- Check: port and firewall rules.

- Check: key permissions and correct key selection.

### Host key warnings

- Do not ignore.

- Verify with a trusted source before accepting changes.

### Timeouts and unstable connections

- Use keep-alives if permitted.

- Prefer running long tasks via schedulers or detached sessions.

### “Permission denied”

- It may be the wrong username.

- It may be the wrong key.

- It may be a server-side access control issue.

## 12.11 Worked examples (outline)

### Example 1: First SSH login

- Verify prerequisites (account, host, VPN).

- Connect and interpret the login banner.

- Navigate remote directories and run a simple command.

### Example 2: Move a dataset to a server

- Identify local and remote paths.

- Transfer with `scp` or `sftp`.

- Verify integrity (file size, checksums if taught).

### Example 3: Remote Jupyter via SSH tunnel

- Start Jupyter on the server bound to `localhost`.

- Create a local tunnel.

- Connect in browser; close tunnel when done.

### Example 4: Launch and secure a small cloud VM

- Create instance; restrict inbound SSH to your IP.

- SSH in; run a short job.

- Terminate instance; confirm costs stop accruing.

## 12.12 Exercises

1.  Generate an SSH key pair with a passphrase and identify where keys are stored.

2.  Create an ` /.ssh/config` entry for a host and connect using the alias.

3.  Transfer a directory of files to a server and verify the transfer.

4.  Create a local port forward and access a remote service in your browser.

5.  Connect to a required campus resource through a VPN and note how your network behavior changes.

6.  Cloud practice (if allowed): launch a VM, SSH in, then shut it down and confirm termination.

## 12.13 One-page checklist

- I know whether I need a VPN before SSH.

- I can state: username, hostname, and authentication method.

- My private key is protected (passphrase, correct permissions, not shared).

- I understand host key prompts and do not ignore warnings.

- I can transfer files securely and verify destination paths.

- I can set up a local SSH tunnel for remote services.

- I restrict network exposure (no unnecessary public ports).

- I log out and terminate cloud resources when finished.

## 12.14 Quick reference: common SSH commands

    ssh username@hostname
    ssh -p 2222 username@hostname
    ssh -i ~/.ssh/my_key username@hostname
    ssh -L 8888:localhost:8888 username@hostname
    scp localfile username@hostname:/remote/path/
    sftp username@hostname

## 12.15 Quick reference: vocabulary

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
