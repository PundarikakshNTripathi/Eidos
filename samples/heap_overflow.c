// samples/heap_overflow.c
// Goal: Test run_sanitizer_suite
// This contains a classic heap buffer overflow.

#include <stdlib.h>
#include <stdio.h>

int main() {
    int *array = (int*)malloc(10 * sizeof(int));
    array[10] = 0; // BOOM: Write out of bounds
    free(array);
    return 0;
}
