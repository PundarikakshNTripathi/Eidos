// samples/logic_bug.cpp
// Goal: Test explain_ast_logic
// Contains a common "assignment in if" logic bug.

#include <stdio.h>

void check_value(int x) {
    if (x = 5) { // Logic Bug: Assignment instead of comparison
        printf("x is 5\n");
    } else {
        printf("x is not 5\n");
    }
}
