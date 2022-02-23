
<<<<<<< HEAD
for ont in {32,64}; do
=======
for ont in {32,64,128}; do
	#for n in {2,4,8,16,32,64,128}; do
>>>>>>> 049e6950f869ecbfcbfb896e90e3c891622271fc
		for i in {1..10}; do
			#np=$((${n}/${ppn}))
			#ont=$((128/${n}))
			bcmd="env OMP_NUM_THREADS=${ont} /opt/intel/oneapi/mkl/2022.0.2/benchmarks/hpcg/bin/xhpcg_avx2"
<<<<<<< HEAD
			cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench hpcg_cpu --tag $1x_ssocket_${ont}ont_p210 --dir \"../\" --cpu-power 1 --cpu-threshold 210"
=======
			cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench hpcg_cpu --tag $1x_dsocket_${ont}ont_p210 --dir \"../\" --cpu-power 1 --cpu-threshold 210"
>>>>>>> 049e6950f869ecbfcbfb896e90e3c891622271fc
			echo "running ${cmd}"
			eval $cmd
			echo "Done!"
		done
	#done
done
