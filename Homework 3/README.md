# Homework 3 - Divide and Conquer 

Two positive integers always have common factors. For example, the common factors 12 and 18 are 1, 2, 3, and 6, 
because we 12 and 18 are divisible by these numbers. 
The greatest common divisor (GCD) of a number is the largest number by which both numbers are divisible. 
In the example, the number 6 is the GCD of 12 and 18.

There are at least two methods for calculating GCD of two numbers. 
One is the method of successive divisions. 
In this process we make several divisions until we reach an exact division. 
The divisor of this division is the GCD. For example, for the 48 and 30 we have:

Practical rule:
  1) we divide the largest number by the smallest number:
   48/30 = 1 (with remainder of 18)
  2) we divide 30 (the divisor of the previous division) by 18 (the rest of the previous division) and so on:
   - 30/18 = 1 (with remainder of 12)
   - 18/12 = 1 (with remainder of 6)
   - 12/6 = 2 (exact division)
3) The divisor of the exact division is 6. So the GCD of 48 and 30 is 6.

Implement a "divide and conquer" algorithm that solves the GCD problem for any two positive integers A and B.

You must implement a function called GCD(a,b)


Provide the solution and an explanation of your solution in a notebook in your Github repository.