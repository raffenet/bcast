#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
import shutil
from pathlib import Path
def check_destination_exists(src_path, dest_path):
    """Check if source basename already exists in destination directory and prompt for overwrite if needed."""
    src_basename = os.path.basename(os.path.normpath(src_path))
    target_path = os.path.join(dest_path, src_basename)
    if os.path.exists(target_path):
        print(
            f"Warning: '{src_basename}' already exists in destination directory '{dest_path}'."
        )
        response = input("Do you want to overwrite? [y/N]: ").strip().lower()
        if response not in ["y", "yes"]:
            print("Operation cancelled.")
            sys.exit(0)
        return True
    return False
def check_source_exists(src_path):
    """Check if source file/directory exists."""
    if not os.path.exists(src_path):
        print(f"Error: Source '{src_path}' does not exist.")
        sys.exit(1)
def find_mpi_executable():
    """Find MPI executable in user PATH."""
    mpi_commands = ["mpiexec", "mpirun"]
    for cmd in mpi_commands:
        if shutil.which(cmd):
            return cmd
    return None
def find_bcast_executable():
    """Find bcast executable in user PATH."""
    return shutil.which("bcast")
def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="MPI Broadcast File Distribution Tool - Python Frontend",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/source/file
  %(prog)s /path/to/source/file /destination/path
  %(prog)s /path/to/directory /shared/storage
  %(prog)s --force /path/to/large/dataset /shared/storage
        """,
    )
    parser.add_argument("source", help="Source file or directory to broadcast")
    parser.add_argument(
        "destination",
        nargs="?",
        default="/tmp",
        help="Destination directory (default: /tmp)",
    )
    # Removed -n argument - tool uses fixed ppn 1 configuration
    parser.add_argument(
        "--mpiexec", help="Path to mpiexec executable (auto-detected if not specified)"
    )
    parser.add_argument(
        "--bcast", help="Path to bcast executable (auto-detected if not specified)"
    )
    parser.add_argument(
        "--force", action="store_true", help="Skip overwrite confirmation"
    )
    return parser.parse_args()
def main():
    args = parse_arguments()
    # Validate arguments
    source_path = os.path.abspath(args.source)
    dest_path = os.path.abspath(args.destination)
    check_source_exists(source_path)
    if not args.force:
        check_destination_exists(source_path, dest_path)
    # Find executables
    mpi_exec = args.mpiexec or find_mpi_executable()
    if not mpi_exec:
        print("Error: Could not find mpiexec/mpirun. Please specify with --mpiexec")
        sys.exit(1)
    bcast_exec = args.bcast or find_bcast_executable()
    if not bcast_exec:
        print(
            "Error: Could not find bcast executable. Please build it first or specify with --bcast"
        )
        sys.exit(1)
    # Build MPI command using ppn syntax only (1 process per node)
    mpi_cmd = [
        mpi_exec,
        "-ppn",
        "1",
        bcast_exec,
        source_path,
        dest_path,
    ]
    print(f"Broadcasting {source_path} to {dest_path} using 1 process per node...")
    print(f"Command: {' '.join(mpi_cmd)}")
    print()
    # Execute MPI command
    try:
        result = subprocess.run(mpi_cmd, check=True)
        print("Broadcast completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: MPI command failed with exit code {e.returncode}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Command not found: {mpi_cmd[0]}")
        sys.exit(1)
if __name__ == "__main__":
    main()
