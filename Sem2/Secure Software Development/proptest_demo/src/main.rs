use std::io::{self, Write};

/// Returns true if `year` is a leap year in the Gregorian calendar.
fn is_leap_year(year: u32) -> bool {
    (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)
}

/// Given a month (1–12) and year, returns the maximum valid day for that month.
fn days_in_month(year: u32, month: u32) -> u32 {
    match month {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11             => 30,
        2 if is_leap_year(year)    => 29,
        2                          => 28,
        _                          => 0, // invalid month
    }
}

/// Parses a date string of the form "YYYY-MM-DD" into (year, month, day),
/// returning `None` if the format is wrong or any component is out of range.
fn parse_date(s: &str) -> Option<(u32, u32, u32)> {
    // Format check
    if s.len() != 10 || !s.is_ascii() {
        return None;
    }
    if &s[4..5] != "-" || &s[7..8] != "-" {
        return None;
    }

    // Numeric parsing
    let y = s[0..4].parse::<u32>().ok()?;
    let m = s[5..7].parse::<u32>().ok()?;
    let d = s[8..10].parse::<u32>().ok()?;

    // Range validation
    if m < 1 || m > 12 {
        return None;
    }
    let max_day = days_in_month(y, m);
    if d < 1 || d > max_day {
        return None;
    }

    Some((y, m, d))
}

fn main() {
    let mut input = String::new();

    loop {
        print!("Enter date (YYYY-MM-DD), or blank to quit: ");
        io::stdout().flush().unwrap();

        input.clear();
        if io::stdin().read_line(&mut input).is_err() {
            eprintln!("Error reading input; exiting.");
            break;
        }

        let s = input.trim();
        if s.is_empty() {
            break;
        }

        match parse_date(s) {
            Some((y, m, d)) => println!("→ OK: parsed as {}-{:02}-{:02}\n", y, m, d),
            None => println!("→ Error: '{}' is not a valid YYYY-MM-DD\n", s),
        }
    }

    println!("Exiting!");
}

#[cfg(test)]
mod tests {
    use super::{days_in_month, parse_date};
    use proptest::prelude::*;
    use proptest::string::string_regex;
    use proptest::test_runner::{Config, FileFailurePersistence, TestRunner};
    use std::cell::Cell;

    // Property-based tests: 10 cases each, no shrinking
    proptest! {
        #![proptest_config(ProptestConfig {
            cases: 10,
            max_shrink_iters: 0,
            .. ProptestConfig::default()
        })]

        /// 1) Numeric triplets: check valid vs. invalid days per month
        #[test]
        fn test_1_numeric_dates(
            y in 0u32..10000,
            m in 1u32..13,
            d in 1u32..32,
        ) {
            let date_str = format!("{:04}-{:02}-{:02}", y, m, d);
            println!("[numeric_dates] trying {}", date_str);

            let expected = if d <= days_in_month(y, m) {
                Some((y, m, d))
            } else {
                None
            };

            prop_assert_eq!(parse_date(&date_str), expected);
        }

        /// 2) Garbage or malformed strings must never panic and always return `None`
        #[test]
        fn test_2_invalid_strings_never_panics_and_returns_none(
            s in prop_oneof![
                // Exactly-10 chars that are neither digit nor hyphen
                string_regex(r"[^\d-]{10}").unwrap().boxed(),
                // Any other sequence of non-control chars
                "\\PC*".prop_map(|s| s).boxed(),
            ]
        ) {
            println!("[invalid] {:?} → {:?}", s, parse_date(&s));
            prop_assert_eq!(parse_date(&s), None);
        }
    }

    /// 3) Manual invalid cases grouped into one test
    #[test]
    fn test_3_manual_invalid_cases() {
        let cases = [
            ("2025-04-31", "April-31 edge"),
            ("2025-13-01", "Month out of range"),
            ("2025-01-00", "Day zero"),
            ("2025/02/28", "Wrong separator"),
            ("20250228", "Missing hyphens"),
            ("abcd-ef-gh", "Non-digits"),
        ];

        for (input, desc) in &cases {
            let parsed = parse_date(input);
            println!("[{}] parse_date({}) = {:?}", desc, input, parsed);
            assert_eq!(parsed, None, "{} should be invalid, got {:?}", desc, parsed);
        }
    }

    /// 4) Demo: run 20 random cases and log pass/fail with summary
    #[test]
    fn demo_4_numeric_dates_full_log() {
        let mut runner = TestRunner::new(Config {
            cases: 20,
            max_shrink_iters: 0,
            failure_persistence: Some(Box::new(FileFailurePersistence::Off)),
            .. Config::default()
        });

        let strat = (0u32..10000, 0u32..15, 0u32..35);

        let pass_count = Cell::new(0);
        let fail_count = Cell::new(0);

        runner
            .run(&strat, |(y, m, d)| {
                let date_str = format!("{:04}-{:02}-{:02}", y, m, d);
                if parse_date(&date_str).is_some() {
                    pass_count.set(pass_count.get() + 1);
                    println!("[pass] {}", date_str);
                } else {
                    fail_count.set(fail_count.get() + 1);
                    println!("[FAIL] {}", date_str);
                }
                Ok(())
            })
            .unwrap();

        println!(
            "\nSummary: {} passed, {} failed",
            pass_count.get(),
            fail_count.get()
        );
    }
}
