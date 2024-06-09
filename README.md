# ELF Function Hasher for Linux
Smart ELF binary function hash tool for checking code changes (ELF Binary diffing)

# Install
Download the Python code using git clone or wget in this git repository

# Supported OS
It can only run on Linux. And objdump, grep, awk binary are required

# How to use
- Get hashs and function size for all functions in ELF binary<br>
$ ./elf_func_hash.py {elf binary}<br>
![image](https://github.com/kbgsft/ELF-Function-Hasher/assets/17945347/50c89f16-ac0a-43f8-95e7-aaaab99bcb19)

- Get assembly code for function name you want (it will be filtered for smart comparison)<br>
$ ./elf_func_hash.py {elf binary} {function name}<br>
![image](https://github.com/kbgsft/ELF-Function-Hasher/assets/17945347/a8a487cd-cf81-48b2-9e3d-2962fd73c1c4)

- Using when comparison<br>
![image](https://github.com/kbgsft/ELF-Function-Hasher/assets/17945347/c7b4a79f-379e-4340-bb81-75c67423d002)


# Relase history
- 2024-06-09 : v1.2<br>
  : Hash algorithm change (sha256 -> md5)<br>
  : get_functions() has been changed to improve speed<br>
  <br>
- 2024-06-08 : v1.0
  first dist
