# Mastermind
This was a coding problem I had to do for a Job Interview. It had to meet the
following criteria:

The application creates a secret code of 4 digits. Each digit must be between 1 and 6. The code breaker
(user) gets some number of chances to figure out the code (configurable). The code breaker will enter
their guess at the command line when prompted (ex: 1234). The application will then respond with
some number of +’s and -’s where the +’s are always printed before the -’s. If the code breaker guesses
correctly, the program prints “You solved it!”. If the code breaker runs out of tries, the program prints
“You lose :(“
The scoring rules are:
  - For each number in the guess that matches the number and position of a number
    in the secret code, the score includes one plus sign. For each number in the guess
    that matches the number but not the position of a number in the secret code,
    the score includes one minus sign.

  - Each position in the secret code can only be matched once. For example, a
    guess of 1134 against a secret code of 1234 would get three plus signs: one
    for each of the exact matches in the first, third and fourth positions. The
    number match in the second position would be ignored.
