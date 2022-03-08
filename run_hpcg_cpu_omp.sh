
for ont in {1,2,4,8,16}; do
	#for n in {2,4,8,16,32,64,128}; do
		for i in {1..5}; do
			#np=$((${n}/${ppn}))
			#ont=$((128/${n}))
			bcmd="env OMP_NUM_THREADS=${ont} /opt/intel/oneapi/mkl/2022.0.2/benchmarks/hpcg/bin/xhpcg_avx2"
			cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench hpcg_cpu --tag $1x_dsocket_${ont}ont_p190 --dir \"../\" --cpu-power 1 --cpu-threshold 190"
			echo "running ${cmd}"
			eval $cmd
			echo "Done!"
		done
	#done
done
