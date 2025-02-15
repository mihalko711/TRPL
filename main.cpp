#include <iostream>
#include "eval_xpr.h"
using namespace std;

int main(){
	string pol1 = "(a + b)";
	Expression kek1 = Expression(pol1);
	
	cout << kek1 << endl;
}
