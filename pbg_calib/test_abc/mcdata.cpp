//
//  mcdata.cpp
//  mcdigit
//
//  Created by Steffen Strauch on 4/1/21.
//

#include "mcdata.h"
#include <iostream>

mcdata::mcdata(TTree* t, std::string system)
    : tree(t)
    , system_id(system)
{
}

mcdata::~mcdata()
{
}

bool mcdata::is_available(std::string name)
{
    // test if certain branch exists
    for (auto branch : *tree->GetListOfBranches()) {
        if (branch->GetName() == name)
            return true;
    }
    std::cout << "mcdata::is_available: Can't find " << name << " in g4PSI tree.\n";
    return false;
}

std::string mcdata::get_system_id()
{
    return system_id;
}
