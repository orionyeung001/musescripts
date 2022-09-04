//
//  mcdata.hpp
//  mcdigit
//
//  Created by Steffen Strauch on 4/1/21.
//

#ifndef mcdata_hpp
#define mcdata_hpp

#include <TTree.h>
#include <stdio.h>
#include <string.h>

class mcdata {
public:
    mcdata(TTree* t, std::string system);
    virtual ~mcdata() = 0;

    typedef std::vector<int> VectorInt;
    typedef std::vector<double> VectorDouble;

    virtual bool is_available() = 0;
    std::string get_system_id();

protected:
    TTree* tree;
    std::string system_id;

    bool is_available(std::string name);
};

#endif /* mcdata_hpp */
