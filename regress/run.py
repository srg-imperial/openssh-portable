#!/usr/bin/python2

import argparse

import os
import os.path

from os import listdir, getcwd
from os.path import isfile, join, abspath
from sys import argv
from shutil import move

from subprocess import call

sshsDir = abspath(join(os.pardir,'install'))
sshs    = [f for f in listdir(sshsDir) if isfile(join(sshsDir, f, 'bin/ssh'))]

parser = argparse.ArgumentParser(description='Run OpenSSH tests')

parser.add_argument('-vxssh',
        action='store_true',
        help='Run clients with Varan')

parser.add_argument('-vxsshd',
        action='store_true',
        help='Run server with Varan')

parser.add_argument('ssh',
        choices=sshs,
        nargs='+',
        help='Compilations to use')

argLines = ' '.join(argv[1:]).split('--')

args = parser.parse_args(argLines[0].split())

if args.vxssh:
    logFileName = 'vx_ssh_' + '_'.join(args.ssh) + '.log'
elif args.vxsshd:
    logFileName = 'vx_sshd_' + '_'.join(args.ssh) + '.log'
else:
    logFileName = args.ssh[0] + '.log'


## if isfile(logFileName):
##     move(logFileName, logFileName + '.old')
## 
logFile = open(logFileName, 'w')

objdir   = abspath(os.pardir)
curdir   = getcwd()
builddir = abspath(os.pardir)
obj      = getcwd()
path     = builddir + ':$PATH'

vx    = '/home/lganchin/repos/varan/varan/bin/src/vx'
tools = [
        'scp',
        'ssh',
        'ssh-agent',
        'ssh-add',
        'ssh-keygen',
        'ssh-pkcs11-helper',
        'ssh-keyscan',
        'sftp',
        ]
servers = [
        ('sbin', 'sshd'),
        ('libexec', 'sftp-server'),
        ]
bins  = {}

if args.vxssh:
    for t in tools:
        bin = vx
        for ssh in args.ssh:
            bin = bin + ' ' + abspath(join(os.pardir, 'install', ssh, 'bin', t))
        bin = bin + ' -- '
        bins[t] = bin
else:
    for t in tools:
        bins[t] = abspath(join(os.pardir, 'install', args.ssh[0], 'bin', t))

if args.vxsshd:
    for s in servers:
        bin = vx
        for ssh in args.ssh:
            bin = bin + ' ' + abspath(join(os.pardir, 'install', ssh, s[0], s[1]))
        bin = bin + ' -- '
        bins[s[1]] = bin
else:
    for s in servers:
        bins[s[1]] = abspath(join(os.pardir, 'install', args.ssh[0], s[0], s[1]))

command = 'make \\'
command = command + '\n.OBJDIR="'  + objdir   + '" \\'
command = command + '\n.CURDIR="'  + curdir   + '" \\'
command = command + '\nBUILDDIR="' + builddir + '" \\'
command = command + '\nOBJ="'      + obj      + '" \\'
command = command + '\nPATH="'     + path     + '" \\'
command = command + '\nPATH="'     + path     + '" \\'

command = command + '\nTEST_SSH_SCP="'       + bins['scp']        + '" \\'
command = command + '\nTEST_SSH_SSH="'       + bins['ssh']        + '" \\'
command = command + '\nTEST_SSH_SSHAGENT="'  + bins['ssh-agent']  + '" \\'
command = command + '\nTEST_SSH_SSHADD="'    + bins['ssh-add']    + '" \\'
command = command + '\nTEST_SSH_SSHKEYGEN="' + bins['ssh-keygen'] + '" \\'
command = command + '\nTEST_SSH_SSHPKCS11HELPER="' + bins['ssh-pkcs11-helper'] + '" \\'
command = command + '\nTEST_SSH_SSHKEYSCAN="' + bins['ssh-keyscan'] + '" \\'
command = command + '\nTEST_SSH_SFTP="'       + bins['sftp']        + '" \\'

command = command + '\nTEST_SSH_SSHD="' + bins['sshd'] + '" \\'
command = command + '\nTEST_SSH_SFTPSERVER="' + bins['sftp-server'] + '" \\'

command = command + '\nTEST_SHELL="sh" \\'

command = command + '\nt-exec'

print(command)

## if len(argLines) > 1:
##     command = command + argLines[1]

## env = os.environ.copy()
## bbs = map((lambda bb: join(busyboxesDir, bb,'busybox')), args.bbs)
## 
## if args.vx:
##     env['VX']  = '1'
##     env['BBS'] = ' '.join(bbs)
## else:
##     env['VX']  = '0'
##     env['BBS'] = bbs[0]
## 
## if args.afl:
##     env['AFL']  = '5'
##     env['VX']  = '0'
##     env['BBS'] = bbs[0]
## else:
##     env['AFL']  = '0'
## 
## if args.afltest:
##     env['AFLTEST'] = '1'
## else:
##     env['AFLTEST'] = '0'
## 
## env['BB']  = bbs[0]
## 
call(command,
        stdout=logFile,
        stderr=logFile,
#        env=env,
        shell=True)
