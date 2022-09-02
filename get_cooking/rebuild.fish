function rebuild -d 'simply goes to build dir, runs make install -j6 and comes back'
    make -C ~/muse/build/ install -j6
end
