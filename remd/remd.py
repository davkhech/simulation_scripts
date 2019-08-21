import os
import argparse
import numpy as np
import subprocess


def parse_args(*argument_array):
    parser = argparse.ArgumentParser()
    parser.add_argument('lowest', type=float)
    parser.add_argument('highest', type=float)
    parser.add_argument('replicas', default=1, type=int)
    return parser.parse_args(*argument_array)


def prepare_directory(nvt, npt, md, temp, ind):
    dir_name = 'prepare_{}'.format(ind)
    ret = subprocess.run(['mkdir', dir_name])
    if ret.returncode == 1:
        subprocess.run(['rm', '-rf', dir_name])
        subprocess.run(['mkdir', dir_name])
    with open('{}/nvt.mdp'.format(dir_name), 'w') as wf:
        wf.write(nvt.format(temp, temp, temp, temp))
    with open('{}/npt.mdp'.format(dir_name), 'w') as wf:
        wf.write(npt.format(temp, temp, temp))
    with open('{}/md.mdp'.format(dir_name), 'w') as wf:
        wf.write(md.format(temp, temp, temp))
    return dir_name


def equilibrate(dir_name, ind):
    print(dir_name)
    cmd = 'gmx_mpi grompp -f {0}/nvt.mdp -c system.gro -r system.gro -p topol.top -o {0}/nvt.tpr -n index.ndx'.format(dir_name)
    subprocess.run(cmd.split(' '))
    print('-' * 80)
    print('nvt', dir_name)
    print('-' * 80)
    cmd = 'gmx_mpi mdrun -v -deffnm {}/nvt'.format(dir_name)
    subprocess.run(cmd.split(' '))

    cmd = 'gmx_mpi grompp -f {0}/npt.mdp -c {0}/nvt.gro -r {0}/nvt.gro -t {0}/nvt.cpt -p topol.top -o {0}/npt.tpr -n index.ndx'.format(dir_name)
    subprocess.run(cmd.split(' '))
    print('-' * 80)
    print('npt', dir_name)
    print('-' * 80)
    cmd = 'gmx_mpi mdrun -v -deffnm {}/npt'.format(dir_name)
    subprocess.run(cmd.split(' '))

    cmd = 'gmx_mpi grompp -f {0}/md.mdp -c {0}/npt.gro -t {0}/npt.trr -p topol.top -o md_remd_{1}.tpr -n index.ndx'.format(dir_name, ind)
    subprocess.run(cmd.split(' '))
    print('-' * 80)
    print('md tpr file is ready', dir_name)
    print('-' * 80)


def prepare_remd_directory(ind):
    dir_name = 'replica_{}'.format(ind)
    ret = subprocess.run(['mkdir', dir_name])
    if ret.returncode == 1:
        subprocess.run(['rm', '-rf', dir_name])
        subprocess.run(['mkdir', dir_name])
    cmd = 'cp md_remd_{0}.tpr replica_{0}/topol.tpr'.format(ind)
    subprocess.run(cmd.split(' '))


def run_replica_exchange(replicas):
    cmd = 'mpirun -np 8 gmx_mpi mdrun -v -replex 10 -multidir ' + ' '.join(['replica_{}'.format(i) for i in range(replicas)])
    print(cmd)
    subprocess.run(cmd.split(' '))


def main(args):
    replicas = args.replicas
    temp_k = (np.log(args.highest) - np.log(args.lowest)) / (replicas - 1)
    with open('nvt.mdp') as f:
        nvt = f.read()
    with open('npt.mdp') as f:
        npt = f.read()
    with open('md.mdp') as f:
        md = f.read()
    temps = []
    for i in range(replicas):
        temp = args.lowest * np.exp(temp_k * i)
        temps.append(temp)
        dir_name = prepare_directory(nvt, npt, md, temp, i)
        print('Directory prepared for temperature', temp)
        equilibrate(dir_name, i)
        prepare_remd_directory(i)
    run_replica_exchange(replicas)


if __name__ == '__main__':
    main(parse_args())
