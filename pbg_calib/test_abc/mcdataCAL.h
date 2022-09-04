//
//  mcdataCAL.h
//  mcdigit
//
//  Created by Steffen Strauch on 4/20/21.
//

#ifndef mcdataCAL_hpp
#define mcdataCAL_hpp

#include "mcdata.h"
#include <stdio.h>

class mcdataCAL : public mcdata {
public:
    mcdataCAL(TTree* t, std::string system);
    ~mcdataCAL();
    bool is_available();

    int CAL_Hit;
    VectorInt* CAL_CopyID; // copyID of each hit copy.
    VectorDouble* CAL_W;
    VectorInt* CAL_Particle;
    VectorDouble* CAL_PhotonY;
    VectorDouble* CAL_Time;
    VectorDouble* CAL_PosX;
    VectorDouble* CAL_PosY;
    VectorDouble* CAL_PosZ;
    VectorDouble* CAL_PosHitX;
    VectorDouble* CAL_PosHitY;
    VectorDouble* CAL_PosHitZ;
    VectorDouble* CAL_DirHitX;
    VectorDouble* CAL_DirHitY;
    VectorDouble* CAL_DirHitZ;

private:
    bool is_available_test;
};

#endif /* mcdataCAL_hpp */
