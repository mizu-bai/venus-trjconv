from dataclasses import dataclass
from typing import List

import numpy as np

from ._libvenus import VENUSMol


@dataclass
class XYZMol:
    num_atoms: int
    title: str
    atom_name: List[str]
    xyz: np.array  # Angstrom

    def __str__(self) -> str:
        xyz_contents = []
        xyz_contents.append(f"{self.num_atoms}")
        xyz_contents.append(f"{self.title}")

        for i in range(self.num_atoms):
            xyz_contents.append(
                f"{self.atom_name[i]:4s}"
                f"{self.xyz[i][0]:13.8f}"
                f"{self.xyz[i][1]:13.8f}"
                f"{self.xyz[i][2]:13.8f}"
            )

        return "\n".join(xyz_contents)

    @staticmethod
    def from_file(
        xyz_file: str,
    ) -> 'XYZMol':
        contents = open(xyz_file, "r").readlines()
        contents = [line.rstrip() for line in contents]

        num_atoms = int(contents.pop(0))
        title = contents.pop(0)
        atom_name = []
        xyz = []

        for i in range(num_atoms):
            line = contents.pop(0)
            arr = line.split()
            atom_name.append(arr[0])
            atom_xyz = [float(x) for x in arr[1:4]]
            xyz.append(atom_xyz)

        xyz = np.array(xyz)

        xyz_mol = XYZMol(
            num_atoms=num_atoms,
            title=title,
            atom_name=atom_name,
            xyz=xyz,
        )

        return xyz_mol


def xyz_traj_from_venus_traj(
    venus_traj: List[VENUSMol],
    struct_mol: XYZMol,
) -> List[XYZMol]:
    traj = []

    for venus_mol in venus_traj:
        mol = XYZMol(
            num_atoms=struct_mol.num_atoms,
            title=f"{struct_mol.title}, t= {venus_mol.time:.4f} ps",
            atom_name=struct_mol.atom_name,
            xyz=venus_mol.position * 10.0,
        )

        traj.append(mol)

    return traj


if __name__ == "__main__":
    import sys

    xyz_mol = XYZMol.from_file(sys.argv[1])
    print(xyz_mol)
