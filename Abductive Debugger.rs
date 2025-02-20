use regex::Regex;
use std::collections::HashMap;

#[derive(Debug)]
struct DebugRule {
    pattern: String,
    probable_cause: String,
    confidence: f64, // Bayesian confidence score
}

struct RuleStats {
    hits: u32,
    total_checks: u32,
}

struct Debugger {
    rules: Vec<DebugRule>,
    knowledge_base: HashMap<String, RuleStats>, // Tracks rule performance
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
            confidence: 0.5, // Initial prior probability
        });
    }

    fn preprocess_log(log: &str) -> String {
        // NLP-inspired preprocessing
        let log = log.to_lowercase();
        let re = Regex::new(r"[^\w\s]").unwrap();
        re.replace_all(&log, "").to_string()
    }

    fn analyze_log(&mut self, log: &str) -> Option<String> {
        let processed_log = Self::preprocess_log(log);
        let mut best_match: Option<&DebugRule> = None;

        for rule in &mut self.rules {
            let re = Regex::new(&rule.pattern).unwrap();
            let matches = re.is_match(&processed_log);
            
            let stats = self.knowledge_base
                .entry(rule.pattern.clone())
                .or_insert(RuleStats { hits: 0, total_checks: 0 });
            
            stats.total_checks += 1;
            
            if matches {
                stats.hits += 1;
                // Bayesian update with pseudocounts (alpha=1, beta=1)
                let alpha = 1.0;
                let beta = 1.0;
                rule.confidence = (stats.hits as f64 + alpha) / (stats.total_checks as f64 + alpha + beta);
                
                // Update best match if higher confidence
                if best_match.map(|r| r.confidence < rule.confidence).unwrap_or(true) {
                    best_match = Some(rule);
                }
            } else {
                // Update confidence even when no match
                let alpha = 1.0;
                let beta = 1.0;
                rule.confidence = (stats.hits as f64 + alpha) / (stats.total_checks as f64 + alpha + beta);
            }
        }

        best_match.map(|rule| {
            format!(
                "Probable Cause: {} (Confidence: {:.2})",
                rule.probable_cause, rule.confidence
            )
        })
    }
}

fn main() {
    let mut debugger = Debugger::new();
    
    // Updated patterns to match preprocessed logs
    debugger.add_rule(r"panic at line \d+", "Segmentation fault or memory issue");
    debugger.add_rule(r"missing field \w+", "Struct field missing in Rust code");
    debugger.add_rule(r"expected type \w+", "Type mismatch error");
    debugger.add_rule(r"undefined function \w+", "Function not declared or out of scope");
    
    let logs = vec![
        "PANIC! at line 42",
        "missing field `username`",
        "Expected type `String`, found `i32`",
        "undefined function 'calculate'"
    ];

    for log in logs {
        if let Some(result) = debugger.analyze_log(log) {
            println!("Log: {}\n-> {}\n", log, result);
        } else {
            println!("No matching rule found for: {}\n", log);
        }
    }
}