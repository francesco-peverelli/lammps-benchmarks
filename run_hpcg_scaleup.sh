
for ppn in {1,2}; do
	for n in {1..1}; do
		for i in {16,32,64,128,256,512,1024,2048}; do
			np=$((${n}/${ppn}))
			ont=$((128/${n}))
			rpl_str="3s/.*/${i} ${i} ${i}/"
			rpl="sed -i '$rpl_str' ../hpcg.dat"
			eval $rpl
			eval "cat ../hpcg.dat"
			bcmd="mpiexec.hydra -n ${np} -ppn ${ppn} env OMP_NUM_THREADS=${ont} KMP_AFFINITY=granularity=fine,compact,1,0 /opt/intel/oneapi/mkl/2022.0.2/benchmarks/hpcg/bin/xhpcg_avx2"
			cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench hpcg_cpu --tag ${i}x_${np}n_${ppn}ppn_${ont}ont_p220 --dir \"../\" --cpu-power 1 --cpu-threshold 220"
			echo "running ${cmd}"
			eval $cmd
			echo "Done!"
		done
	done
done
