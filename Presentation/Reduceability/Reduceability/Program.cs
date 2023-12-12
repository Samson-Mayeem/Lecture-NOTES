using System;

namespace Reduceability
{
    internal class Program
    {
        static void Main(string[] args)
        {
            int N = 16;
            int number_of_operations = 0;

            System.out.print("Logarithmic reduction of N: ");
            for (int i = N; i > 1; i = i / 2)
            {
                System.out.print(i + " ");
                number_of_operations++;
            }
            System.out.println();
            System.out.print("Algorithm Runtime for reducing N to 1: " + number_of_operations);
        }
    }
    }
}
