
for ont in {32,64}; do
		for i in {1..10}; do
			#np=$((${n}/${ppn}))
			#ont=$((128/${n}))
			bcmd="env OMP_NUM_THREADS=${ont} /opt/intel/oneapi/mkl/2022.0.2/benchmarks/hpcg/bin/xhpcg_avx2"
			cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench hpcg_cpu --tag $1x_ssocket_${ont}ont_p210 --dir \"../\" --cpu-power 1 --cpu-threshold 210"
			echo "running ${cmd}"
			eval $cmd
			echo "Done!"
		done
	#done
done
