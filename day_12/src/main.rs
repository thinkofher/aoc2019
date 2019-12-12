extern crate gcd;

use std::io;
use std::io::prelude::*;
use std::ops::{Add, AddAssign};

use gcd::Gcd;

trait Coordinates {
    fn cords(&self) -> (i32, i32, i32);

    fn energy(&self) -> i32 {
        let (x, y, z) = self.cords();
        vec![x, y, z].into_iter().map(|n| n.abs()).sum()
    }
}

#[derive(Debug, Clone, PartialEq)]
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

impl Point {
    pub fn new(x: i32, y: i32, z: i32) -> Point {
        Point { x: x, y: y, z: z }
    }

    pub fn from_vec(vec: Vec<i32>) -> Point {
        Point::new(
            *vec.get(0).unwrap(),
            *vec.get(1).unwrap(),
            *vec.get(2).unwrap(),
        )
    }
}

#[derive(Debug, Clone, PartialEq)]
struct Velocity {
    x: i32,
    y: i32,
    z: i32,
}

impl Velocity {
    pub fn new() -> Velocity {
        Velocity { x: 0, y: 0, z: 0 }
    }
}

impl Add for Velocity {
    type Output = Velocity;

    fn add(self, other: Velocity) -> Velocity {
        Velocity {
            x: self.x + other.x,
            y: self.y + other.y,
            z: self.z + other.z,
        }
    }
}

impl AddAssign for Velocity {
    fn add_assign(&mut self, other: Self) {
        *self = Self {
            x: self.x + other.x,
            y: self.y + other.y,
            z: self.z + other.z,
        }
    }
}

impl Coordinates for Point {
    fn cords(&self) -> (i32, i32, i32) {
        (self.x, self.y, self.z)
    }
}

impl Coordinates for Velocity {
    fn cords(&self) -> (i32, i32, i32) {
        (self.x, self.y, self.z)
    }
}

#[derive(Debug, Clone, PartialEq)]
struct Planet {
    position: Point,
    velocity: Velocity,
}

impl Planet {
    pub fn from_vec(vec: Vec<i32>) -> Planet {
        Planet {
            position: Point::from_vec(vec),
            velocity: Velocity::new(),
        }
    }

    pub fn apply_gravity(&mut self, gravity: Velocity) {
        self.velocity += gravity;
    }

    pub fn move_by_velocity(&mut self) {
        self.position.x += self.velocity.x;
        self.position.y += self.velocity.y;
        self.position.z += self.velocity.z;
    }
}

type Planets = Vec<Planet>;
type GravityFunc = dyn Fn(Planet, Planets) -> Velocity;

fn gravity_x(planet_to_calc: Planet, planets: Planets) -> Velocity {
    let dx = planets
        .clone()
        .into_iter()
        .filter(|planet| planet.position.x > planet_to_calc.position.x)
        .count() as i32
        - planets
            .clone()
            .into_iter()
            .filter(|planet| planet.position.x < planet_to_calc.position.x)
            .count() as i32;

    Velocity { x: dx, y: 0, z: 0 }
}

fn gravity_y(planet_to_calc: Planet, planets: Planets) -> Velocity {
    let dy = planets
        .clone()
        .into_iter()
        .filter(|planet| planet.position.y > planet_to_calc.position.y)
        .count() as i32
        - planets
            .clone()
            .into_iter()
            .filter(|planet| planet.position.y < planet_to_calc.position.y)
            .count() as i32;

    Velocity { x: 0, y: dy, z: 0 }
}

fn gravity_z(planet_to_calc: Planet, planets: Planets) -> Velocity {
    let dz = planets
        .clone()
        .into_iter()
        .filter(|planet| planet.position.z > planet_to_calc.position.z)
        .count() as i32
        - planets
            .clone()
            .into_iter()
            .filter(|planet| planet.position.z < planet_to_calc.position.z)
            .count() as i32;

    Velocity { x: 0, y: 0, z: dz }
}

fn gravity(planet_to_calc: Planet, planets: Planets) -> Velocity {
    gravity_y(planet_to_calc.clone(), planets.clone())
        + gravity_x(planet_to_calc.clone(), planets.clone())
        + gravity_z(planet_to_calc, planets)
}

fn total_energy(planets: &Planets) -> i32 {
    return planets
        .into_iter()
        .map(|planet| planet.position.energy() * planet.velocity.energy())
        .sum();
}

fn take_steps(planets: &mut Planets, steps: usize, gravity_func: &GravityFunc) {
    for _ in 0..steps {
        let default_planets = planets.clone();

        for planet in planets.into_iter() {
            planet.apply_gravity(gravity_func(planet.clone(), default_planets.clone()));
        }

        for planet in planets.into_iter() {
            planet.move_by_velocity();
        }
    }
}

fn compare_planets(a: &Planets, b: &Planets) -> bool {
    for (first, second) in a.into_iter().zip(b.into_iter()) {
        if first != second {
            return false;
        }
    }
    true
}

fn find_period(planets: &mut Planets, initial_state: &Planets, gravity_func: &GravityFunc) -> u64 {
    let mut n = 0;
    loop {
        take_steps(planets, 1, gravity_func);
        n += 1;
        if compare_planets(initial_state, planets) {
            break n;
        }
    }
}

fn lcm(denominators: Vec<u64>) -> u64 {
    denominators
        .clone()
        .into_iter()
        .fold(*denominators.get(0).unwrap(), |a, b| a * b / a.gcd(b))
}

fn main() {
    let input = io::stdin();

    let mut planets = Vec::new();

    for line in input.lock().lines() {
        let planet_information: Vec<i32> = line
            .unwrap_or_else(|_| {
                eprintln!("Failed to parse data!");
                std::process::exit(1);
            })
            .trim_matches('<')
            .trim_matches('>')
            .split(',')
            .map(|s| String::from(s.trim_matches(' ')))
            .map(|s| {
                String::from(&s[2..]).parse().unwrap_or_else(|_| {
                    eprintln!("Failed to parse data!");
                    std::process::exit(1);
                })
            })
            .collect();
        planets.push(Planet::from_vec(planet_information));
    }

    let initial_state = planets.clone();
    take_steps(&mut planets, 1000, &gravity);
    println!("First ans: {}", total_energy(&planets));

    let mut periods = Vec::new();
    planets.clone_from(&initial_state);
    periods.push(find_period(&mut planets, &initial_state, &gravity_x));
    periods.push(find_period(&mut planets, &initial_state, &gravity_y));
    periods.push(find_period(&mut planets, &initial_state, &gravity_z));

    println!("Second ans: {}", lcm(periods));
}
