project('bcast', 'c',
  version : '1.0.0',
  default_options : ['warning_level=2',
                      'optimization=2',
                      'c_std=c99'])

# Get MPI path from option
mpi_path = get_option('with_mpi')

# Try to find MPI using pkg-config/system or user-provided path
mpi_dep = dependency('mpi', required : false, language : 'c')

if not mpi_dep.found()
  if mpi_path != ''
    # User provided a path, try to use it
    message('Using MPI from user-provided path: ' + mpi_path)
    mpi_dep = declare_dependency(
      include_directories : include_directories(mpi_path / 'include'),
      link_args : ['-L' + mpi_path / 'lib', '-lmpi']
    )
  else
    # Try to find mpicc in PATH and use it for MPI detection
    mpicc = find_program('mpicc', required : false)
    if mpicc.found()
      message('Using MPI compiler found in PATH: ' + mpicc.full_path())
      # Get compiler flags from mpicc
      cpp_args = run_command(mpicc, '-showme:compile', check : true).stdout().strip()
      link_args = run_command(mpicc, '-showme:link', check : true).stdout().strip()
      
      mpi_dep = declare_dependency(
        compile_args : cpp_args.split(),
        link_args : link_args.split()
      )
    else
      error('MPI not found. Please install MPI or use --with-mpi=<path>')
    endif
  endif
else
  message('Using MPI found by pkg-config/system')
endif

# Check for tar availability
tar_prog = find_program('tar', required : true)
message('Using tar: ' + tar_prog.full_path())

# Executable
executable('bcast',
  'bcast.c',
  dependencies : [mpi_dep],
  install : true,
  install_dir : get_option('bindir')
)

# Install Python frontend
install_data('bcast.py',
  install_dir : get_option('bindir'),
  install_mode : 'rwxr-xr-x'
)
