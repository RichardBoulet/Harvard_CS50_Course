#include <stdio.h>

#include <cs50.h>

#include <math.h>

#include <stdlib.h>

// Get the length of long

int countdigit(long n)
{
    int count = 0;

    while (n != 0)

    {
        n = n / 10;
        ++count;
    }

    return count;
}

// Credit card company checker script using C

int main(void)

{
    long card;
    int count;

    // Get card number
    card = get_long("Enter Your Card Number: ");

    count = countdigit(card);

    if (count < 13)
    {
        printf("INVALID\n");
        exit(0);
    }

    // Get first digit of card number

    long power = pow(10, count - 1);

    int first_digit = card / power;

    // Initiate if thens for different card types

    int other_stop;
    string valid;

    if ((count == 16) && (first_digit == 4))

    {
        other_stop = count / 2;
        valid = "VISA";
    }

    if (count == 15)

    {
        other_stop = count / 2 + 1;
        valid = "AMEX";
    }

    if (count == 13)

    {
        other_stop = count / 2 + 1;
        valid = "VISA";
    }

    if ((count == 16) && (first_digit == 5))

    {
        other_stop = count / 2;
        valid = "MASTERCARD";
    }

    // Card check

    int i;
    int digits_sum = 0;
    int digit_tens;
    long card_1 = card;
    int digit;

    for (i = 1; i <= count / 2; i++)
    {
        digit = (card_1 % 100);
        digit /= 10;
        digit = digit * 2;

        if (digit > 9)
        {
            digit_tens = digit - 10;
            digits_sum = digits_sum + 1 + digit_tens;
        }
        else
        {
            digits_sum = digits_sum + digit;
        }

        card_1 /= 100;

    }

    int other_digits_sum = 0;
    int other_digit;
    long card_2 = card;
    i = 1;

    for (i = 1; i <= other_stop; i++)
    {
        other_digit = (card_2 % 10);

        other_digits_sum = other_digits_sum + other_digit;

        card_2 /= 100;
    }

    digits_sum = digits_sum + other_digits_sum;

    string notvalid = "INVALID";

    if ((digits_sum % 10) == 0)

    {
        printf("%s\n", valid);
    }

    else

    {
        printf("%s\n", notvalid);
    }

}