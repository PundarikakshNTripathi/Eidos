// samples/vectorization_fail.cpp
// Goal: Test analyze_assembly_essence
// This loop has a pointer aliasing issue that often prevents auto-vectorization.

void add_arrays(int* a, int* b, int* c, int n) {
    for (int i = 0; i < n; i++) {
        a[i] = b[i] + c[i];
    }
}
