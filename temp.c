#include <stdio.h>
#include <stdlib.h>

int main(void){
char* sus;
sus = malloc(100 * sizeof(char));
scanf("%[^\n]%*c", sus);
printf("%s\n", sus);
return 0;
}