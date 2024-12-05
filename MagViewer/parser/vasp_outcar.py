import numpy as np


def vasp_magmom_parser(path):
    with open(path + "OUTCAR", "r") as f:
        lines = f.readlines()
        x_lines, y_lines, z_lines = [], [], []
        for n, line in enumerate(lines):
            if "NIONS" in line:
                nions = int(line.split()[11])
            if "magnetization (x)" in line:
                x_lines.append(n)
            if "magnetization (y)" in line:
                y_lines.append(n)
            if "magnetization (z)" in line:
                z_lines.append(n)
            if "TOTAL-FORCE" in line:
                pos_line = n
            if "(direct lattice)" in line:
                scal_pos_line = n
            if "volume of cell" in line:
                cell_volume = float(line.split()[-1])

        mag, scal_pos, pos, force = [], [], [], []
        for n in range(len(x_lines)):
            mag_x, mag_y, mag_z = np.zeros(nions), np.zeros(nions), np.zeros(nions)
            for i in range(nions):
                mag_x[i] = float(lines[x_lines[n] + 4 + i].split()[4])
                mag_y[i] = float(lines[y_lines[n] + 4 + i].split()[4])
                mag_z[i] = float(lines[z_lines[n] + 4 + i].split()[4])
            mag.append([mag_x, mag_y, mag_z])

        for i in range(nions):
            scal_pos.append(
                [
                    float(lines[scal_pos_line + 1 + i].split()[0]),
                    float(lines[scal_pos_line + 1 + i].split()[1]),
                    float(lines[scal_pos_line + 1 + i].split()[2]),
                ]
            )
            pos.append(
                [
                    float(lines[pos_line + 2 + i].split()[0]),
                    float(lines[pos_line + 2 + i].split()[1]),
                    float(lines[pos_line + 2 + i].split()[2]),
                ]
            )
            force.append(
                [
                    float(lines[pos_line + 2 + i].split()[3]),
                    float(lines[pos_line + 2 + i].split()[4]),
                    float(lines[pos_line + 2 + i].split()[5]),
                ]
            )

    mag, scal_pos, pos, force = np.array(mag), np.array(scal_pos), np.array(pos), np.array(force)

    outcar = {
        "magmom": mag,
        "cell_volume": cell_volume,
        "scal_pos": scal_pos,
        "positions": pos,
        "forces": force,
    }

    return outcar
