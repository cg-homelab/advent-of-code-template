const WORDS: [&str; 9] = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
];

pub fn process(input: &str) -> String {
    input.lines().map(extract).sum::<u32>().to_string()
}

fn extract(line: &str) -> u32 {
    let bytes = line.as_bytes();
    let mut digits = (0..bytes.len()).filter_map(|i| {
        if bytes[i].is_ascii_digit() {
            Some(u32::from(bytes[i] - b'0'))
        } else {
            WORDS
                .iter()
                .position(|w| bytes[i..].starts_with(w.as_bytes()))
                .map(|p| p as u32 + 1)
        }
    });
    let first = digits.next().expect("line without a digit");
    let last = digits.next_back().unwrap_or(first);
    first * 10 + last
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example() {
        let input = include_str!("../example2.txt");
        assert_eq!(process(input), "281");
    }
}
