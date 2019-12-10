use std::env;
use std::io;
use std::io::prelude::*;

enum Operation {
    Add,
    Multiply,
}

impl Operation {
    fn from_i32(code: i32) -> Option<Operation> {
        match code {
            1 => Some(Operation::Add),
            2 => Some(Operation::Multiply),
            _ => None,
        }
    }

    fn execute(&self, a: i32, b: i32) -> i32 {
        match &self {
            Operation::Add => a + b,
            Operation::Multiply => a * b,
        }
    }
}

fn prepare_calculations(intcode: &mut Vec<i32>, noun: i32, verb: i32) {
    {
        let val = intcode.get_mut(1).unwrap();
        *val = noun;
    }
    let val = intcode.get_mut(2).unwrap();
    *val = verb;
}

fn solve_intcode(mut intcode: Vec<i32>) -> i32 {
    for (min, max) in (0..intcode.len() / 4).zip(1..intcode.len() / 4 + 1) {
        let parameters_positions: Vec<usize> = (min * 4..max * 4).collect();

        let operation: Operation;
        let first_value: i32;
        let second_value: i32;
        let ans_position: usize;
        {
            let operation_code = *intcode.get(parameters_positions[0]).unwrap();
            operation = match Operation::from_i32(operation_code) {
                Some(op) => op,
                None => {
                    break;
                }
            }
        }
        {
            first_value = *intcode
                .get(*intcode.get(parameters_positions[1]).unwrap() as usize)
                .unwrap();
        }
        {
            second_value = *intcode
                .get(*intcode.get(parameters_positions[2]).unwrap() as usize)
                .unwrap();
        }
        {
            ans_position = *intcode.get(parameters_positions[3]).unwrap() as usize;
        }
        let ans = intcode.get_mut(ans_position).unwrap();
        *ans = operation.execute(first_value, second_value);
    }
    return *intcode.get(0).unwrap();
}

fn main() {
    let input = io::stdin();
    let mut intcode = Vec::new();

    let numerical_args: Vec<i32> = env::args()
        .skip(1)
        .map(|val| {
            val.parse().unwrap_or_else(|_| {
                eprintln!("Only numerical values as arguments!");
                std::process::exit(1);
            })
        })
        .collect();

    let search_value: i32 = *numerical_args.get(0).unwrap_or_else(|| {
        eprintln!("You have to provide value for search!");
        std::process::exit(1);
    });

    for line in input.lock().lines() {
        let mut code: Vec<i32> = line
            .unwrap_or(String::from(""))
            .split(',')
            .map(|val| val.parse().unwrap())
            .collect();
        intcode.append(&mut code);
    }

    prepare_calculations(&mut intcode, 12, 2);

    let mut ans: Option<i32> = None;
    for noun in 0..100 {
        for verb in 0..100 {
            let mut intcode_to_solve = intcode.clone();
            prepare_calculations(&mut intcode_to_solve, noun, verb);
            let solved_value = solve_intcode(intcode_to_solve);
            if solved_value == search_value {
                ans = Some(100 * noun + verb);
            }
        }
    }

    match ans {
        Some(value) => println!("{}", value),
        None => println!("Could not find the answer.")
    }
}
