import os
import glob
import re
import threading
from multiprocessing import Pool, Manager
import cv2
import numpy as np
import stag
import skimage.draw
import scipy.ndimage
from tqdm import tqdm
import queue as queue_module  # for queue.Empty exceptions
import multiprocessing
multiprocessing.set_start_method('spawn', force=True)
import sys
import ttkbootstrap as ttk
from STag_Convert_GUI import STag_Convert_GUI, load_settings
import threading
import tkinter as tk
from tkinter import messagebox
import time


    


def show_initial_info():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo(
        title="Reminder to prepare your data",
        message=(
            "This is a reminder: \n\n"
            "Please place your videos in the 'Videos_to_analyse' folder.\n\n"
            "Each subfolder inside it should contain .npz files.\n"
            "The program will create one video per subfolder.\n\n"
            "Click OK to proceed to settings."
        )
    )
    root.destroy()


colour_palette = [
    (255, 0, 0),      # red
    (0, 255, 0),      # green
    (0, 0, 255),      # blue
    (255, 255, 0),    # yellow
    (0, 255, 255),    # cyan
    (255, 0, 255),    # magenta
    (255, 128, 0),    # orange
    (128, 0, 255),    # violet
    (0, 128, 255),    # light blue
    (128, 255, 0),    # lime
    (255, 0, 128),    # pink
    (128, 128, 0),    # olive
    (0, 128, 128),    # teal
    (128, 0, 128),    # purple
    (255, 153, 51),   # apricot
    (102, 255, 102),  # light green
    (102, 102, 255),  # periwinkle
    (255, 102, 178),  # rose
    (255, 204, 0),    # gold
    (0, 204, 153),    # turquoise
    (153, 51, 255)    # amethyst
]

def getOrder(x):
    try:
        return int(re.search(r'_(\d{6})_\d+frames\.npz$', x).group(1))
    except Exception:
        return 999999

def runVideoTagDetection(colour_palette, stag_libraries, frame_reconstruction, filename_addon, n_cols, display_recentID_bar):
    if n_cols == 1:
        colour_coding = False
        display_recentID_bar = False
    else:
        colour_coding = True
    fnames = [f for f in os.listdir('Videos_to_analyse')
              if os.path.isdir(os.path.join('Videos_to_analyse', f))]

    # get WIDTH and HEIGHT from first frame
    if not fnames:
        print("\nExiting program due to: \nNo videos found in the 'Videos_to_analyse' folder. Please add videos and re-run.")
        sys.exit()
    files = glob.glob(os.path.join('Videos_to_analyse', fnames[0], '*.npz'))
    npz_data = np.load(files[0], allow_pickle=True)
    bsr_matrix = npz_data['bsr_matrix'][0]
    WIDTH, HEIGHT = bsr_matrix.shape

    display_width = 2028
    display_height = 1520
    input_resolution_factor = WIDTH / display_width
    output_zoom_x = display_width / WIDTH
    output_zoom_y = display_height / HEIGHT

    output_dir = "Analysed_videos"
    os.makedirs(output_dir, exist_ok=True)

    args = [
        (fname, colour_palette, frame_reconstruction, filename_addon, n_cols, WIDTH, HEIGHT,
         display_width, display_height, input_resolution_factor, output_zoom_x, output_zoom_y,
         output_dir, colour_coding, stag_libraries, display_recentID_bar)
        for fname in fnames
    ]

    return args  # return the list of arguments

def detect_markers_and_assign_colours(grey, recentIDs, available_colours, display_width, display_height, colour_coding, stag_libraries, n_cols, print_buffer):
    grey_8bit = grey.astype(np.uint8)
    img = 255 - grey_8bit
    render = np.repeat(grey_8bit.copy()[:, :, np.newaxis], 3, axis=2)
    frame_corners = []
    frame_ids = []
    temp_hold = []
    new_ids = []
    for libraryHD in stag_libraries:
        corners, ids, _ = stag.detectMarkers(img, libraryHD) #
        frame_corners.extend(corners)
        frame_ids.extend((libraryHD) * 1000 + ids)
    if colour_coding:
        for marker_id in frame_ids:
            found = False
            for row in recentIDs:
                if row[0] == marker_id:
                    temp_hold.append(row.copy())
                    recentIDs.remove(row)
                    found = True
                    break
            if not found:
                new_ids.append([marker_id])
        total_rows = len(recentIDs) + len(temp_hold) + len(new_ids)
        if total_rows > n_cols:
            x = total_rows - n_cols
            for row in recentIDs[-x:]:
                available_colours.append(row[1])
            recentIDs = recentIDs[:-x]
        if new_ids:
            for i in range(len(new_ids)):
                if available_colours:
                    new_ids[i].append(available_colours.pop())
                else:
                    print_buffer.append('Number of tags detected exceeds the number of unique colours. Please change "n_col"')
        recentIDs = temp_hold + new_ids + recentIDs
    return img, render, frame_corners, frame_ids, recentIDs, available_colours

def apply_overlay(img, render, corners, ids, recentIDs, input_resolution_factor, output_zoom, colour_coding):
    for i, marker in enumerate(corners):
        marker = marker[0]
        marker_id = ids[i]
        if colour_coding:
            color = next((row[1] for row in recentIDs if row[0] == marker_id), None)
        else:
            color = (0, 0, 255)
        assert marker.ndim == 2
        single_marker_mask = np.zeros_like(render[:, :, 0], dtype=bool)
        rr, cc = skimage.draw.polygon_perimeter(marker[:, 1], marker[:, 0], render.shape[:2])
        single_marker_mask[rr, cc] = True
        single_marker_mask = scipy.ndimage.binary_dilation(single_marker_mask, iterations=4)
        render[single_marker_mask, :] = color

        center_x = int(np.mean(marker[:, 0]))
        center_y = int(np.mean(marker[:, 1]))
        height, width = render.shape[:2]
        if center_x - 75 < 0:
            text_x = center_x + 30
        else:
            text_x = center_x - 75
        if center_y - 35 < 0:
            text_y = center_y + 50
        else:
            text_y = center_y - 20
        cv2.putText(render, str(marker_id[0]), (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5 * (input_resolution_factor / output_zoom), color,
                    int(round(1 * (input_resolution_factor / output_zoom))))
    return render

def pad_to_size(image, target_width, target_height, pad_color=(0, 0, 0)):
    img_h, img_w = image.shape[:2]
    aspect_ratio = img_w / img_h
    target_ratio = target_width / target_height

    if aspect_ratio > target_ratio:
        new_w = target_width
        new_h = int(target_width / aspect_ratio)
    else:
        new_h = target_height
        new_w = int(target_height * aspect_ratio)

    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    top = (target_height - new_h) // 2
    bottom = target_height - new_h - top
    left = (target_width - new_w) // 2
    right = target_width - new_w - left

    padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=pad_color)
    return padded

def process_single_video(args):
    (fname, colour_palette, frame_reconstruction, filename_addon, n_cols, WIDTH, HEIGHT,
     display_width, display_height, input_resolution_factor, output_zoom_x, output_zoom_y,
     output_dir, colour_coding, stag_libraries, display_recentID_bar, print_buffer, queue) = args

 

    recentIDs = []
    available_colours = colour_palette.copy()

    try:
        files = glob.glob(os.path.join('Videos_to_analyse', fname, '*.npz'))
        files = sorted(files, key=getOrder)
        total_files = len(files)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        videoname = os.path.join(output_dir, f'{fname}_TagsDetected_{filename_addon}.mp4')
        out = cv2.VideoWriter(videoname, fourcc, 5, (display_width, display_height), isColor=True)

        for i, fn in enumerate(files):
            npz_data = np.load(fn, allow_pickle=True)

            frame_ids = npz_data['frameid']
            timestamps = npz_data['timestamp']
            bsr_matrices = npz_data['bsr_matrix']

            sorted_indices = np.argsort(frame_ids)
            frame_ids = frame_ids[sorted_indices]
            timestamps = timestamps[sorted_indices]
            bsr_matrices = bsr_matrices[sorted_indices]

            for j, bsr_matrix in enumerate(bsr_matrices):
                coo = bsr_matrix.tocoo()
                frame = np.zeros((bsr_matrix.shape[0], bsr_matrix.shape[1]), dtype=np.uint8)
                frame[coo.row, coo.col] = coo.data.astype(np.uint8)
                if j == 0:
                    key_frame = frame.copy()
                    image = key_frame
                else:
                    if frame_reconstruction:
                        key_frame_overlay = key_frame.copy()
                        key_frame_overlay[frame > 0] = frame[frame > 0]
                        image = key_frame_overlay
                    else:
                        image = frame.copy()

                img, render, corners, ids, recentIDs, available_colours = detect_markers_and_assign_colours(
                    image, recentIDs, available_colours, display_width, display_height, colour_coding, stag_libraries, n_cols, print_buffer)
                render = apply_overlay(img, render, corners, ids, recentIDs, input_resolution_factor,
                                       output_zoom_x, colour_coding)
                resized_render = cv2.resize(render, (display_width, display_height), interpolation=cv2.INTER_NEAREST)

                if display_recentID_bar:
                    text_bar = add_recentID_bar(recentIDs, resized_render)
                    resized_render = np.vstack((resized_render, text_bar))

                frame_to_write = pad_to_size(resized_render, display_width, display_height)
                out.write(frame_to_write)

            # Send progress update after processing each npz file
            queue.put((fname, i + 1, total_files))



    except Exception as e:
        print_buffer.append(f"skipped {fname} due to error: {e}")
    finally:
        if out:
            out.release()
        queue.put((fname, total_files, total_files)) 
        #in case a corrupt .npz file exists, the listener still wants to receive a current==total signal. otherwise it will wait forever.


def listener(queue, video_names):
    pbars = {}
    completed = set()
    position_map = {name: i for i, name in enumerate(video_names)}  # fixed lines

    while len(completed) < len(video_names):
        try:
            fname, current, total = queue.get(timeout=1)

            if fname not in pbars:
                pbars[fname] = tqdm(total=total, desc=fname, position=position_map[fname], leave=True)
            
            pbars[fname].n = current
            pbars[fname].refresh()

            if current == total:
                # Don't close here, just mark as completed
                completed.add(fname)

        except queue_module.Empty:
            continue

    # Close all bars at the end
    for bar in pbars.values():
        bar.close()


def add_recentID_bar(recentIDs, image):
    # Sort by marker ID
    recentIDs = sorted(recentIDs, key=lambda x: x[0])

    max_per_row = 8
    num_ids = len(recentIDs)
    num_rows = (num_ids + max_per_row - 1) // max_per_row  # ceil division

    box_height = 60
    box_margin = 10
    text_thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2

    img_width = image.shape[1]
    bar_height = 210
    bar = np.ones((bar_height, img_width, 3), dtype=np.uint8) * 255  # white background

    for idx, (marker_id, color) in enumerate(recentIDs):
        row = idx // max_per_row
        col = idx % max_per_row

        box_width = img_width // max_per_row
        x1 = col * box_width
        y1 = row * (box_height + box_margin)
        x2 = x1 + box_width
        y2 = y1 + box_height

        cv2.rectangle(bar, (x1, y1), (x2, y2), color, -1)

        text = str(marker_id)
        text_size, _ = cv2.getTextSize(text, font, font_scale, text_thickness)
        text_x = x1 + (box_width - text_size[0]) // 2
        text_y = y1 + (box_height + text_size[1]) // 2

        cv2.putText(bar, text, (text_x, text_y), font, font_scale, (255, 255, 255), text_thickness, cv2.LINE_AA)

    return bar

def launch_convert_gui():
    root = ttk.Window(themename="solar")
    app = STag_Convert_GUI(root)
    root.mainloop()
    return app.started

def run_main_processing(settings, print_buffer):
    stag_libraries = settings["stag_libraries"]
    filename_addon = settings["filename_addon"]
    frame_reconstruction = settings["frame_reconstruction"]
    n_cols = settings["n_cols"]
    display_recentID_bar = settings["display_recentID_bar"]
    
    args = runVideoTagDetection(colour_palette, stag_libraries, frame_reconstruction, filename_addon, n_cols, display_recentID_bar)
    video_names = [arg[0] for arg in args]

    manager = multiprocessing.Manager()  # explicitly multiprocessing.Manager()
    q = manager.Queue()

    args_with_queue = [(*arg, print_buffer, q) for arg in args]

    listener_thread = threading.Thread(target=listener, args=(q, video_names))
    listener_thread.daemon = True
    listener_thread.start()

    with multiprocessing.Pool(processes=min(len(args_with_queue), os.cpu_count())) as pool:
        pool.map(process_single_video, args_with_queue)

    listener_thread.join()



if __name__ == '__main__':
    print_buffer = multiprocessing.Manager().list()

    show_initial_info()
    if not launch_convert_gui():
        print("User closed the GUI without pressing Start. Exiting.")
        sys.exit(0)
    print('Processing Has Started')
    time.sleep(1)
    settings = load_settings()
    time.sleep(1)
    run_main_processing(settings, print_buffer)
    for line in print_buffer:
        print(line)
    print("Finished processing videos")

    

'''
 
    show_initial_info()
    if not launch_convert_gui():
        print("User closed the GUI without pressing Start. Exiting.")
        sys.exit(0)

    settings = load_settings()
    run_main_processing(settings)

'''