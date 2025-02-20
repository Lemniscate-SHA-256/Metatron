use regex::Regex;
use std::collections::HashMap;

#[derive(Debug)]
struct DebugRule {
    pattern: String,
    probable_cause: String,
    confidence: f64, // Adaptive learning score
}

struct Debugger {
    rules: Vec<DebugRule>,
    knowledge_base: HashMap<String, f64>, // Error tracking
}

impl Debugger {
    fn new() -> Self {
        Debugger {
            rules: vec![],
            knowledge_base: HashMap::new(),
        }
    }

    fn add_rule(&mut self, pattern: &str, cause: &str) {
        self.rules.push(DebugRule {
            pattern: pattern.to_string(),
            probable_cause: cause.to_string(),
            confidence: 1.0,
        });
    }

    fn analyze_log(&mut self, log: &str) -> Option<String> {
        for rule in &mut self.rules {
            let re = Regex::new(&rule.pattern).unwrap();
            if re.is_match(log) {
                // Adjust confidence dynamically
                let entry = self.knowledge_base.entry(rule.pattern.clone()).or_insert(1.0);
                *entry = (*entry + 1.0) / 2.0; // Bayesian-style update
                rule.confidence = *entry; // Update confidence in rule

                return Some(format!(
                    "Possible Cause: {} (Confidence: {:.2})",
                    rule.probable_cause, rule.confidence
                ));
            }
        }
        None
    }
}

fn main() {
    let mut debugger = Debugger::new();
    
    // Add regex patterns for error detection
    debugger.add_rule(r"panic! at line (\d+)", "Possible segmentation fault or memory issue.");
    debugger.add_rule(r"missing field `(.*?)`", "Struct field might be missing in Rust code.");
    debugger.add_rule(r"expected type `(.*?)`", "Type mismatch error, check variable types.");
    
    // Example error logs
    let logs = vec![
        "panic! at line 42", 
        "missing field `username`", 
        "expected type `String`, found `int`"
    ];

    for log in logs {
        if let Some(result) = debugger.analyze_log(log) {
            println!("Log: {}\n-> {}\n", log, result);
        } else {
            println!("No matching rule found for: {}\n", log);
        }
    }
}
