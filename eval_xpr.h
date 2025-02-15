#include <iostream>
#include <string>
#include <stack>

using namespace std;

class Expression
{
    private:
        string xpr_str;
    public:
        Expression(string xpr_str);
        Expression& operator=(const Expression& obj);
        friend ostream& operator<<(ostream& os, const Expression& obj);
};