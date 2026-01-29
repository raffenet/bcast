project('bcast', 'c',
  version : '1.0.0',
  default_options : ['warning_level=2',
                      'optimization=2',
                      'c_std=c99'])

# Get MPI path from option
mpi_path = get_option('with_mpi')

# Try to find MPI automatically or use user-provided path
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
    # Try common MPI locations
    common_paths = [
      '/usr/local',
      '/usr',
      '/opt/homebrew/',
    ]
    
    found_mpi = false
    foreach path : common_paths
      mpi_header = path + '/include/mpi.h'
      mpi_lib_so = path + '/lib/libmpi.so'
      mpi_lib_dylib = path + '/lib/libmpi.dylib'
      
      if run_command('test', '-f', mpi_header, check : false).returncode() == 0 and \
         (run_command('test', '-f', mpi_lib_so, check : false).returncode() == 0 or \
          run_command('test', '-f', mpi_lib_dylib, check : false).returncode() == 0)
        message('Found MPI at: ' + path)
        mpi_dep = declare_dependency(
          include_directories : include_directories(path + '/include'),
          link_args : ['-L' + path + '/lib', '-lmpi']
        )
        found_mpi = true
        break
      endif
    endforeach
    
    if not found_mpi
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