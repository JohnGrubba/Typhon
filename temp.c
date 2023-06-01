#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

int main(void){
int integer = 2;
bool boolean = false;

boolean = false;

printf("%d\n", integer);
printf("%s\n", boolean ? "true" : "false", boolean);

char* input_str;

input_str = malloc(100 * sizeof(char));
scanf("%s", input_str);

printf("%s\n", input_str);
return 0;
}