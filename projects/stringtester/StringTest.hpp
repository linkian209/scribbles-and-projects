#ifndef STRINGTEST_H
#define STRINGTEST_H

#include <stack>
#include <iomanip>
#include <vector>
#include <string>

class StringTest
{
	private:
		std::vector<int> stringLengths;
		std::vector<std::string> outputStrings;
		int inputChars = 0, outputChars = 0, averageLength = 0;

	public:
		// Constructor and Destructor
		StringTest() {}
		~StringTest() {}

		//Test Strings function
		void testStrings(std::vector<std::string> inputStrings);

		//Print Statistics
		void printStatistics();
};
#endif
