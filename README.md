# bcast - MPI Broadcast File Distribution Tool

A high-performance parallel file distribution tool for HPC clusters using MPI broadcast operations.

## Description

bcast efficiently distributes files and directories across MPI ranks by using MPI broadcast operations. The tool creates a tar archive of the source data on rank 0, broadcasts it in chunks to all ranks, and extracts it locally on each node.

## Features

- Efficient parallel file distribution using MPI broadcast
- Supports files and directories
- Built-in performance monitoring and reporting
- Optimized for HPC cluster environments
- Uses configurable 1GB buffer chunks for optimal performance

## Requirements

- MPI implementation (MPICH, Open MPI, Intel MPI, etc.)
- MPI compiler wrapper (mpicc)
- tar command
- Python 3.6+ (for Python frontend)
- POSIX-compliant system

## Installation

### From Source (Meson)

```bash
# Automatic MPI detection (searches build user's environment)
meson setup builddir
ninja -C builddir
ninja -C builddir install

# Or specify MPI installation path
meson setup builddir -Dwith_mpi=/path/to/mpi/install
ninja -C builddir
ninja -C builddir install
```



### Cross-compilation for HPC Systems

For distribution to different HPC systems, use the standard Meson workflow:

```bash
# Create distribution tarball
ninja -C builddir dist
```

This will create `bcast-1.0.0.tar.gz` which can be transferred and built on target systems.

### MPI Configuration

The build system automatically detects MPI installations in common locations:
- `/usr/local`, `/usr`
- `/opt/homebrew`

To use a custom MPI installation, specify the path with:
```bash
meson setup builddir -Dwith_mpi=/path/to/mpi/install
```

## Usage

### Python Frontend (Recommended)

```bash
# Basic usage - broadcast file to /tmp on all nodes
./bcast.py /path/to/source/file

# Broadcast to specific destination directory
./bcast.py /path/to/source/file /path/to/destination

# Broadcast file or directory
./bcast.py /path/to/directory /shared/storage

# Force overwrite without prompting
./bcast.py --force /path/to/large/dataset /shared/storage

# Force overwrite without prompting
./bcast.py --force /path/to/source/file /path/to/destination

# Specify custom MPI or bcast executables
./bcast.py --mpiexec /custom/path/to/mpiexec --bcast /custom/path/to/bcast /path/to/source
```

The Python frontend provides:
- **Argument validation** - Checks if source exists
- **Overwrite protection** - Prompts before overwriting existing destinations
- **Automatic executable detection** - Finds MPI and bcast executables
- **Cleaner interface** - Handles MPI details internally
- **Designed for 1 process per node** - Optimal performance for HPC cluster topology

### Direct MPI Usage

```bash
# Basic usage - broadcast file to /tmp on all nodes
mpiexec -ppn 1 ./bcast /path/to/source/file

# Broadcast to specific destination directory
mpiexec -ppn 1 ./bcast /path/to/source/file /path/to/destination

# Broadcast directory
mpiexec -ppn 1 ./bcast /path/to/directory /shared/storage
```

## Performance

The tool reports transfer statistics including:
- Total data transferred (GiB)
- Maximum time across all ranks
- Transfer rate (GiB/s)

## License

[Add your license information here]

## Author

[Add author information here]
