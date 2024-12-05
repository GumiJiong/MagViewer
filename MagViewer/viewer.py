import sys

import MagViewer as mv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider


def visualize(mag, pos, volume, ori_mag=None):
    # 3d plot mags
    fig = plt.figure(figsize=(10, 10))
    global ax
    ax = fig.add_subplot(111, projection="3d")
    fig.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.2)

    cm = plt.get_cmap("coolwarm")
    ax.scatter(
        pos[:, 0],
        pos[:, 1],
        pos[:, 2],
        s=volume * 8000 / len(pos),
        c=volume,
        alpha=0.5,
        cmap=cm,
    )

    global mms, selected_ion, frame, ion, scale_factor
    frame, ion = 0, 0
    scale_factor = 0.1
    ax.set_title(
        f"Voronoi Volume: {volume[0]:.2f}, Magmom: {mag[frame][:, 0]} / {np.linalg.norm(mag[frame][:, 0]):.2f}"
    )

    if ori_mag is not None:
        ax.quiver(
            pos[:, 0],
            pos[:, 1],
            pos[:, 2],
            ori_mag[0] * scale_factor,
            ori_mag[1] * scale_factor,
            ori_mag[2] * scale_factor,
            color="k",
        )
    mms = ax.quiver(
        pos[:, 0],
        pos[:, 1],
        pos[:, 2],
        mag[0][0] * scale_factor,
        mag[0][1] * scale_factor,
        mag[0][2] * scale_factor,
        color="r",
    )
    ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.05])
    frame_slider = Slider(
        ax=ax2,
        label="image",
        valfmt="%d",
        valmin=0,
        valmax=len(mag) - 1,
        # valinit=1,
        dragging=True,
        valstep=1,
    )

    def frame_update(val):
        global mms, frame
        frame = frame_slider.val
        ax.set_title(
            f"Voronoi Volume: {volume[ion]:.2f}, Magmom: {mag[frame][:, ion]} / {np.linalg.norm(mag[frame][:, ion]):.2f}"
        )
        mms.remove()
        mms = ax.quiver(
            pos[:, 0],
            pos[:, 1],
            pos[:, 2],
            mag[frame][0] * scale_factor,
            mag[frame][1] * scale_factor,
            mag[frame][2] * scale_factor,
            color="r",
        )
        fig.canvas.draw_idle()

    frame_slider.on_changed(frame_update)

    selected_ion = ax.scatter(
        pos[0, 0], pos[0, 1], pos[0, 2], s=100, c="black", alpha=1
    )
    ax3 = fig.add_axes([0.95, 0.2, 0.05, 0.7])
    ion_slider = Slider(
        ax=ax3,
        label="ion",
        valfmt="%d",
        valmin=0,
        valmax=len(pos) - 1,
        # valinit=1,
        dragging=True,
        valstep=1,
        orientation="vertical",
    )

    def ion_update(val):
        global selected_ion, ion
        ion = ion_slider.val
        ax.set_title(
            f"Voronoi Volume: {volume[ion]:.2f}, Magmom: {mag[frame][:, ion]} / {np.linalg.norm(mag[frame][:, ion]):.2f}"
        )
        selected_ion.remove()
        selected_ion = ax.scatter(
            pos[ion, 0], pos[ion, 1], pos[ion, 2], s=100, c="black"
        )
        fig.canvas.draw_idle()

    ion_slider.on_changed(ion_update)

    plt.show()


def view_opt():
    if len(sys.argv) == 3:
        print("Ensure the two OUTCAR files share the same geometry.")
        ori_mag = mv.vasp_magmom_parser(sys.argv[2] + "/")["magmom"][-1]
    else:
        ori_mag = None

    outcar = mv.vasp_magmom_parser(sys.argv[1] + "/")

    v_volume = mv.voronoi_volume(outcar["scal_pos"]) * outcar["cell_volume"]
    visualize(outcar["magmom"], outcar["scal_pos"], v_volume, ori_mag)


def view_Ecurve(npoints=6):
    if len(sys.argv) == 4:
        npoints = int(sys.argv[3])

    ori_outcar = mv.vasp_magmom_parser(sys.argv[2] + "/")
    v_volume = mv.voronoi_volume(ori_outcar["scal_pos"]) * ori_outcar["cell_volume"]
    ori_mag = ori_outcar["magmom"][-1]

    base_path = sys.argv[1] + "/"
    mags = np.zeros((npoints, 3, len(ori_outcar["scal_pos"])))

    for i in range(len(ori_outcar["scal_pos"])):
        for j in range(npoints):
            path = f"{base_path}{i}/{j}/"
            outcar = mv.vasp_magmom_parser(path)
            mags[j, :, i] = outcar["magmom"][-1][:, i]
    visualize(mags, ori_outcar["scal_pos"], v_volume, ori_mag)


if __name__ == "__main__":
    view_opt()
