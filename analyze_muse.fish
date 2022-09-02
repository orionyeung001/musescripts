#! /usr/local/bin/fish
function analyze_muse -d 'Runs multi analysis for single given run number'
  set -l RAW_ROOT_DIR '~/muse/rootfiles/cooked_root/'
  set -l COOKED_ROOT_DIR '~/muse/rootfiles'
  set -l needs_prereqs false # assert already has prerequisites
  set -l needs_recompile false # assert need to recompile
  set -l show_after true # assert need to open last few root files
  set -l log_event_text false # assert no need to save output

  # do options
  set -l options 'n/new' 'C/nocompile' 'c/compile' 's/show' 'S/noshow' 't/eventtext'
  argparse --name=analyze $options -- $argv

  if set -q _flag_S
    set show_after false
  end

  if set -q _flag_s
    set show_after true
  end

  if set -q _flag_n
    set needs_prereqs true
  end

  if set -q _flag_C
    set needs_recompile false
  end

  if set -q _flag_c
    set needs_recompile true
  end

  if set -q _flag_t
    set log_event_text true
  end

  # if $log_event_text
  #   # uncomments
  #   sed -i '' '/#define __TRIG_TDC_DEBUG/s;// ;;g' '~/muse/src/plugins/analysis/Trigger/src/trigger_timing.cpp'
  # else
  #   # comments
  #   sed -i '' '/#define __TRIG_TDC_DEBUG/s;^#;// #;' '~/muse/src/plugins/analysis/Trigger/src/trigger_timing.cpp'
  # end



# ---- recompile if needed
  if $needs_recompile
    make -C ~/muse/build/ install -j6
    # >$TMPDIR/cmake.log 2>$TMPDIR/cmake.err

    if test $status -ne 0
      bat $TMPDIR/cmake.err $TMPDIR/cmake.out
      return 1
    else
      cd ~/muse
    end
  end

# ---- save the args to be readable
  set -l run_num $argv[1]
  set -l plugins $argv[2..]
  echo "running plugins: $plugins"

# ---- run analysis
  for plugin in $plugins
    if $needs_prereqs
      switch $plugin
        case TOF
          analyze_muse -C $run_num BH BM VETO TOF
          set -e new_run
        case TRIG_TIMING
          analyze_muse -C $run_num BH TRIG_TIMING
          set -e new_run
        case '*'
          echo -- "$plugin is not yet supported needing -n/--new flag"
      end

    else
      __muse_analyze_one $run_num $plugin
    end # end of if need prereq
  end

  if $show_after
    root (ls -lt rootfiles/*.root | head -n5 | tr -s ' ' | cut -d' ' -f9)
  end

  if $log_event_text
    head -n10000 "txt_data/event_disp_output.txt" > (printf '%05d.out' $run_num)
  end

end # end of analyze_muse


