# This program creates the sbatch file needed to run each job.
#
# Input parameters
#   dirname     (type: string)  --> The directory path you would like to save the file
#   jobName     (type: string)  --> The name of the job that will show up on the queue
#   queue       (type: string)  --> The queue you wish to submit to (serial, CLUSTER, or debug)
#   inputFile   (type: string)  --> The name of the input file for the Molpro job
#
import os

#base_dir = '/home/sjlee/projects/wccr10'
base_dir = '/home/sjlee/projects/wccr10/test'
queue_cluster = 'CLUSTER,debug'
batch_mem = 59000

def main(file_path,file_name,job_name,queue,num_cpus,mem,input_file,trunc_space=False):
    with open(os.path.join(file_path,file_name),'w') as file1:
        file1.write('#!/bin/bash\n')
        file1.write('#\n')
        file1.write('#SBATCH --job-name={}\n'.format(job_name))
        file1.write('#SBATCH --output=job-%J.out\n')
        file1.write('#SBATCH --error=job-%J.err\n')
        file1.write('#SBATCH --partition={}\n'.format(queue))
        file1.write('#SBATCH --nodes=1\n')
        file1.write('#SBATCH --ntasks-per-node={}\n'.format(num_cpus))
        file1.write('#SBATCH --mem={}\n'.format(mem))
        file1.write('#SBATCH -t 24:00:00\n')
        file1.write('\n')
        file1.write('# Write out some information on the job\n')
        file1.write('echo "Starting at `date`"\n')
        file1.write('echo "Running on hosts: $SLURM_NODELIST"\n')
        file1.write('echo "Running on $SLURM_NNODES nodes."\n')
        file1.write('echo "Running on $SLURM_NPROCS processors."\n')
        file1.write('echo "Current working directory is `pwd`"\n')
        file1.write('\n')
        file1.write('# Load intel compilers since they were used to compile Molpro\n')
        file1.write('module purge\n')
        file1.write('module load compiler/gcc/7.2.0\n')
        file1.write('module load mpi/openmpi/3.1.2/gcc-7.2.0\n')
        file1.write('module unload compiler/intel/intel-18\n')
        file1.write('module load globalarrays/5.7.0_openmpi-3.1.2-gcc72\n')
        file1.write('module load Eigen/3.3.5\n')
        file1.write('\n')
        file1.write('# Run molpro script\n')
        file1.write('rm -r //scratch/$SLURM_JOBID\n')
        file1.write('mkdir //scratch/$SLURM_JOBID\n')
        if trunc_space:
            file1.write('cp ./trunc_space.txt //scratch/$SLURM_JOBID\n')
        file1.write('/home/sjlee/molproTinker/gradients/bin/molpro -n $SLURM_NPROCS {} -d //scratch/$SLURM_JOBID\n'.format(input_file))
        file1.write('rm -r //scratch/$SLURM_JOBID\n')

        #input_f = input1 % (job_name, queue, num_cpus, mem, input_file)
        #file1.write(input_f)
