# no need to test machine since I can't imagine I'll call this from a login
# shell if I'm on the wrong machine

fish_add_path --global "/Users/orion/.muse/x86_64/bin/"

alias root 'root -l'
source "$ROOTSYS/bin/thisroot.fish"
set -gx DYLD_LIBRARY_PATH "$ROOTSYS/lib" "$HOME/.muse/x86_64/lib"
cd $HOME/muse

set -gx G4NEUTRONHPDATA "/Users/orion/packages/geant4/geant4-10.7.3-install/share/Geant4-10.7.3/data/G4NDL4.6"
set -gx G4LEDATA "/Users/orion/packages/geant4/geant4-10.7.3-install/share/Geant4-10.7.3/data/G4EMLOW7.13"
set -gx G4LEVELGAMMADATA "/Users/orion/packages/geant4/geant4-10.7.3-install/share/Geant4-10.7.3/data/PhotonEvaporation5.7"
set -gx G4RADIOACTIVEDATA "/Users/orion/packages/geant4/geant4-10.7.3-install/share/Geant4-10.7.3/data/RadioactiveDecay5.6"
set -gx G4PARTICLEXSDATA "/Users/orion/packages/geant4/geant4-10.7.3-install/share/Geant4-10.7.3/data/G4PARTICLEXS3.1.1"
set -gx G4PIIDATA "/Users/orion/packages/geant4/geant4-10.7.3-install/share/Geant4-10.7.3/data/G4PII1.3/"
set -gx G4REALSURFACEDATA "/Users/orion/packages/geant4/geant4-10.7.3-install/share/Geant4-10.7.3/data/RealSurface2.2"
set -gx G4SAIDXSDATA "/Users/orion/packages/geant4/geant4-10.7.3-install/share/Geant4-10.7.3/data/G4SAIDDATA2.0"
set -gx G4ABLADATA "/Users/orion/packages/geant4/geant4-10.7.3-install/share/Geant4-10.7.3/data/G4ABLA3.1"
set -gx G4INCLDATA "/Users/orion/packages/geant4/geant4-10.7.3-install/share/Geant4-10.7.3/data/G4INCL1.0"
set -gx G4ENSDFSTATEDATA "/Users/orion/packages/geant4/geant4-10.7.3-install/share/Geant4-10.7.3/data/G4ENSDFSTATE2.3"
