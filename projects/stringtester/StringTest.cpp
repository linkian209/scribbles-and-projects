#include "StringTest.hpp"
#include <iostream>

void StringTest::testStrings(std::vector<std::string> inputStrings)
{
	// Now start the big loop through all strings
	for (int currIndex = 0; currIndex < inputStrings.size(); ++currIndex)
	{
		// Get current string
		std::string currString = inputStrings.at(currIndex);

		//add the number of input chars to the vector and total count
		inputChars += currString.size();
		stringLengths.push_back(currString.size());

		//Check if there is a hyphen at the end
		if (currString[currString.size() - 1] == '-')
		{
			std::cout << "Hyphen at end!" << std::endl;

			// Remove the hyphen and concatinate the current and next strings
			currString = currString.substr(0, currString.size() - 1);
			// Make sure we don't go over, otherwise we just use the current string if we are at the end
			if (currIndex + 1 <= inputStrings.size())
			{
				std::string nextString = inputStrings.at(++currIndex);
				// Add input char counts
				inputChars += nextString.size();
				stringLengths.push_back(nextString.size());
				// Concat strings
				currString += nextString;
			}
		}

		// Check if we have 3 caps in the first 5 chars
		int capCount = 0;
		for (int i = 0; i < (currString.size() >= 5 ? 5 : currString.size()); ++i)
		{
			if (isupper(currString[i]))
			{
				++capCount;
			}
		}

		if (capCount >= 3)
		{
			std::cout << "More than 3 caps!" << std::endl;
			for (int j = 0; j < currString.size(); ++j)
			{
				currString[j] = static_cast<char>(toupper(currString[j]));
			}
		}

		// Perform one of the following ops based on string length
		std::string output = currString;
		//If we have a multiple of 4, reverse string
		if (currString.size() % 4 == 0)
		{
			std::cout << "Reverse String!" << std::endl;

			// Push in chars to a stack then pop them off to reverse string
			std::stack<char> tempStack;
			for (int k = 0; k < currString.size(); ++k)
			{
				tempStack.push(currString[k]);
			}

			for (int l = 0; tempStack.size(); ++l)
			{
				output[l] = tempStack.top();
				tempStack.pop();
			}
		}

		// If we have a multiple of 5, truncate to 5
		if ((currString.size() % 5) == 0)
		{
			std::cout << "Truncate!" << std::endl;
			output = currString.substr(0, 5);
		}

		// Else the output is the input


		// Output statistics
		outputChars += output.size();
		stringLengths.push_back(output.size());

		// Add output to output strings vector
		outputStrings.push_back(output);
	}

	// Output Strings
	std::cout << std::endl;
	for (int m = 0; m < outputStrings.size(); ++m)
	{
		std::cout << "String #" << m + 1 << ": " << outputStrings.at(m) << std::endl;
	}

}

void StringTest::printStatistics()
{
	// Output Stats
	std::cout << std::endl << "Statistics:" << std::endl;
	std::cout << "Total input characters: " << inputChars << std::endl;
	std::cout << "Total output characters: " << outputChars << std::endl;
	float average = 0;
	for (int n = 0; n < stringLengths.size(); ++n)
	{
		average += stringLengths.at(n);
	}
	average = average / stringLengths.size();
	std::cout << "Average String Length: " << average << std::endl;
}