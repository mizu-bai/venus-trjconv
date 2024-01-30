# venus-trjconv

A VENUS96 trajectory converter

Author: mizu-bai

## Requirements

- Python 3.8 and above
- Numpy

## Features

`venus-trjconv` can convert VENUS96 trajectories to `gro`, `g96`, and `xyz` format, making it easier to visualize and analyze the trajectories calculated by VENUS96.

## Usage

```sh
$ python3 -m venus_trjconv -h
usage: venus_trjconv [-h] -f F [-s S] [-o O] [-r R]

Convert VENUS96 trajectory to other formats.

optional arguments:
  -h, --help  show this help message and exit
  -f F        Trajectory: VENUS96 output
  -s S        Structure: gro xyz
  -o O        Trajectory: gro g96 xyz
  -r R        Reorder file
```

## Example

In folder `example/`, there is a QCT trajectory of methane molecule.

- `ch4.dt5`: VENUS96 input file.
- `ch4.out`: VENUS96 output file, containing 5 trajectories.
- `template.gro`: Gro file, `venus_trjconv` will read the title, number of atoms, residue numbers, residue names, atom names, atom numbers and box size stored in it.
- `template.xyz`: XYZ file, `venus_trjconv` will read the title, number of atoms stored in it.
- `reorder.txt`: In VENUS96 output, the order of atoms is `H H H H C`, while it is supposed to be `C H H H H` in converted trajectories. Thus, a reorder file should be supplied. In the `reorder.txt` file, the first line is `5`, indicating that the 5th atom (`C`) in VENUS96 output should be the 1st atom in converted trajectories. If the order of atoms in the VENUS96 output is correct, the reorder file and `-r` option are not necessary.

Convert to `gro`

```bash
$ python3 -m venus_trjconv -f ch4.out -s template.gro -o gro/ch4_traj.gro -r reorder.txt
```

Convert to `g96`

```bash
$ python3 -m venus_trjconv -f ch4.out -o g96/ch4_traj.g96 -r reorder.txt
```

Convert to `xyz`

```bash
$ python3 -m venus_trjconv -f ch4.out -s template.xyz -o xyz/ch4_traj.xyz -r reorder.txt
```

## Reference

(1) Hase, W. L.; Duchovic, R. J.; Hu, X.; Komornicki, A.; Lim, K. F.; Lu, D.-H.; Peslherbe, G. H.; Swamy, K. N.; Vande Linde, S. R.; Varandas, A., Wang, H.; Wolf, R. J. VENUS96: A general chemical dynamics computer program, _Quantum Chemical Program Exchange (QCPE) Bulletin_, **1996**, _16_ (4), 671. https://www.depts.ttu.edu/chemistry/Venus/index.php

(2) Abraham, M. J.; Murtola, T.; Schulz, R.; Páll, S.; Smith, J. C.; Hess, B.; Lindahl, E. GROMACS: High Performance Molecular Simulations through Multi-Level Parallelism from Laptops to Supercomputers. _SoftwareX_ **2015**, _1–2_, 19–25. https://doi.org/10.1016/j.softx.2015.06.001.

(3) Scott, W. R. P.; Hünenberger, P. H.; Tironi, I. G.; Mark, A. E.; Billeter, S. R.; Fennen, J.; Torda, A. E.; Huber, T.; Krüger, P.; van Gunsteren, W. F. The GROMOS Biomolecular Simulation Program Package. _J. Phys. Chem. A_ **1999**, _103_ (19), 3596–3607. https://doi.org/10.1021/jp984217f.

## License

BSD-2-Clause license
