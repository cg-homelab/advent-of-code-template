mod part1;
mod part2;

use std::process::ExitCode;
use std::{env, fs};

fn main() -> ExitCode {
    let part = env::args().nth(1).unwrap_or_default();
    let input = fs::read_to_string("input.txt")
        .expect("input.txt missing — paste your puzzle input");
    match part.as_str() {
        "1" => println!("{}", part1::process(&input)),
        "2" => println!("{}", part2::process(&input)),
        _ => {
            eprintln!("usage: day-__DAY__ <1|2>");
            return ExitCode::FAILURE;
        }
    }
    ExitCode::SUCCESS
}
