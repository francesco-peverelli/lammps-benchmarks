
for ont in {1,2}; do
	#for n in {64}; do
		for i in {1..5}; do
			#np=$((${n}/${ppn}))
			#ont=$((128/${n}))
			n=32
			bcmd="mpiexec.hydra -n ${n} env OMP_NUM_THREADS=${ont} KMP_AFFINITY=granularity=fine,compact,1,0 /opt/intel/oneapi/mkl/2022.0.2/benchmarks/hpcg/bin/xhpcg_avx2"
			cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench hpcg_cpu --tag $1x_${n}n_ssocket_${ont}ont_p110 --dir \"../\" --cpu-power 1 --cpu-threshold 110"
			echo "running ${cmd}"
			eval $cmd
			echo "Done!"
		done
	#done
done
