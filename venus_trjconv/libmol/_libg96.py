from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np

from ._libvenus import VENUSMol


@dataclass
class G96Mol:
    title: str
    timestep: Tuple[int, float]
    position: np.array  # nm
    velocity: np.array  # nm/ps
    box_vectors: np.array = field(default_factory=lambda: np.zeros(3))

    def __str__(self) -> str:
        contents = []

        # title
        contents.append("TITLE")
        contents.append(self.title)
        contents.append("END")

        # timestep
        contents.append("TIMESTEP")
        contents.append(f"{self.timestep[0]:15d}{self.timestep[1]:15.6f}")
        contents.append("END")

        # position
        contents.append("POSITIONRED")

        for pos in self.position:
            contents.append(f"{pos[0]:15.9f}{pos[1]:15.9f}{pos[2]:15.9f}")

        contents.append("END")

        # velocity
        contents.append("VELOCITYRED")

        for vel in self.velocity:
            contents.append(f"{vel[0]:15.9f}{vel[1]:15.9f}{vel[2]:15.9f}")

        contents.append("END")

        # box
        contents.append("BOX")
        contents.append(
            f"{self.box_vectors[0]:15.9f}"
            f"{self.box_vectors[1]:15.9f}"
            f"{self.box_vectors[2]:15.9f}"
        )
        contents.append("END")

        return "\n".join(contents)


def g96_traj_from_venus_traj(
    venus_traj: List[VENUSMol],
) -> List[G96Mol]:
    traj = []

    for (venus_frame_idx, venus_mol) in enumerate(venus_traj):
        mol = G96Mol(
            title="",
            timestep=[venus_frame_idx, venus_mol.time],
            position=venus_mol.position,
            velocity=venus_mol.velocity,
        )

        traj.append(mol)

    return traj
