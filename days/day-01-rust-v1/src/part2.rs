pub fn process(input: &str) -> String {
    // Placeholder: total number of characters across all lines.
    input
        .lines()
        .map(|line| extract(line))
        .sum::<u32>()
        .to_string()
}

fn extract(line: &str) -> u32 {
    let mut fixed_line = (0..line.len()).filter_map(|index| {
        let line_from_index = &line[index..];
        let result = if line_from_index.starts_with("one") {
            '1'
        } else if line_from_index.starts_with("two") {
            '2'
        } else if line_from_index.starts_with("three") {
            '3'
        } else if line_from_index.starts_with("four") {
            '4'
        } else if line_from_index.starts_with("five") {
            '5'
        } else if line_from_index.starts_with("six") {
            '6'
        } else if line_from_index.starts_with("seven") {
            '7'
        } else if line_from_index.starts_with("eight") {
            '8'
        } else if line_from_index.starts_with("nine") {
            '9'
        } else {
            line_from_index.chars().next().unwrap()
        };

        result.to_digit(10)
    });

    let first = fixed_line.next().expect("Must be a number");

    match fixed_line.last() {
        Some(last) => format!("{0}{1}", first, last),
        None => format!("{0}{1}", first, first),
    }
    .parse::<u32>()
    .unwrap()
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
