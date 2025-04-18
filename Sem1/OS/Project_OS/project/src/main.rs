fn main() {
    unsafe {
        read_out_of_bounds();
    }
}

unsafe fn read_out_of_bounds() {
    let arr = [1, 2, 3, 4];
    unsafe {
        let val = *arr.as_ptr().add(4);
        println!("Read value: {}", val);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic(expected = "index out of bounds")]
    fn test_out_of_bounds_access() {
        // We're testing if the function panics as expected when accessing out of bounds.
        unsafe {
            read_out_of_bounds();
        }
    }
}
