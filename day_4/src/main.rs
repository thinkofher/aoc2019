use std::env;

fn collect_args() -> Vec<i32> {
    env::args()
        .skip(1)
        .map(|val| {
            val.parse().unwrap_or_else(|_| {
                eprintln!("Only numerical values as arguments!");
                std::process::exit(1);
            })
        })
        .collect()
}

fn split_to_digits(value: &i32) -> Vec<u8> {
    format!("{}", value)
        .chars()
        .map(|value| value.to_string().parse().unwrap())
        .collect()
}

fn two_adjacent(numbers: &i32) -> bool {
    let numbers_vec = split_to_digits(numbers);
    numbers_vec
        .iter()
        .zip(numbers_vec.iter().skip(1))
        .any(|(first, second)| first == second)
}

fn never_decrase(numbers: &i32) -> bool {
    let numbers_vec = split_to_digits(numbers);
    numbers_vec
        .iter()
        .zip(numbers_vec.iter().skip(1))
        .all(|(first, second)| first <= second)
}

fn main() {
    let numerical_args: Vec<i32> = collect_args();

    let min_value: i32 = *numerical_args.get(0).unwrap_or_else(|| {
        eprintln!("You have to provide minimum value of range!");
        std::process::exit(1);
    });

    let max_value: i32 = *numerical_args.get(1).unwrap_or_else(|| {
        eprintln!("You have to provide maximum value of range!");
        std::process::exit(1);
    });

    if max_value < min_value {
        eprintln!("Maximum value has to be greater than minimum value!");
        std::process::exit(1);
    }

    let codes: Vec<_> = (min_value..max_value + 1)
        .filter(|val| split_to_digits(val).len() == 6)
        .filter(never_decrase)
        .filter(two_adjacent)
        .collect();

    println!("{}", codes.len());
}
