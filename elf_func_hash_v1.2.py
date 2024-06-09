#!/usr/bin/python
'''
Title  : ELF Function Hasher for Linux v1.2 (24.06.09)
desc   : Smart ELF binary function hash tool for checking code changes (ELF Binary diffing)
author : xcuter
source : https://github.com/kbgsft/ELF-Function-Hasher
blog   : https://blog.naver.com/xcuter
'''
import subprocess
import hashlib
import sys
import os
import re
import io

DEBUG = False

try:
    import __builtin__
except ImportError:
    import builtins as __builtin__

def printd(*args, **kwargs):
    if DEBUG == True:
        return __builtin__.print(*args, **kwargs)

def get_functions(binary):
    cmd = "objdump -t %s | grep 'F .text' | awk '{print $5,$6}'" % binary
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    res = result.stdout.decode()
    res = io.StringIO(res)

    functions = []
    for line in res:
        line = line.replace('\n', '')
        l = line.split(' ')
        functions.append((l[0], l[1]))

    return functions

def get_filtered_asm(opcode):
    printd("before :", opcode)
    asm = ""
    if '#' in opcode:
        code = opcode.split("#")
        asm = code[0].strip()
    else:
        asm = opcode.strip()

    if len(asm) > 7: # if operand is exist
        if asm[7] != '%':
            pos = asm.find('<')
            if pos != -1:
                asm = asm[0:7] + asm[pos:]
            else:
                pos = asm.find('(')
                if pos != -1:
                   asm = asm[0:7] + asm[pos:]
        else:
            pos1 = asm.find(',0x')
            pos2 = asm.find('(')
            if pos1 != -1 and pos2 != -2:
                if pos1 < pos2:
                    asm = asm[0:pos1+1] + asm[pos2:]

    printd("after  :", asm)
    printd("")
    return asm

def get_function_bytes(binary, func_name, view_func):
    result = subprocess.run(['objdump', '-d', binary, '--section=.text'], capture_output=True, text=True)
    in_function = False
    func_asm = ""

    for line in result.stdout.splitlines():
        if line.strip().endswith(f'<{func_name}>:'):
            in_function = True
        elif in_function:
            if ':' in line:
                parts = line.split(':')
                address = parts[1].strip()
                if '\t' in address:
                    opcode = address.split('\t')
                    opcode = opcode[1].strip()
                    asm = get_filtered_asm(opcode)

                    if view_func != "" and func_name == view_func:
                        print(asm)

                    func_asm += asm
                if not address:
                    break
            else:
                break
    return func_asm.encode()


def hash_function(func_bytes):
    return hashlib.md5(func_bytes).hexdigest()


if __name__ == "__main__":

    print("============================================================")
    print("       ELF Function Hasher v1.2 for Linux (by xcuter)       ")
    print("============================================================\n")

    binary_path = ""
    view_func = ""
    
    if len(sys.argv) == 1:
        print("%s <binary> <function to view(option)>" % sys.argv[0])
        sys.exit()
    
    if len(sys.argv) >= 2:
        binary_path = sys.argv[1]
        if os.path.isfile(binary_path) == False:
            print("[-] '%s' is not exist" % binary_path)
            sys.exit()
    
    if len(sys.argv) == 3:
        view_func = sys.argv[2]
    
    functions = get_functions(binary_path)

    print("hash                            	size		function name")
    print("-------------------------------------------------------------------------")
    for size, name in functions:
        size = int(size, 16)
        if view_func != "":
            if view_func == name:
                func_bytes = get_function_bytes(binary_path, name, view_func)
                if func_bytes:
                    func_hash = hash_function(func_bytes)
                    print(f"{func_hash}\t{size}\t\t{name}")
    
        else:
            func_bytes = get_function_bytes(binary_path, name, view_func)
            if func_bytes:
                func_hash = hash_function(func_bytes)
                print(f"{func_hash}\t{size}\t\t{name}")
    
    print("\n[+] All Done.")
