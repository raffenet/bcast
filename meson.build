project('bcast', 'c')

# Get MPI path from option
mpi_path = get_option('with_mpi')

if mpi_path != ''
    # User provided a path, only check this specific location
    message('Using MPI from user-provided path: ' + mpi_path)

    # Verify MPI installation exists at the specified path
    mpi_header = mpi_path / 'include' / 'mpi.h'
    mpi_lib_so = mpi_path / 'lib' / 'libmpi.so'
    mpi_lib_dylib = mpi_path / 'lib' / 'libmpi.dylib'

    if run_command('test', '-f', mpi_header, check: false).returncode() != 0
        error('MPI header not found at: ' + mpi_header)
    endif

    if run_command('test', '-f', mpi_lib_so, check: false).returncode() != 0 and run_command(
        'test',
        '-f',
        mpi_lib_dylib,
        check: false,
    ).returncode() != 0
        error('MPI library not found in: ' + mpi_path / 'lib')
    endif

    mpi_dep = declare_dependency(
        include_directories: include_directories(mpi_path / 'include'),
        link_args: ['-L' + mpi_path / 'lib', '-lmpi'],
    )
else
    # Try to find MPI automatically using pkg-config/system or PATH
    mpi_dep = dependency('mpi', required: false, language: 'c')

    if not mpi_dep.found()
        # Try to find mpicc in PATH and use it for MPI detection
        mpicc = find_program('mpicc', required: false)
        if mpicc.found()
            message('Using MPI compiler found in PATH: ' + mpicc.full_path())
            # Get compiler flags from mpicc
            cpp_args = run_command(mpicc, '-showme:compile', check: true).stdout().strip()
            link_args = run_command(mpicc, '-showme:link', check: true).stdout().strip()

            mpi_dep = declare_dependency(
                compile_args: cpp_args.split(),
                link_args: link_args.split(),
            )
        else
            error('MPI not found. Please install MPI or use --with-mpi=<path>')
        endif
    else
        message('Using MPI found by pkg-config/system')
    endif
endif

# Check for tar availability
tar_prog = find_program('tar', required: true)
message('Using tar: ' + tar_prog.full_path())

# Executable
executable(
    'bcast',
    'bcast.c',
    dependencies: [mpi_dep],
    install: true,
)

# Install Python frontend
install_data(
    'bcast.py',
    install_dir: 'bin',
    install_mode: 'rwxr-xr-x',
)
