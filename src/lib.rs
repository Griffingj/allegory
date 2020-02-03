extern crate core;

#[no_mangle]
pub extern "C" fn times2(x: i32) -> i32 {
    x * 2
}

pub mod rust;