from dataclasses import dataclass
from typing import List

import numpy as np

ANCHOR_NUM_ATOMS = "NUMBER OF ATOMS"
ANCHOR_MASSES = "MASSES OF ATOMS"
ANCHOR_TRAJ = "TRAJECTORY NUMBER"
ANCHOR_CYCLE = "THE CYCLE COUNT IS"


@dataclass
class VENUSMol:
    num_atoms: int
    time: float  # ps
    position: np.array  # in nm
    velocity: np.array  # in nm/ps


def extract_venus_traj(
    venus_out: str,
    verbose: bool = False,
) -> List[List[VENUSMol]]:
    """Parse VENUS96 output.

    Arguments:
        venus_out (str): Path to VENUS96 output.
        verbose (bool): Whether to show verbose output.
            Defaults to False.

    Returns:
        traj_list (List[List[VENUSMol]]): List of trajectories.
    """

    contents = open(venus_out, "r").readlines()
    num_lines = len(contents)
    cur_line_idx = 0
    cur_traj_idx = 0

    num_atoms = 0
    masses = []
    traj_list = []

    while cur_line_idx < num_lines:
        line = contents[cur_line_idx]

        # parse num_atoms
        if ANCHOR_NUM_ATOMS in line:
            num_atoms = int(line.split("=")[-1])

        # parse masses
        if ANCHOR_MASSES in line:
            cur_line_idx += 2
            line = contents[cur_line_idx]
            masses = np.array([float(x) for x in line.split()])

        # parse traj
        if ANCHOR_TRAJ in line:
            cur_traj_idx = int(line.split()[3])
            if cur_traj_idx > len(traj_list):
                if verbose:
                    print(f"Trajectory: {cur_traj_idx}")

                traj_list.append([])

        # parse current traj
        if ANCHOR_CYCLE in line:
            cur_cycle = int(line.split()[4])
            # integration stepsize in units of 10-14 sec
            # 1.0e-14 s -> 1.0e-02 ps
            cur_time = float(line.split()[6]) * 1.0e-02

            if verbose:
                print(f"Cycle: {cur_cycle} Time: {cur_time:.3f} ps")

            cur_line_idx += 4

            position = []
            velocity = []

            for i in range(num_atoms):
                cur_line_idx += 1
                line = contents[cur_line_idx]
                arr = line.split()

                # coordinates in units of Angstrom
                # 1.0 Angstrom -> 0.1 nm
                atom_pos = 0.1 * np.array([float(x) for x in arr[:3]])
                position.append(atom_pos)

                # momenta in units of amu * Angstrom / (1.0e-14 s)
                # 1.0 amu * Angstrom / (1.0e-14 s) -> 10.0 (g/mol) * (nm/ps)
                atom_p = np.array([float(x) for x in arr[3:]])
                atom_vel = 10.0 * atom_p / masses[i]
                velocity.append(atom_vel)

            position = np.array(position)
            velocity = np.array(velocity)

            # create VENUSMol
            venus_mol = VENUSMol(
                time=cur_time,
                num_atoms=num_atoms,
                position=position,
                velocity=velocity,
            )

            traj_list[-1].append(venus_mol)

        cur_line_idx += 1

    return traj_list


if __name__ == "__main__":
    import sys

    traj_list = extract_venus_traj(sys.argv[1])

    print(f"{len(traj_list) = }")
    print(f"{len(traj_list[0]) = }")
    print(traj_list[0][0])
