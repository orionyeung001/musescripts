//
//  mcdataCAL.cpp
//  mcdigit
//
//  Created by Steffen Strauch on 5/20/21.
//

#include "mcdataCAL.h"
#include <iostream>
#include <TRandom.h>


mcdataCAL::mcdataCAL(TTree* t, std::string system)
    : mcdata(t, system)
{
   CAL_Hit = 0;
   CAL_CopyID = nullptr; // copyID of each hit copy.
   CAL_W = nullptr;
   CAL_Particle = nullptr;
   CAL_PhotonY = nullptr;
   CAL_Time = nullptr;
   CAL_PosX = nullptr;
   CAL_PosY = nullptr;
   CAL_PosZ = nullptr;
   CAL_PosHitX = nullptr;
   CAL_PosHitY = nullptr;
   CAL_PosHitZ = nullptr;
   CAL_DirHitX = nullptr;
   CAL_DirHitY = nullptr;
   CAL_DirHitZ = nullptr;
    
    is_available_test = mcdata::is_available(system_id + "_Hit");

    if (is_available_test) {
        tree->SetBranchStatus((system + "*").c_str(),1);
        tree->SetBranchAddress((system + "_Hit").c_str(), &CAL_Hit);
        tree->SetBranchAddress((system + "_CopyID").c_str(), &CAL_CopyID);
        tree->SetBranchAddress((system + "_W").c_str(), &CAL_W);
        tree->SetBranchAddress((system + "_ParticleID").c_str(), &CAL_Particle);
        tree->SetBranchAddress((system + "_PhotonY").c_str(), &CAL_PhotonY);
        tree->SetBranchAddress((system + "_Time").c_str(), &CAL_Time);
        tree->SetBranchAddress((system + "_PosX").c_str(), &CAL_PosX);
        tree->SetBranchAddress((system + "_PosY").c_str(), &CAL_PosY);
        tree->SetBranchAddress((system + "_PosZ").c_str(), &CAL_PosZ);
        tree->SetBranchAddress((system + "_PosHitX").c_str(), &CAL_PosHitX);
        tree->SetBranchAddress((system + "_PosHitY").c_str(), &CAL_PosHitY);
        tree->SetBranchAddress((system + "_PosHitZ").c_str(), &CAL_PosHitZ);
        tree->SetBranchAddress((system + "_DirHitX").c_str(), &CAL_DirHitX);
        tree->SetBranchAddress((system + "_DirHitY").c_str(), &CAL_DirHitY);
        tree->SetBranchAddress((system + "_DirHitZ").c_str(), &CAL_DirHitZ);
    }
}

mcdataCAL::~mcdataCAL()
{
    
}

bool mcdataCAL::is_available()
{
    return is_available_test;
}

