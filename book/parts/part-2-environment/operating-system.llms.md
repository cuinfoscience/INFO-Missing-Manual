# 9  Operating System

> **TIP:**
>
> **Prerequisites:** none. This chapter stands on its own.
>
> **See also:** [sec-filesystem](#sec-filesystem), [sec-terminal](#sec-terminal), [sec-pkg-mgmt](#sec-pkg-mgmt).

## Purpose

Your operating system (OS) is the platform that runs everything else: browsers, spreadsheets, programming tools, and file storage. Small OS maintenance mistakes—missed updates, broken permissions, full disks, weak account security, or missing backups—can derail assignments and corrupt data. This chapter gives novice students a practical, low-stress routine for keeping [Windows](https://support.microsoft.com/en-us/windows) and [macOS](https://support.apple.com/guide/mac-help/welcome/mac) stable, updated, and recoverable.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Find key OS settings on Windows and macOS using built-in search and navigation.

2.  Check OS version/build information and interpret what matters for troubleshooting.

3.  Understand types of updates and apply a safe patching workflow.

4.  Set a baseline security posture (account hygiene, screen lock, encryption awareness).

5.  Configure backups and understand restore/recovery options.

6.  Apply a simple troubleshooting playbook (what to try first, what evidence to gather).

7.  Establish a sustainable maintenance schedule for a semester.

## Running theme: stability comes from routines

Most OS problems are predictable. The goal is not perfection; it is consistent, low-effort habits that prevent avoidable failures.

## 9.1 A beginner mental model of the OS

The operating system is the layer that sits between your applications and your hardware, and it is responsible for almost everything that lets a computer feel like a coherent device. It manages your **user accounts**, which is what makes your files separate from someone else’s on the same machine, and it enforces the **permissions** that decide who can read or write what. It owns the **hardware and drivers** — your keyboard, your Wi-Fi card, your storage devices — and translates between them and the apps that need to use them. It runs your **network connections** and your **file system**, launches and stops your applications, and ships its own **updates** along with the built-in security protections that defend you from most casual malware. And when something goes wrong, the OS provides the **recovery tools** that help you get back to a working state.

There is a useful split inside that long list, between the things you should learn to manage yourself and the things you should leave alone. You are in charge of your settings, your updates, your backups, your storage usage, and your accounts — these are the levers that determine whether your computer stays stable. You are explicitly *not* in charge of things like aggressive third-party “cleaner” or “optimizer” apps, registry hacks copied from random forums, drivers downloaded from sketchy websites instead of the vendor’s official site, or any security setting whose effect you cannot articulate in one sentence. Each of those is a category of fix that has hurt many more people than it has helped. The rule of thumb: if you do not understand what a change does, the right action is to not make the change.

## 9.2 Getting oriented: where settings live

On Windows, almost everything you will routinely change lives in the **Settings** app (the gear icon), which has top-level sections for System, Windows Update, Apps, Accounts, and Privacy & Security. There is a separate **Windows Security** app that hosts the things related to Defender and the firewall, and there is also the older **Control Panel**, which Microsoft has been slowly migrating away from but which still holds a few specific tools — File History, for example, lives there on many systems. If you cannot find a setting in the Settings app, the next place to look is Control Panel, and the place after that is to type the name of what you want into the Start menu search box.

On macOS, the analogous hub is **System Settings** (recently renamed from “System Preferences” — older guides may still use that name). The most relevant top-level sections are General, Privacy & Security, and Network. Beyond System Settings there are a handful of utility apps tucked under Applications → Utilities that come up often: **Disk Utility** for managing storage, **System Information** for the comprehensive view of your hardware, and **Activity Monitor** for seeing what is currently using your CPU, memory, and battery.

The single most useful skill on either OS is knowing that the Settings panel has a search box at the top, and that searching for a keyword usually jumps you straight to the right page. You do not need to memorize the menu hierarchy; you need to memorize a small vocabulary of keywords. Type `update`, `backup`, `encryption`, `privacy`, `firewall`, `storage`, or `recovery` into the search box, and you will land on the relevant page faster than navigating through the menus by hand.

## 9.3 Know your system: version, storage, and constraints

Before you troubleshoot anything, know three things about your machine: what version of the OS is running, how much storage is free, and where your files actually live. These are the facts every help channel will ask you for first, and most surprise failures turn out to trace back to one of them.

### Check OS version and build

Record your OS version as part of your baseline notes — the same way you might note your student ID or your office hours. When you search for error messages later, “macOS 14.5” or “Windows 11 23H2” is often the difference between finding a solved question in five seconds and finding nothing at all. Knowing the build number also lets you tell whether an update actually installed.

``` text
Windows:   Settings → System → About
           — look at "OS build" and "Version"
           — or press Win+R, type "winver", press Enter

macOS:     Apple menu → About This Mac
           — look at the macOS name (e.g., Sonoma), version (14.5),
             and build number (click Version for the build)
```

![](graphics/PLACEHOLDER-windows-about.png)

Figure 9.1: ALT: Windows Settings → System → About page, with “OS build” and “Version” fields highlighted so the reader knows exactly where to find them.

![](graphics/PLACEHOLDER-macos-about.png)

Figure 9.2: ALT: macOS “About This Mac” dialog, showing the macOS name, version, and build number.

It helps to understand the three categories of “version” you will see mentioned. A **major version** is the flagship release: Windows 11, macOS Sonoma, macOS Sequoia. These come roughly once a year. A **feature release or minor update** (Windows “feature update,” macOS point release like 14.5 → 14.6) adds capabilities and small changes and comes more frequently. A **security or patch update** is a smaller, targeted fix that shows up more or less monthly — these are the updates you should always install quickly. Keeping the three categories straight tells you how careful to be about any given update: feature and major upgrades deserve planning; security patches deserve speed.

### Check storage health early and often

A surprising number of “my computer is broken” support tickets turn out to be “my disk is 100% full and nothing can write anymore.” Full disks cause Python scripts to fail with cryptic errors, browsers to crash, updates to stall, and notebooks to silently fail to save. Checking free space is the first diagnostic you should learn, and you should do it before you panic about anything else.

``` text
Windows:   Settings → System → Storage
           — shows total, used, and a breakdown by category
           — "Temporary files" and "Downloads" are usually the biggest easy wins

macOS:     Apple menu → About This Mac → More Info → Storage Settings
           — same breakdown, plus a "Manage..." button that lists large files
```

A practical rule of thumb: keep at least **15–20% of your disk free at all times**. Modern SSDs slow down dramatically when they fill up, and the operating system itself needs scratch space for swap, caches, and updates. Running at 1–2% free is asking for trouble — at that point even opening a large spreadsheet can fail. When free space dips below the buffer, clear it: empty the Downloads folder, remove old installers, delete obsolete virtual environments ([sec-virtual-environments](#sec-virtual-environments)), and uninstall apps you are not using.

### Understand local vs synced storage

Cloud sync tools — OneDrive on Windows, iCloud Drive on macOS, Google Drive, Dropbox — blur the line between “the file is on your laptop” and “the file is available if the network is up.” Modern versions of both OneDrive and iCloud default to a “files on demand” mode where files show up in your file browser but are not actually downloaded until you open them. For everyday documents this is convenient. For programming and data work it can be catastrophic, because your script sees a file that *is not really there*, tries to read it, and either hangs for minutes while the OS downloads it or fails with an opaque error.

The fix is to be explicit about what lives locally. For any dataset your code needs, mark it as “Always keep on this device” in the sync client (right-click the folder in the file browser, look for the “Always keep on this device” option in OneDrive, or “Keep Downloaded” in Finder for iCloud). Better still, keep your active project folder — including the `data/raw` directory — *outside* the synced area entirely, and use version control ([sec-git-github](#sec-git-github)) for the code and an explicit data workflow for the datasets. Sync is a backup convenience, not a project filesystem.

``` bash
# Quick sanity check that a file is really local and not a stub:
ls -lh data/raw/sales.csv
# If the size is the actual size (e.g., 4.2M), it's local.
# If it's tiny (a few KB) or the icon shows a cloud, it's a stub.
```

## 9.4 Updates and patching: best practices

### Why updates matter

New security vulnerabilities in operating systems and major applications are discovered routinely — every month or two — and the only practical defense is to install the patches that fix them. Updates also do less dramatic but equally valuable work: they fix reliability bugs that would otherwise crash your apps in mysterious ways, and they ship compatibility fixes that keep your hardware (Wi-Fi, audio, printers) working as those device makers update their own drivers. Skipping updates does not save you time; it just shifts the cost from a planned ten-minute restart into an unplanned multi-hour debugging session at the worst possible moment.

### Types of updates

Not every update is the same. **Security updates** patch known vulnerabilities and are the highest priority: install them as soon as you can, even if they require a restart. **Quality or bug-fix updates** are smaller changes that improve stability; they are usually safe to install whenever they appear. **Feature updates and major upgrades** are larger changes — a new version of macOS, a Windows feature update, a major Office release — and they sometimes break workflows in ways that take time to debug. Treat these as planned events you choose to install on a calm day, not on the morning of a deadline. **Driver and firmware updates** affect specific hardware (graphics cards, Wi-Fi chips, the laptop firmware itself), and you should install them only from your OS’s update mechanism or directly from the hardware vendor’s website — never from third-party “driver finder” sites, which are a major vector for malware.

### A safe patching workflow

Treat patching as a small ritual rather than an interruption. Five steps make the difference between a smooth update and a painful one. **First, back up before you begin** — either by running a backup explicitly or by confirming that your existing backup ran in the last day or two. The point is that if anything goes wrong during the update, you have a known-good state to return to. **Second, pick a good time window**: not the ten minutes before an exam, not while you have unsaved work in twelve open windows, ideally a moment when you can spare twenty minutes and a restart. **Third, install the updates and let them complete**, including any restarts the system asks for. **Fourth, verify your core tools still work** after the restart — open your browser, open a spreadsheet, activate your conda or venv environment, launch Jupyter, run one of your notebooks. This is the cheapest possible regression check, and it catches the common case where an update silently broke a Python interpreter or a kernel registration. **Fifth, write down what changed** if anything is now misbehaving. The OS keeps an update history (Windows Update has it under “Update history”; macOS keeps it under About This Mac → Software Update), and noting the date and version of an update that broke something gives you exactly the information you will need to ask for help.

### Windows update practices

- Know where Windows Update settings live.

- Understand restarts and “active hours”.

- Use pause controls sparingly and intentionally.

- Keep track of optional updates and driver updates.

### macOS update practices

- Know where Software Update settings live.

- Distinguish between point updates (safer) and major upgrades (plan ahead).

- Consider enabling automatic updates, but still check periodically.

## 9.5 Security baseline for students

### Accounts and authentication

The lowest-effort, highest-impact thing you can do for your account security is to use a **password manager** (1Password, Bitwarden, the built-in iCloud Keychain or Microsoft Edge password manager, etc.) and let it generate a unique, long, random password for every site and service. The whole reason password managers exist is that the rule “use a strong, unique password everywhere” is impossible without one. Layered on top of that, **enable multi-factor authentication (MFA)** for your key accounts — your university login, your email, your code-hosting account (GitHub or GitLab), your cloud provider. MFA is the single most effective defense against the most common attack on student accounts, which is a leaked password from a different site being tried against yours. Finally, do your day-to-day work as a **non-administrator account** when the option exists. Administrator privileges should be a thing you elevate to for specific actions (installing software, changing system settings), not the mode you live in.

### Screen lock and physical security

Set your laptop to **require a password on wake**, and set the auto-lock timer short — five minutes is reasonable for a personal laptop, shorter for a shared workspace. The point is not paranoia; it is that an unlocked laptop in a coffee shop is a one-step path to losing all of your work and having someone send embarrassing messages from your accounts. Both Windows and macOS make this configurable in two clicks: on Windows, Settings → Accounts → Sign-in options; on macOS, System Settings → Lock Screen.

### Built-in protections

You almost certainly do not need a third-party antivirus. Both operating systems ship with capable built-in protections that you should learn to find and confirm are turned on. On Windows, the relevant app is **Windows Security** — open it from the Start menu and look at “Virus & threat protection” and “Firewall & network protection.” Both should be enabled. On macOS, the equivalents live under **Privacy & Security** in System Settings, and the model is slightly different: macOS does not ship with a Windows-style antivirus, but it does enforce app sandboxing and prompts you when an app first asks for access to your files, microphone, camera, or location. When those prompts appear, read them before clicking — denying an app the access it does not need is the easiest privacy improvement you will ever make.

### Encryption awareness (and recovery keys)

Disk encryption protects your data if your laptop is lost or stolen — without your password, the disk is unreadable, even to someone who removes it and plugs it into another machine. On Windows the feature is called [**BitLocker**](https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/) (or “device encryption” on consumer editions); on macOS it is called [**FileVault**](https://support.apple.com/guide/mac-help/protect-data-on-your-mac-with-filevault-mh11785/mac). Both are usually on by default on modern hardware, but it is worth confirming.

Encryption introduces exactly one new dependency you must take seriously: the **recovery key**. The recovery key is what unlocks the disk if you forget your password or if something corrupts your account, and it is the only way back in. Both operating systems will offer to store it — in your Microsoft account, your Apple ID, or printed/saved by you somewhere safe. Make sure you know where yours lives, and *write it down somewhere outside your encrypted laptop* before you change anything related to encryption. The cardinal rule is: never proceed with an encryption change you do not understand the recovery for, because the failure mode is “your data is now permanently inaccessible to anyone, including you.”

### Software installation hygiene

Install software only from places you can trust: the vendor’s official website, the platform’s app store (Microsoft Store or Mac App Store), or a reputable package manager ([Homebrew](https://brew.sh/) on macOS, [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) on Windows, [conda](https://docs.conda.io/en/latest/) or [pip](https://pip.pypa.io/en/stable/) in your Python environment). Random “freeware” download sites are one of the most common malware vectors, and they routinely bundle adware and toolbars with whatever you actually wanted. Keep your browser up to date, since the browser is the single program that handles the most untrusted input you encounter. And periodically uninstall software you no longer use — every installed app is a small attack surface, and removing the ones you do not need shrinks the surface for free.

## 9.6 Backups and recovery: the student safety net

Losing a week of coursework to a dead hard drive, a lost laptop, or a mis-typed `rm` command is one of the most demoralizing things that can happen to a student. The cost of setting up a backup once is measured in minutes; the cost of not having one is measured in re-doing work. Get this right before the rest of the chapter.

### What backups are (and are not)

A **backup** is a separate, restorable copy of your data. The word “separate” matters: if the copy lives on the same drive as the original, any failure that takes out the original also takes out the copy. A backup worth trusting lives on a different device — an external drive, a network-attached disk, a cloud service — and it can be restored from that copy to a new machine on demand.

**Cloud sync is not the same thing as a backup.** OneDrive, iCloud Drive, and Dropbox keep your files synchronized across devices, which is wonderful for convenience, but sync *propagates deletions*: delete a file on your laptop and the cloud copy vanishes seconds later, then the copy on your other devices vanishes seconds after that. If your laptop gets infected with ransomware that encrypts your files, the sync client will happily replicate the ransomware’s damage everywhere. Some sync services offer a “version history” or “recently deleted” feature that partially compensates — OneDrive keeps deleted files for thirty days, iCloud keeps them for thirty days — but the window is short and you should never rely on it as your primary safety net.

A backup worth having is **automatic**, **regular**, and **restorable**. Automatic means you do not have to remember to run it; regular means it happens often enough that the worst-case data loss is small (an hour, a day, not a month); restorable means you have *actually verified* that you can get a file back out of it.

### Windows backups (the 2024+ approach)

Windows has two backup stories, and the new one is easier than the old one. **Windows Backup** (Start menu → “Windows Backup”) is a Microsoft-account-based flow that saves your folders, apps, and settings to OneDrive, so that when you sign in on a new Windows PC you can pick up where you left off. This is convenient for laptop replacement but it is *not* a full-system backup and it is bound to how much OneDrive storage you have.

For a real backup, pair that with **File History** writing to an external drive. Plug in a USB drive (any size — 1 TB external drives are cheap), open Control Panel → File History (it still lives in the old Control Panel on most systems; search “File History” from the Start menu), select the drive, and turn it on. File History will copy the contents of your user folders (Documents, Desktop, Pictures, etc.) to the external drive every hour and keep old versions. The result is a versioned archive you can browse by right-clicking any folder and choosing “Restore previous versions.”

``` text
Windows:   Control Panel → File History → Select drive → Turn on
           Settings → Accounts → Windows Backup → configure OneDrive sync
```

### macOS backups with Time Machine

[Time Machine](https://support.apple.com/guide/mac-help/back-up-your-mac-with-time-machine-mh11421/mac) is the simplest good backup tool on any operating system. Plug in an external drive (Time Machine will offer to format it for you; say yes if it is a dedicated backup drive), open System Settings → General → Time Machine, click “Add Backup Disk,” and select it. macOS starts an initial backup immediately and then runs incremental backups every hour the drive is connected.

The under-appreciated feature is how easy Time Machine makes *restoring*. You do not have to wait for a disaster — you can open any folder and click the Time Machine icon in the menu bar, then “Browse Time Machine Backups,” to scroll through every past version of that folder and restore any file from any point in history. This is invaluable for “I accidentally overwrote a paragraph of my thesis two days ago” situations, not just “my laptop died” situations.

``` text
macOS:     System Settings → General → Time Machine → Add Backup Disk
           Menu bar icon → Browse Time Machine Backups (to restore)
```

### Test your restore (the step most people skip)

A backup you have never restored from is a backup you do not really know works. Make this a deliberate exercise the first time you configure backups: pick a small unimportant file, delete it, and then restore it from the backup. On Windows, right-click the parent folder and choose “Restore previous versions,” find your file, and restore it. On macOS, use the Time Machine browser as described above. The whole drill takes five minutes, and afterward you know — not believe, *know* — that the system works and that you can drive it when you need to.

### Recovery tools when something really breaks

Both operating systems include a special **recovery environment** that boots when the normal system will not. You reach it differently on each:

``` text
Windows:   Hold Shift while clicking Restart → Troubleshoot → Advanced options
           — "Startup Repair" for boot problems
           — "System Restore" if restore points were enabled
           — "Reset this PC" as a last resort (keeps or wipes files)

macOS:     Intel:    Hold Cmd+R at startup
           Apple Silicon: Hold the power button until "Options" appears
           — Disk Utility → First Aid to repair the disk
           — Time Machine restore to roll back the whole system
           — Reinstall macOS (keeps your files in most cases)
```

The recovery environment is the tool of last resort. You reach for it when the system will not boot, when the disk is showing errors, or when something has corrupted the OS badly enough that normal fixes do not work. Because it is rare, most students do not think about it until they need it — at which point they panic. The better move is to *know the keystroke that gets you into recovery mode on your specific machine*, written down somewhere outside the machine, so that when the emergency comes you spend zero time Googling “how do I boot my Mac into recovery.”

## 9.7 Performance and stability maintenance

The goal of this section is not to make your computer “fast” — that is what marketing copy promises. The goal is to prevent the everyday conditions that make a computer *slow* or *unreliable*, and to do so without accidentally breaking anything. The emphasis is on safe, reversible changes you can make with confidence.

### Storage cleanup (do no harm)

The right cleanup targets are the ones you can identify by sight: old installers in Downloads, duplicate copies of large files, archived projects you know you are done with, and the “temporary files” cache the OS is happy to flush. The wrong targets are files you do not recognize, especially anything inside system folders or hidden directories — when in doubt, do not delete.

Use your OS’s built-in storage view first, because it already knows what is safe to remove and what is not:

``` text
Windows:   Settings → System → Storage → Storage Sense
           — "Cleanup recommendations" flags large files, unused apps,
             and temp files that are safe to remove
           — Storage Sense can also auto-clean Downloads and Recycle Bin
             after N days

macOS:     Apple menu → About This Mac → More Info → Storage Settings → Manage
           — "Recommendations" lists large unused files and old iOS backups
           — "Review Files" sorts by size so you can see what is eating space
```

For finding genuinely large files that the built-in tools missed, a dedicated disk-usage visualizer like WinDirStat (Windows) or GrandPerspective / DaisyDisk (macOS) paints a map of your disk where the biggest rectangles are the biggest files. This is often the fastest way to find “oh, I had a 40 GB video project sitting in a folder I forgot about.”

**Never delete files whose purpose you do not know.** Hidden system directories (`C:\Windows`, `/System`, `/Library`, `~/Library` on macOS) contain things your OS and your apps rely on. Removing something in there to free space almost always breaks something later, and the breakage will show up far enough from the delete that you will not connect the two.

### Startup and background apps

Every app that launches at login spends some of your CPU, memory, and battery before you even open your first window, and a laptop that loads twenty of them at login feels permanently sluggish. Most of those apps added themselves to the startup list the first time you installed them, without asking, and most of them do not need to be there.

``` text
Windows:   Settings → Apps → Startup
           — toggle off anything with "High impact" that you don't need
             immediately at login
           — or: Task Manager → Startup apps tab for the same list

macOS:     System Settings → General → Login Items & Extensions
           — "Open at Login" shows apps that launch at sign-in; click the minus
             to remove the ones you don't need
           — "Allow in Background" shows helper processes that run even when
             their parent app isn't open
```

Disable anything you do not use regularly — updater daemons for apps you rarely open, cloud sync clients for services you no longer use, hardware “companion apps” for peripherals you no longer own. Log out and back in to see the effect. This is reversible: if you turn something off and an app stops working properly, you can turn it back on in the same settings panel.

### Battery, heat, and laptop health

Laptops throttle themselves when they get hot. If your computer is permanently running its fans at full speed or living at 95 °C, it is also permanently running slower than it should. The fix is almost never software — it is airflow. Do not use a laptop on a blanket or a bed for extended work; the cushion blocks the intake vents on the bottom. Once or twice a semester, with the laptop off, use a can of compressed air to clear dust from the visible fan intakes. If the fan is audibly louder than it was a year ago, the inside is probably dusty.

Battery health on modern laptops is something the OS will tell you about directly. On macOS, System Settings → Battery shows “Maximum Capacity” as a percentage of the original design capacity; anything below about 80% is a good candidate for a service appointment. On Windows, `powercfg /batteryreport` at the command line generates an HTML report of your battery’s full charge capacity history:

``` bash
# Windows (Command Prompt or PowerShell):
powercfg /batteryreport /output "battery.html"
# Open the generated file to see capacity vs. design capacity.
```

A failing charger can also cause mysterious reliability problems — the machine suddenly suspends, or the battery never quite reaches full charge. If you suspect the charger, try a different known-good one before blaming the laptop.

### Drivers and peripherals

Drivers are the OS’s interface to your hardware, and they are the single category of update where “install it from the wrong place” can cause real damage. The rule is simple: **install drivers only from the OS’s own update mechanism or directly from the hardware vendor’s official website.** Do not download drivers from third-party “driver finder” or “driver updater” sites — they are, without exaggeration, one of the most common sources of adware and malware on student laptops.

For printers, the easiest reliable workflow is to let the OS auto-detect the printer and install a generic driver, then install the manufacturer’s official app only if you need specific features. For Wi-Fi and Bluetooth, driver updates usually come through the regular OS update channel and you should not need to touch them manually.

When a peripheral misbehaves — the printer refuses to connect, the external monitor shows the wrong resolution — the information a help channel will want is specific: the exact device model (usually on a sticker), the exact OS version, the exact error message, and what changed recently. Write those down before you ask for help; they halve the time to resolution.

## 9.8 Troubleshooting playbook (student-friendly)

When your computer stops working the way you expect, the temptation is to try fifteen things at once in a panic. The reliable way is the opposite: a short ordered list of the cheapest diagnostics, applied one at a time, until the problem either resolves or becomes clearer. The playbook below is deliberately boring — almost all OS-level problems fall to the first few steps.

### Start with the simplest reversible steps

Before anything clever, try these in order. Each one takes under a minute. Most problems do not survive past step three.

1.  **Restart the affected app.** Quit it completely — not just close the window, actually quit — and reopen it. On macOS, `Cmd+Q` is “quit,” not `Cmd+W`, which only closes the window. On Windows, check the system tray for minimized apps and right-click → Exit. About a third of all “app is broken” symptoms are cleared by this one step.
2.  **Restart the computer.** The cliché “have you tried turning it off and on again” is a cliché because it works. A clean restart clears leaked memory, resets hung background processes, reinitializes drivers, and finishes any pending updates. Do a full Shutdown → Start, not just Sleep → Wake, because sleep does not actually reset anything.
3.  **Check free disk space.** Use the method from earlier in this chapter. If you are below ~5% free, that is very likely your actual problem. Free some space before anything else.
4.  **Check network connectivity.** Can you open a different website? Does a different app on the same network work? Is the Wi-Fi icon showing connected? Many “the app is broken” reports are actually “my Wi-Fi disconnected and the app handled it badly.”
5.  **Identify what changed recently.** Did you install something in the last day? Did an OS update run overnight? Did you change a setting? The vast majority of “it was working yesterday” problems are caused by a specific, findable recent change.

If none of the first five steps resolved the problem, you know the issue is real and you can escalate to more involved diagnostics. But start here every time — you will often skip the escalation entirely.

### Use safe mode when normal startup fails

Both operating systems have a **safe mode** that boots with the minimum set of extensions and drivers. Safe mode is the right tool when the normal boot is either failing or producing a system that is so broken you cannot troubleshoot from inside it.

``` text
macOS (Apple Silicon):  Shut down → hold the power button until "Loading
                        startup options" appears → select the disk while
                        holding Shift → "Continue in Safe Mode"
macOS (Intel):          Hold Shift at power-on until the login screen
                        appears. "Safe Boot" will be visible in the menu bar.

Windows:                Hold Shift while clicking Restart → Troubleshoot →
                        Advanced options → Startup Settings → Restart →
                        press F4 or F5 for Safe Mode
```

If your machine works fine in safe mode but fails in normal mode, the problem is something that loads at normal startup — a third-party driver, a login item, a background extension. Reboot back to normal, disable the suspects one at a time, and the one that fixes the problem is your culprit.

### Gather evidence before asking for help

When the playbook runs out and you need to ask a TA or a help channel, the quality of your question determines how quickly you get an answer (see [sec-asking-questions](#sec-asking-questions)). The minimum evidence to collect:

- **OS version and build** (from the section earlier in this chapter).
- **Device model** (Windows: Settings → System → About → “Device specifications”; macOS: Apple menu → About This Mac).
- **Free disk space** — because this is the first thing anyone will ask.
- **The exact error message.** Not “it says there’s an error.” The exact text, copy-pasted if possible, or a screenshot if the text cannot be selected.
- **When the error happens.** At startup? When you open a specific app? After a specific action?
- **Steps to reproduce.** What do you do, in order, that triggers the problem? Can you trigger it on demand, or is it intermittent?
- **What changed recently.** Updates installed, apps installed or removed, settings changed, files moved.

Prefer copy-pasted text to screenshots. Screenshots cannot be searched, quoted, or fed into a search engine to find other people with the same problem. Use screenshots when the error is a graphical element (a dialog without selectable text, a broken layout) but copy the text whenever you can. See [sec-asking-questions](#sec-asking-questions) for the fuller treatment of how to write a good help request.

## 9.9 A semester maintenance schedule

The point of a schedule is to spread small amounts of maintenance across the semester so that nothing ever stacks up into an emergency. The schedule below is intentionally lightweight — the entire thing takes about an hour a month — and the whole goal is to make sure you never have to think “oh no, I haven’t backed up in six weeks” at 11 PM the night before a deadline.

### Weekly rituals (about 10 minutes)

Once a week, ideally at the same time (end of your Sunday study session is a common choice), run through a short health check:

``` text
Weekly checklist:
[ ] Check for pending OS updates; install security patches
[ ] Confirm the last backup ran within the past day
[ ] Glance at free disk space; clean up if under 15%
[ ] Empty the Trash / Recycle Bin
[ ] Restart the computer at least once this week
```

The “restart once a week” line is easy to forget because modern laptops suspend on close and can go weeks without a real restart, which lets background processes and memory leaks accumulate. A fresh reboot on Sunday night is the cheapest way to start the week with a clean slate.

### Monthly deep check (about 20–30 minutes)

Once a month, do the slightly longer review that covers the things that do not change quickly enough to need weekly attention:

``` text
Monthly checklist:
[ ] Install any pending feature updates (if you have time to recover)
[ ] Review and prune startup / login items
[ ] Uninstall apps you haven't used in months
[ ] Glance at the Downloads folder and clear it out
[ ] Verify the backup by restoring one random file
[ ] Update your primary editor and its extensions
[ ] Update conda, pip, and any other package managers you rely on
```

The “verify the backup by restoring one random file” line is the most important and the easiest to skip. A backup you have never restored from is a claim, not a guarantee. Spending two minutes once a month to confirm it still works is cheap insurance.

### Before major milestones (projects, finals, deadlines)

In the week leading up to a big deadline or an exam, the strategy changes: minimize risk rather than maximize capability. The rule is **do not change anything you do not have to**. Specifically:

``` text
Pre-deadline checklist:
[ ] Backups are current AND you have verified you can restore from them
[ ] Free disk space is above 15%
[ ] Do NOT install major OS upgrades or feature updates
[ ] Do NOT upgrade conda, pip, or any package in your active environment
[ ] Confirm your core tools still run end-to-end:
    - editor opens the project
    - conda/venv activates
    - jupyter notebook launches
    - the project's main script or notebook runs from a clean start
[ ] Have a second machine or cloud backup available for emergency access
```

The last point is worth thinking about seriously. What is your plan if your laptop dies at 8 PM the night before a submission? If the answer is “I don’t know, I’d panic,” spend an hour now making a plan: pushing your code to GitHub, knowing where a library or lab computer is, having a lightweight workflow that could run on a borrowed machine. The plan does not have to be fancy — it just has to exist before you need it.

> **NOTE:**
>
> - [Microsoft Support: Windows](https://support.microsoft.com/en-us/windows) — the canonical help portal for Windows updates, backups, and security.
> - [Apple Support: Mac](https://support.apple.com/guide/mac-help/welcome/mac) — the Mac User Guide, covering Software Update, Time Machine, and FileVault.
> - [StaySafeOnline: Cybersecurity Basics](https://staysafeonline.org/online-safety-privacy-basics/) — a plain-language primer on passwords, MFA, and account hygiene.

## 9.10 Worked examples

### Setting up a safe update routine

You want to make sure your operating system stays patched without having an update interrupt you in the middle of an exam. The setup is the same shape on both operating systems. On Windows, open Settings → Windows Update, confirm that “Check for updates” finds nothing pending, and click “Advanced options” to set your **active hours** — the window each day during which Windows will not restart you. Pick something that covers your normal class and study time. On macOS, open System Settings → General → Software Update, click the small (i) next to “Automatic updates,” and turn on “Check for updates,” “Download new updates when available,” and “Install macOS updates.” The actual restart is still up to you, but you no longer have to remember to check.

Once that is configured, build the habit of installing pending updates on a quiet day rather than ignoring the notifications until the next reboot is forced. Ten minutes once a week is much cheaper than an unplanned forty-minute update at 2 AM the night before a deadline.

### Configuring backups and testing a restore

On Windows, the easiest reliable backup approach is **File History** to an external drive. Plug in the drive, open Settings → System → Storage → Advanced storage settings → Backup options (or, on older systems, Control Panel → File History), and turn on automatic backups to that drive. Set a schedule (hourly is fine; the deltas are small) and confirm that the most recent backup time updates after a few minutes. On macOS, the equivalent is **Time Machine**: plug in an external drive, open System Settings → General → Time Machine, click “Add Backup Disk,” and select it. macOS will start an initial backup immediately and then run incremental backups every hour while the drive is connected.

Setting up a backup is the easy half. The half people skip is *testing the restore*, which is the only proof that the backup actually works. Pick a small unimportant file, delete it, and recover it from your backup. On Windows, right-click the folder it lived in and choose “Restore previous versions.” On macOS, click the Time Machine icon in the menu bar and choose “Browse Time Machine Backups,” then navigate back in time to the version you want and click “Restore.” Once you have done this once, you know the system works and you know how to use it under stress. The restore drill is also the moment you discover any problems — wrong drive, missing folder coverage, permissions issue — at a time when fixing them is cheap.

### Recovering from a broken update

Sometimes an update breaks something. You install Windows updates and your Wi-Fi stops working, or you upgrade macOS and a key app refuses to launch. The recovery move depends on how bad it is.

The first step is to figure out what changed. On Windows, Settings → Windows Update → Update history lists every recent update with dates and KB numbers. On macOS, System Settings → General → About → System Report → Installations shows a similar list. Cross-reference the failure date with the install date — if the failure started immediately after a specific update, that update is your suspect. Search for the KB number or update name plus the symptom; if it is a known issue, others have already hit it and the workaround is usually documented.

If you need to roll the update back, both OSes provide that. Windows lets you uninstall recent updates from the same Update history page. macOS does not allow you to roll back an OS update directly, but Time Machine can restore the entire system from a backup made before the update — which is the reason you set up backups in the first place. As a last resort, both systems have a recovery mode (Shift+Restart on Windows, Command+R at boot on Macs with Intel chips, or hold the power button on Apple Silicon) that boots into a small repair environment where you can reset, restore, or reinstall the operating system. Treat reinstallation as a real but final option — it works, but it is hours of effort, and it requires a backup that you have already verified.

## 9.11 Exercises

1.  Record your OS version/build and device model in a troubleshooting note.

2.  Find the update settings page and take a screenshot of where you would check for updates.

3.  Configure a backup (Windows Backup/File History or Time Machine) and verify the last backup time.

4.  Locate your encryption setting (Windows device encryption/BitLocker or macOS FileVault) and write down where the recovery key would be stored (do not paste the key into your notes).

5.  Identify and disable one unnecessary startup/login item.

6.  Simulate a recovery: restore one older version of a document from backup.

## 9.12 One-page checklist

- I can find key settings (updates, backups, security, storage).

- I know my OS version/build and can report it.

- Updates are enabled and I install them on a schedule.

- I avoid major upgrades right before deadlines.

- Backups are configured, recent, and I have practiced a restore.

- I keep adequate free disk space.

- Screen lock is enabled and accounts use strong authentication.

- I understand encryption recovery keys and where they are stored.

- I can follow a basic troubleshooting playbook and gather evidence.

## 9.13 Quick map: where common settings live

### Windows (typical)

- **Windows Update:** Settings → Windows Update

- **Security:** Windows Security app; Settings → Privacy & security

- **Recovery:** Settings → System → Recovery

- **Backups:** Settings → Accounts/Backup areas; Control Panel for File History (on many systems)

### macOS (typical)

- **Software Update:** System Settings → General → Software Update

- **Privacy & security:** System Settings → Privacy & Security

- **Encryption:** Privacy & Security → FileVault

- **Backups:** System Settings → General → Time Machine

An operating system manages all of the resources that you interact with while using a computer. For instance, it manages input from the keyboard, what is displayed on a screen, and how you open and close programs. When you interact with your computer, you are interacting with the operating system. For instance, Windows is an operating system.

Keeping your operating system up-to-date ensures that you have the latest features, security, and bug fixes.
