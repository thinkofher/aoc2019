use std::io;
use std::io::prelude::*;

fn calculate_fuel(mass: i32) -> i32 {
    (mass / 3) - 2
}

fn main() {
    let input = io::stdin();
    let mut total_fuel = 0;

    for line in input.lock().lines() {
        let mass_of_module: i32 = line.unwrap().parse().unwrap_or(0);
        total_fuel += calculate_fuel(mass_of_module);
    }
    println!("Total fuel needed: {}", total_fuel);
}
