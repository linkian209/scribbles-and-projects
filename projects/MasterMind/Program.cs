using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MasterMind
{
    class Program
    {
        // Globals
        const int CODE_SIZE = 4;
        // Find Struct
        struct Find
        {
            public int data, currentIndex;
            public bool found;
            public int[] indexes;
            public bool minusAdded;

            public Find(int d)
            {
                data = d;
                currentIndex = 0;
                found = false;
                minusAdded = false;
                indexes = new int[CODE_SIZE];
                for(int i = 0; i < CODE_SIZE; ++i)
                {
                    indexes[i] = -1;
                }
            }
        }

        static void Main(string[] args)
        {
            // Application Variables
            int[] secretCode = new int[CODE_SIZE];
            int numOfGuesses = 5; // Default to 5
            if(args.Length != 0)
            {
                numOfGuesses = int.Parse(args[0]);
            }

            // Create Secret Code
            Random rand = new Random();
            //Console.Out.Write("Secret Code: ");
            for(int i = 0; i < CODE_SIZE; ++i)
            {
                secretCode[i] = (rand.Next() % 6) + 1;
                //Console.Out.Write("[" + secretCode[i] + "]");
            }
            //Console.Out.Write('\n');

            // Main Loop
            Console.Out.Write("Playing Mastermind with " + numOfGuesses + " guess" + (numOfGuesses != 1 ? "es.\n" : ".\n"));
            bool complete = false;
            bool cracked = false;
            int numOfTries = 0;
            do
            {
                // Parse in User Guess
                bool parsed = false;
                int guess;
                do
                {
                    Console.Out.Write("Please enter your guess as a single number with no spaces: ");
                    string strGuess = Console.In.ReadLine();
                    if(int.TryParse(strGuess, out guess))
                    {
                        guess = int.Parse(strGuess);
                        parsed = true;
                    }
                    else
                    {
                        Console.Out.Write(strGuess + " is an invalid guess. ");
                    }
                } while (!parsed);

                // Make an array out of the user guess
                int[] userGuess = new int[CODE_SIZE];
                for(int j = 0; j < CODE_SIZE; ++j)
                {
                    // Get each individual number of the array
                    // Dividing by 10 ^ j gets us the correct digit in the ones place, 
                    // then % 10 to get the single digit
                    userGuess[CODE_SIZE-1-j] = (guess / Convert.ToInt32(Math.Pow(10,j))) % 10;
                }

                /* FOR DEBUG
                Console.Out.Write("User Guess: ");
                for(int k = 0; k < userGuess.Length; ++k)
                {
                    Console.Out.Write("[{0}]", userGuess[k]);
                }
                Console.Out.Write('\n');
                */

                // Check if we got the correct guess
                numOfTries++;
                cracked = checkCodes(secretCode, userGuess);

                //Console.Out.Write(cracked + "\n");

                if(cracked)
                {
                    Console.Out.Write("You Solved it!!! You got it correct in {0} guess" + (numOfTries > 1 ? ".\n" : "es.\n"), numOfTries);
                }

                if(numOfTries == numOfGuesses)
                {
                    complete = true;
                    Console.Out.Write("You Lose :(\n");
                }
            } while (!complete && !cracked);
        }

        static bool checkCodes(int[] secretCode, int[] userCode)
        {
            // Assume we got it wrong
            bool retval = false;
            // Print parameters
            int numOfStars = 0, numOfMinuses = 0;

            // Make a copy of the secret code
            int[] copy = new int[CODE_SIZE];
            for(int q = 0; q < CODE_SIZE; ++q)
            {
                copy[q] = secretCode[q];
            }

            // Now check to see how many stars we have
            for(int i = 0; i < CODE_SIZE; ++i)
            {
                // If we subtract the numbers and get a 0, they are the same.
                copy[i] -= userCode[i];
                if(copy[i] == 0)
                {
                    numOfStars++;
                }
            }

            // If we have 4 stars, we have the code
            if (numOfStars == 4)
            {
                retval = true;
            }

            // Now check for minuses if we need to
            if(numOfStars != 4)
            {

                for(int k = 0; k < copy.Length; ++k)
                {
                    // Search array to see if a match exists
                    Find currNum = checkNumOfInstances(secretCode, userCode[k]);

                    // If the number exists in the array
                    if(currNum.found)
                    {
                        // Check the indexes
                        for(int r = 0; currNum.indexes[r] != -1; ++r)
                        {
                            // We have dealt with this number, ignore it
                            if(copy[currNum.indexes[r]] == 0)
                            {
                                continue;
                            }
                            else
                            {
                                // Only do this to the first non dealt with instance of the number
                                copy[currNum.indexes[r]] = 0;
                                numOfMinuses++;
                                break;
                            }
                            
                        }
                    }
                }
            }

            // Print Program Response
            string stars = "", minuses = "";
            for(int j = 0; j < (numOfStars >= numOfMinuses ? numOfStars : numOfMinuses); ++j)
            {
                if(j < numOfStars)
                {
                    stars += "*";
                }

                if(j < numOfMinuses)
                {
                    minuses += "-";
                }
            }

            Console.Out.Write(stars + minuses + "\n");

            return retval;
        }

        static Find checkNumOfInstances(int[] code, int num)
        {
            Find retval = new Find(num);

            // Check to see if we can find the number
            for(int i = 0; i < CODE_SIZE; ++i)
            {
                if(code[i] == num)
                {
                    retval.found = true;
                    retval.indexes[retval.currentIndex++] = i;
                }
            }
            return retval;
        }
    }
}
