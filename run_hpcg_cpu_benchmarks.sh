
for ont in {1,2}; do
	#for n in {2,4,8,16,32,64,128}; do
		for i in {1..10}; do
			#np=$((${n}/${ppn}))
			#ont=$((128/${n}))
			n=64
			bcmd="mpiexec.hydra -n ${n} env OMP_NUM_THREADS=${ont} KMP_AFFINITY=granularity=fine,compact,1,0 /opt/intel/oneapi/mkl/2022.0.2/benchmarks/hpcg/bin/xhpcg_avx2"
			cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench hpcg_cpu --tag $1x_${n}n_1ppn_${ont}ont_p210 --dir \"../\" --cpu-power 1 --cpu-threshold 210"
			echo "running ${cmd}"
			eval $cmd
			echo "Done!"
		done
	#done
done
