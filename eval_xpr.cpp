#include "eval_xpr.h"

Expression::Expression(string xpr_str)
{
    this->xpr_str = xpr_str;
}

ostream& operator<<(ostream& os, const Expression& xpr)
{
    os << "Expression: " << xpr.xpr_str;
    return os;
}

Expression::Expression& operator=(const Expression& xpr)
{
    this->xpr_str = xpr.xpr_str;
}