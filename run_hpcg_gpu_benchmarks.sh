
for g in {1,2,4,6,8}; do
	ont=$((104/${g}))
	bcmd="mpirun -np $g env OMP_NUM_THREADS=${ont} ./xhpcg-3.1_gcc_485_cuda-10.0.130_ompi-3.1.0_sm_35_sm_50_sm_60_sm_70_sm_75_ver_10_9_18"
	cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench hpcg_gpu --tag bm_${g}g_$1x_60s_${ont}ont_gw$2 --dir \"../\" --arch BM.GPU3.8 --gpu-power $g --cpu-power 1 --gpu-threshold $2" 
	echo "running ${cmd}"
	eval $cmd
	echo "Done!"
done
