#include <iostream>
#include "things.h"
#include "some.h"

namespace sm
{
    namespace lbr
    {
        void printSomething()
        {
            std::cout << "ololo, " << someString << std::endl;
        }
    }
}