
/*A Polynomial-time reduction is a method for solving one problem using another.
E-TM = {< M > : M is a TM and L(M) = \phi}
CLIQUE = {< G, k > : graph G has a clique with at least k vertices}.

Note –
Since CLIQUE is NP => some NDTMCLIQUE accepts CLIQUE.

Reduction(<G, k>)
    construct the following machine M
    M(x):
        1.Run NDTMCLIQUE on input <G, k>.
    2. If NDTMCLIQUE accepts; M rejects x.
    3. Else; M accepts x.
    return <M>
8
We convert the instance <G, k> \in CLIQUE to a TM <M> \in E-TM. And <G, k> \notin CLIQUE to a TM <M> \notin E-TM.*/

//Logarithmic reduction

int N = 16;
int number_of_operations = 0;

Console.Write("Logarithmic reduction of N: ");
for (int i = N; i > 1; i = i / 2)
{
    Console.Write(i + " ");
    number_of_operations++;
}
Console.WriteLine();
Console.WriteLine("Algorithm Runtime for reducing N to 1: " + number_of_operations);