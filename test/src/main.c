#include <stdio.h>
#include "lib.h"
#include <modules/foo.h>

int main() {
	int a,b;
	scanf("%d,%d", &a, &b);
	printf("result 1: %d\n", calc(a,b));
}
