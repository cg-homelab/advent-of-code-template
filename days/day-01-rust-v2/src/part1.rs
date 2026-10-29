pub fn process(input: &str) -> String {
    input
        .lines()
        .map(|line| {
            let mut digits = line
                .bytes()
                .filter(u8::is_ascii_digit)
                .map(|b| u32::from(b - b'0'));
            let first = digits.next().expect("line without a digit");
            let last = digits.next_back().unwrap_or(first);
            first * 10 + last
        })
        .sum::<u32>()
        .to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example() {
        let input = include_str!("../example1.txt");
        assert_eq!(process(input), "142");
    }
}
