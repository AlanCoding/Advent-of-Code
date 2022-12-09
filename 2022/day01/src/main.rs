use std::io;
use std::io::prelude::*;

fn read() -> Vec<Vec<u32>> {
    // let stdin = io::stdin();
    let mut knapsacks = Vec::new();
    let mut current = Vec::new();
    println!("print lines as I read them");
    for l in io::stdin().lock().lines() {
        let line = l.unwrap();
        // println!("{}", line);
        if line == "" {
            knapsacks.push(current);
            current = Vec::new();
        } else {
            current.push(line.parse().unwrap());
        }
    }
    knapsacks.push(current);

    knapsacks
}


fn main() {
    let knp = read();
    // println!("{:?}", knp);
    let mut max_calories: u32 = 0;
    let mut top_three = vec![0, 0, 0];
    for knapsack in knp {
        // println!("{:?}", knapsack);
        let sum: u32 = knapsack.iter().sum();  // should not need .iter
        println!("max: {}", sum);
        println!("min: {:?}", knapsack.iter().min().unwrap());
        if sum > max_calories {
            max_calories = sum;
        }
        if sum > top_three.iter().cloned().min().unwrap() {
            top_three[0] = sum;
            top_three.sort();
        }
    }
    println!("final count");
    println!("{}", max_calories);
    println!("top three {:?}", top_three);
    println!("sum of top three {:?}", top_three.iter().sum::<u32>());
}
