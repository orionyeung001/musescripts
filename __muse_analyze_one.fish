function __muse_analyze_one -d 'runs single analysis for given file, assumes everything given good'

  set -x DYLD_LIBRARY_PATH "$ROOTSYS/lib" "$HOME/.muse/x86_64/lib"
  switch (count $argv)
  case 2
    set MIDAS_DIR '~/muse/midasfiles/'
    set RAW_ROOT_DIR '~/muse/rootfiles/cooked_root/'
    set COOKED_ROOT_DIR '~/muse/rootfiles/'
  case 4
    set RAW_ROOT_DIR $argv[3]
    set COOKED_ROOT_DIR $argv[4]
  case '*'
    echo 'must provide either 2 or 4 arguments to know path'
    exit
  end

  # parse which is which
  set -l run_num (string match -r '\d+' $argv[1] $argv[2])
  # remove leading zeros to handle if given with/without them
  set -l run_num (string trim --left --char=0 $run_num)
  set -l plugin (string match -r '\D+' $argv[1] $argv[2])

  # --- IN/OUTPUT FILE NAMES ---
  set -l MIDAS (printf '%srun%05d.mid' $MIDAS_DIR $run_num)
  set -l ROOT (printf '%srun%05d.root' $RAW_ROOT_DIR $run_num)
  set -l OUT_PREFIX (printf '%srun%05d' $COOKED_ROOT_DIR $run_num)

  set -l BH {$OUT_PREFIX}_BH.root
  set -l BH_DETAIL {$OUT_PREFIX}_BH_Detail.root
  set -l BH_CALIB {$OUT_PREFIX}_BH_Calib.root

  set -l BM {$OUT_PREFIX}_BM.root
  set -l BM_DETAIL {$OUT_PREFIX}_BM_Detail.root
  set -l BM_CALIB {$OUT_PREFIX}_BM_Calib.root

  set -l VETO {$OUT_PREFIX}_VETO.root

  set -l TOF {$OUT_PREFIX}_TOF.root

  set -l SPS {$OUT_PREFIX}_SPS.root

  set -l TRIG {$OUT_PREFIX}_Trigger.root
  set -l TRIG_TIMING {$OUT_PREFIX}_Trigger_timing.root
  set -l TRIG_VIS {$OUT_PREFIX}_trig_vis.root
  set -l TRIG_TEST {$OUT_PREFIX}_trig_test.root
  set -l TRIG_OLD {$OUT_PREFIX}_Trigger_old.root

  # --- FIND RIGHT PLUGIN TO RUN ---
  switch (string upper $plugin)
    case MIDAS
      echo cooker recipes/midas2root/midasconverter.xml $MIDAS $ROOT
    case BM
      cooker recipes/BM/BM.xml $ROOT $BM
    case BM_DETAIL
      cooker recipes/BM/BM_detail.xml $ROOT $BM_DETAIL
    case BM_CALIB
      cooker recipes/BM/BM_calib.xml $ROOT $BM_CALIB
      rm -f *.pdf *.log

    case BH
      cooker recipes/BH/BH.xml $ROOT $BH
    case BH_DETAIL
      cooker recipes/BH/BH_detail.xml $ROOT $BH_DETAIL
    case BH_CALIB
      cooker recipes/BH/BH_calib.xml $ROOT $BH_CALIB
      rm -f *.pdf *.log

    case VETO
      cooker recipes/VETO/VETO.xml $ROOT $VETO

    case TOF
      cooker recipes/analysis/TOF.xml $BH:$BM:$VETO $TOF

    case SPS
      cooker recipes/SPS/SPS.xml $ROOT $SPS
    case SPS_DETAIL
      cooker recipes/SPS/SPS.xml $ROOT $SPS
    case SPS_CALIB
      cooker recipes/SPS/SPS.xml $ROOT $SPS

    case TRIG
      cooker recipes/analysis/Trigger.xml $ROOT $TRIG
    case TRIG_TIMING
      cooker recipes/analysis/Trigger_timing.xml $ROOT:$BH $TRIG_TIMING
    case TRIG_VIS
      visco recipes/analysis/trig_vis.xml $ROOT $TRIG_VIS
    case TRIG_TEST
      visco recipes/analysis/Trigger_testhittree.xml $ROOT:$TRIG $TRIG_TEST
    case TRIG_OLD
      cooker recipes/analysis/Trigger_old.xml $ROOT $TRIG_OLD

    case '*'
      echo "this script does not support that plugin: $plugin"
  end
end

