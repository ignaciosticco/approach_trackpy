# Particle Tracking & Trajectory Overlay

This repository contains small utilities to detect, link, and visualize particle trajectories in frame sequences using trackpy.

> TL;DR: Provide a folder of ordered PNG frames, run the tracker, and get trajectory overlays saved as images you can stitch into a video with ffmpeg.

---

## Contents

run_track.py — Detects features, links them across frames, filters tracks, saves a trajectories file, and generates overlay frames (calls the plotting script internally).

plot_tracking_trajectories.py — Plots cumulative trajectories on top of the original frames and saves overlay images.

run_track_multiparam.py — Random-search over tracking parameters; logs basic stats per parameter set.



---

## Requirements

Python 3.8+

Packages: numpy, pandas, matplotlib, trackpy, pims

Optional: ffmpeg (to convert frames to video)


Install Python packages:

pip install numpy pandas matplotlib trackpy pims


---

## Expected Input / Output

Input: A sequence of images (PNG) in a folder, not a video file. By default:

run_track.py reads input/*.png (expects names like 001.png, 002.png, ...)

run_track_multiparam.py reads input_test/*.png


## Outputs:

data_trajectories.txt — Space-separated file with the filtered, linked trajectories (one row per detection with columns such as x, y, frame, particle).

output2/out_<frame-number> — Overlay images with trajectories drawn up to each frame.

data_trajectories.txt (multiparam summary) — From run_track_multiparam.py, a tab-separated log with parameter values and basic statistics.



You can convert the overlay images to a video using ffmpeg (see below).


---

## Quick Start

1. Prepare frames

Place ordered PNG frames in input/ as 001.png, 002.png, ...

If you start from a video file (e.g., input.mp4), extract frames first:

ffmpeg -i input.mp4 -start_number 1 input/%03d.png



2. Run the tracker

python run_track.py

This will:

Detect and link particles across all frames in input/

Filter tracks (by region and MSD)

Save data_trajectories.txt

Generate overlay frames in output2/



3. Make a video from overlays (optional)

ffmpeg -framerate 25 -i output2/out_%d.png -pix_fmt yuv420p trajectories.mp4



> Note: By default the script iterates frames in chunks and saves out_<frame-number> images. Adjust frame ranges/stride as needed (see the Parameters section).




---

## Parameters & Filtering

Key parameters in run_track.py:

particle_size (odd int) — Approximate particle diameter in pixels for feature detection (e.g., 11).

max_disp — Maximum displacement (pixels) allowed between consecutive frames during linking.

memory — Number of frames a particle can vanish and still be linked.

n_long — Minimum trajectory length (currently commented out in the script; see notes).

n_long_msd — Number of trajectories to keep after ranking by mean squared displacement (MSD) relative to the first point of each track.

Region filter: Tracks with y <= 200 are discarded (t = t[t['y'] > 200]). Adjust or remove as needed.


Frame iteration (at the end of run_track.py):

input_imagenes = ["input/%03d.png" % i for i in range(1,491)] — Expected frame numbers and count.

lista = np.arange(1,490,5) — Chooses frame indices in steps of 5 to generate overlays.

The script calls plot_tracking_trajectories.py for each chunk.


If your frame numbering or count differs, update these ranges accordingly.


---

## How the Visualization Works

plot_tracking_trajectories.py:

Loads data_trajectories.txt and the corresponding source frames passed in via CLI.

For each frame i in the given range, it:

Plots all points from tracks with frame <= i using trackpy.plot_traj(...) over the image.

Fixes axes to image dimensions, flips Y to match image origin, and saves output2/out_<i>.png.



This results in cumulative trajectories that grow over time.


---

## Parameter Search (Optional)

run_track_multiparam.py performs a simple random search over three key tracking parameters:

particle_size (odd values within a range)

max_disp

memory


For each sampled parameter triplet, it:

Runs detection + linking on frames under input_test/

Removes short tracks (threshold n_chicas)

Computes basic per-parameter metrics:

cantidad — number of tracks

mean_l, median_l — mean/median track lengths

mean_msd, median_msd — mean/median MSD over tracks


Appends a line to data_trajectories.txt (configurable via output_name), enabling quick comparison across settings.


> Tip: Use this log to pick a reasonable parameter set for your data. You can then set those values in run_track.py for the actual overlays.


---

## Troubleshooting

No detections or very noisy detections: Tweak particle_size and consider additional feature filters (e.g., minmass, threshold in trackpy.batch).

Broken links / fragmented tracks: Increase max_disp and/or memory.

Overlay size mismatch: Ensure image size is constant across frames; the plot sets fixed axes to the frame size.

Different frame numbering: Update the ranges in run_track.py and the ffmpeg input pattern.



---

MIT License
