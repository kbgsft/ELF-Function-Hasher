# ELF Function Hasher for Linux
Smart ELF binary function hash tool for checking code changes (ELF Binary diffing)

# Install
Download the Python code using git clone or wget in this git repository

# Supported OS
It can only run on Linux. And objdump, grep, awk binary are required

# How to use
- Get hashs and function size for all functions in ELF binary<br>
$ ./elf_func_hash.py {elf binary}

- Get assembly code for function name you want (it will be filtered for smart comparison)<br>
$ ./elf_func_hash.py {elf binary} {function name}

# Relase history
- 2024-06-09 : v1.2<br>
  : Hash algorithm change (sha256 -> md5)<br>
  : get_functions() has been changed to improve speed<br>
  <br>
- 2024-06-08 : v1.0
  first dist
