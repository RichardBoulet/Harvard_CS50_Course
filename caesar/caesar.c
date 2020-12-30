#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>

int valid_1_0(string s);

// main

int main(int argc, string argv[])
{

    int k = atoi(argv[1]) ; // get ascii to integer

    int valid_check = valid_1_0(argv[1]) ;


    // exit if conditions not met
    if(argc != 2 || k < 0 || valid_check < 1) // checks length of argc and that k is positive
    {
        printf( "Usage: ./caesar key\n" ) ;
        return 1;
    }



    string text = get_string("plaintext: ") ;

    printf("ciphertext: ") ;

    int i ;

    int char_int ;

    int length = strlen(text) ;

    for(i = 0; i < length; i++)
    {
        char letter = text[i];

        if(isalpha(letter))
        {
            char modify = 'A';

            if(islower(letter))
            {
                modify = 'a' ;
            }
            printf("%c", (letter - modify + k) % 26 + modify) ;

        }

        else
            printf("%c", letter);
        }

    printf("\n");
    return 0;

}



int valid_1_0(string s)
{
    int length = strlen(s);
    int i;

    for (i = 0; i < length; i++)
    {
        if(!isdigit(s[i]))
        {
            return 0;
        }

    }

    return 1;
}