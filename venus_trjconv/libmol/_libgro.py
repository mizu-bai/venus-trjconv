from dataclasses import dataclass
from typing import List

import numpy as np

from ._libvenus import VENUSMol


@dataclass
class GroMol:
    title: str
    num_atoms: int
    resi_num: List[int]
    resi_name: List[str]
    atom_name: List[str]
    atom_num: List[int]
    position: np.ndarray  # nm
    velocity: np.ndarray  # nm/ps
    box_vectors: np.ndarray = np.zeros(3)

    def __str__(self) -> str:
        contents = []
        contents.append(f"{self.title}")
        contents.append(f"{self.num_atoms}")

        for i in range(self.num_atoms):
            contents.append(
                f"{self.resi_num[i]:5d}"
                f"{self.resi_name[i]:5s}"
                f"{self.atom_name[i]:5s}"
                f"{self.atom_num[i]:5d}"
                f"{self.position[i][0]:8.3f}"
                f"{self.position[i][1]:8.3f}"
                f"{self.position[i][2]:8.3f}"
                f"{self.velocity[i][0]:8.4f}"
                f"{self.velocity[i][1]:8.4f}"
                f"{self.velocity[i][2]:8.4f}"
            )

        contents.append(
            f"{self.box_vectors[0]:10.6f}"
            f"{self.box_vectors[1]:10.6f}"
            f"{self.box_vectors[2]:10.6f}"
        )

        return "\n".join(contents)

    @staticmethod
    def from_file(
        gro_file: str,
    ) -> "GroMol":
        contents = open(gro_file, "r").readlines()
        contents = [line.rstrip() for line in contents]

        title = contents.pop(0)
        num_atoms = int(contents.pop(0))

        resi_num = []
        resi_name = []
        atom_name = []
        atom_num = []
        position = []
        velocity = []

        for i in range(num_atoms):
            line = contents.pop(0)

            # residue number
            resi_num.append(int(line[0:5]))

            # residue name
            resi_name.append(line[5:10].rstrip())

            # atom name
            atom_name.append(line[10:15].rstrip())

            # atom number
            atom_num.append(int(line[15:20]))

            # position
            atom_pos = [float(x) for x in line[21:45].split()]
            position.append(atom_pos)

            # velocity
            if len(line) > 45:
                atom_vel = [float(x) for x in line[45:69]]
                velocity.append(atom_vel)
            else:
                velocity.append([0.0, 0.0, 0.0])

        position = np.array(position)
        velocity = np.array(velocity)

        box_vectors = np.array([float(x) for x in contents.pop(0).split()])

        gro_mol = GroMol(
            title=title,
            num_atoms=num_atoms,
            resi_num=resi_num,
            resi_name=resi_name,
            atom_name=atom_name,
            atom_num=atom_num,
            position=position,
            velocity=velocity,
            box_vectors=box_vectors,
        )

        return gro_mol


def gro_traj_from_venus_traj(
    venus_traj: List[VENUSMol],
    struct_mol: GroMol,
) -> List[GroMol]:
    traj = []

    for venus_mol in venus_traj:
        mol = GroMol(
            title=f"{struct_mol.title}, t= {venus_mol.time:.4f} ps",
            num_atoms=struct_mol.num_atoms,
            resi_num=struct_mol.resi_num,
            resi_name=struct_mol.resi_name,
            atom_name=struct_mol.atom_name,
            atom_num=struct_mol.atom_num,
            position=venus_mol.position,
            velocity=venus_mol.velocity,
        )

        traj.append(mol)

    return traj


if __name__ == "__main__":
    import sys

    gro_mol = GroMol.from_file(sys.argv[1])
    print(gro_mol)
