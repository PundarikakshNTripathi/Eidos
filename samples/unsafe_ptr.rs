// samples/unsafe_ptr.rs
// Goal: Test analyze_assembly_essence (Rust)

pub fn unsafe_read(ptr: *const i32, offset: isize) -> i32 {
    unsafe {
        *ptr.offset(offset)
    }
}
