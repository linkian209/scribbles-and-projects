#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include "StringTest.hpp"

int main(int argc, const char* argv[])
{
	//Parse inputs
	if (argc != 2)
	{
		std::cout << "Not enough inputs." << std::endl << "Usage: StringTester.exe <string list .txt>" << std::endl;
		return 1;
	}

	// Declarations
	std::string stringlistFile = argv[1];
	std::vector<std::string> inputStrings;


	// Read in strings
	std::filebuf file;	
	if (file.open(stringlistFile.c_str(), std::ios::in))
	{
		std::istream input(&file);
		while (input)
		{
			std::string temp;
			std::getline(input, temp, '\n');
			std::cout << temp << std::endl;
			// Only add if it is not an empty string
			if (temp != "")
			{
				inputStrings.push_back(temp);
			}
		}
		file.close();
	}
	else
	{
		std::cout << "File does not exist or could not be openned!" << std::endl;
		return 1;
	}

	std::cout << "Start Loop" << std::endl;

	// Call the String Tester
	StringTest tester;
	tester.testStrings(inputStrings);
	tester.printStatistics();

	return 0;
}