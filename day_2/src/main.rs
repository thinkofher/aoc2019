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

fn main() {
    let input = io::stdin();
    let mut intcode = Vec::new();

    for line in input.lock().lines() {
        let mut code: Vec<i32> = line
            .unwrap_or(String::from(""))
            .split(',')
            .map(|val| val.parse().unwrap())
            .collect();
        intcode.append(&mut code);
    }

    prepare_calculations(&mut intcode, 12, 2);

    for (min, max) in (0..intcode.len() / 4).zip(1..intcode.len() / 4 + 1) {
        let intcode_slice: Vec<usize> = (min * 4..max * 4).collect();

        let operation: Operation;
        let first_value: i32;
        let second_value: i32;
        let ans_position: usize;
        {
            let operation_code = *intcode.get(intcode_slice[0]).unwrap();
            operation = match Operation::from_i32(operation_code) {
                Some(op) => op,
                None => {
                    println!("Code: {}. Program stops.", operation_code);
                    break;
                }
            }
        }
        {
            first_value = *intcode
                .get(*intcode.get(intcode_slice[1]).unwrap() as usize)
                .unwrap();
        }
        {
            second_value = *intcode
                .get(*intcode.get(intcode_slice[2]).unwrap() as usize)
                .unwrap();
        }
        {
            ans_position = *intcode.get(intcode_slice[3]).unwrap() as usize;
        }
        let ans = intcode.get_mut(ans_position).unwrap();
        *ans = operation.execute(first_value, second_value);
    }
    let result: Vec<String> = intcode.iter().map(|val| format!("{}", val)).collect();
    println!("{}", result.join(","));
}
