# Images for automation

Figures in `chapters/automation.qmd`. `tools/shots` writes the table below from `provenance.json`
and rewrites only what is between the two markers. Notes below the table are
for people: what a figure shows that is easy to miss, and what a retake needs.

<!-- shots:begin: generated from provenance.json by tools/shots; edits between these markers are replaced -->
| File | Kind | Captured | Source | How |
|---|---|---|---|---|
| `github-actions-run.png` | capture | 2026-09-24 | https://github.com/cuinfoscience/INFO-Missing-Manual/actions/runs/36055096074/job/107819930522 | tools/shots: Google Chrome for Testing 154.0.8037.57, 800×1100 at 2× |
<!-- shots:end -->

## Notes

- **`github-actions-run`** is one fixed job, the deploy after #38 merged (run #69), viewed signed out: GitHub lists the steps and hides their logs. A retake of the same URL shows the same steps; only "succeeded … ago" changes. If a later workflow change should appear, point the recipe at a newer run and update the alt text's step list.
- The window is 800 px wide and 1100 tall, so all thirteen steps are on screen; the crop keeps only the job panel.
