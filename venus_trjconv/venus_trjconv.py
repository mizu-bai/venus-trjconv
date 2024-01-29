import argparse
import glob
import os
from copy import deepcopy

import numpy as np

from .libmol import (GroMol, XYZMol, extract_venus_traj,
                     g96_traj_from_venus_traj, gro_traj_from_venus_traj,
                     xyz_traj_from_venus_traj)


def _parse_args():
    # prepare argument parser
    parser = argparse.ArgumentParser(
        prog="venus_trjconv",
        description="Convert VENUS96 trajectory to other formats."
    )

    # options to specify input files
    parser.add_argument(
        "-f",
        type=str,
        help="Trajectory: VENUS96 output",
        required=True,
    )

    parser.add_argument(
        "-s",
        type=str,
        help="Structure: gro xyz",
        required=False,
    )

    # options to specify output files
    parser.add_argument(
        "-o",
        type=str,
        help="Trajectory: gro g96 xyz",
        required=False,
        default="traj.gro",
    )

    # other options (incompatible with gmx trjconv)
    parser.add_argument(
        "-r",
        type=str,
        help="Reorder file",
        required=False,
    )

    args = parser.parse_args()

    return args


def _check_args(args):
    # check args
    if ".gro" in args.o or ".xyz" in args.o:
        if not args.s:
            raise FileNotFoundError(
                "VENUS96 output only contains coordinates and momentum. "
                "To convert to gro or xyz format, specify a structure file "
                "via -s [structure] option."
            )

        if args.o.split(".")[-1] != args.s.split(".")[-1]:
            raise ValueError(
                f"Output format and structure file format do not match.\n"
                f"Output:    {args.o.split('.')[-1]}\n"
                f"Structure: {args.s.split('.')[-1]}"
            )

    # check VENUS96 output
    if not os.path.exists(args.f):
        raise FileNotFoundError(
            f"VENUS96 output {args.venus} does not exist."
        )

    # check structure file
    if args.s:
        if not os.path.exists(args.s):
            raise FileNotFoundError(
                f"Structure file {args.s} does not exist."
            )

    # check reorder file
    if args.r:
        if not os.path.exists(args.r):
            raise FileNotFoundError(
                f"Reorder file {args.r} does not exist."
            )


def _auto_backup(
    file: str,
) -> None:
    if not os.path.exists(file):
        return

    file_dir = os.path.dirname(file)
    file_name = os.path.basename(file)

    old_file_pattern = f"#{file_name}.*#"
    old_files = sorted(glob.glob(os.path.join(
        file_dir,
        old_file_pattern,
    )))

    num_old_files = len(old_files)

    new_backup_file_name = f"#{file_name}.{num_old_files + 1}#"
    new_backup_file = os.path.join(file_dir, new_backup_file_name)

    os.rename(file, new_backup_file)


def main():
    # parse args
    args = _parse_args()

    # check args
    _check_args(args)

    # structure
    if ".gro" in args.o:
        struct_mol = GroMol.from_file(args.s)
    elif ".xyz" in args.o:
        struct_mol = XYZMol.from_file(args.s)

    # reorder
    if args.r:
        # load reorder file
        reorder_map = np.loadtxt(args.r, dtype=np.int32) - 1

    # parse output
    venus_traj_list = extract_venus_traj(
        venus_out=args.f,
        verbose=True,
    )

    # convert traj
    for (venus_traj_idx, venus_traj) in enumerate(venus_traj_list):
        # check structure
        if ".gro" in args.o or ".xyz" in args.o:
            if struct_mol.num_atoms != venus_traj[0].num_atoms:
                raise ValueError(
                    "Numbers of atoms in VENUS96 output and structure "
                    "file do not match."
                )

        # reorder
        if args.r:
            for venus_mol in venus_traj:
                _position = deepcopy(venus_mol.position)
                _velocity = deepcopy(venus_mol.velocity)

                for (old_idx, new_idx) in enumerate(reorder_map):
                    venus_mol.position[old_idx] = _position[new_idx]
                    venus_mol.velocity[old_idx] = _velocity[new_idx]

        # convert
        if ".gro" in args.o:
            out_traj = gro_traj_from_venus_traj(
                venus_traj=venus_traj,
                struct_mol=struct_mol,
            )
        elif ".g96" in args.o:
            out_traj = g96_traj_from_venus_traj(
                venus_traj=venus_traj,
            )
        elif ".xyz" in args.o:
            out_traj = xyz_traj_from_venus_traj(
                venus_traj=venus_traj,
                struct_mol=struct_mol,
            )

        suffix = args.o.split(".")[-1]
        out_traj_file = args.o.replace(
            f".{suffix}",
            f"_{venus_traj_idx + 1}.{suffix}",
        )

        _auto_backup(out_traj_file)

        with open(out_traj_file, "w") as f:
            for frame in out_traj:
                f.writelines(f"{str(frame)}\n")


if __name__ == "__main__":
    main()
