use std::collections::HashMap;

#[derive(Debug, Clone)]
struct DebugRule {
    cause: String,
    effect: String,
}

struct AbductiveDebugger {
    rules: Vec<DebugRule>,
}

impl AbductiveDebugger {
    fn new() -> Self {
        AbductiveDebugger { rules: Vec::new() }
    }

    fn add_rule(&mut self, cause: &str, effect: &str) {
        self.rules.push(DebugRule {
            cause: cause.to_string(),
            effect: effect.to_string(),
        });
    }

    fn infer_cause(&self, observed_effect: &str) -> Option<String> {
        for rule in &self.rules {
            if rule.effect == observed_effect {
                return Some(rule.cause.clone());
            }
        }
        None
    }
}

fn main() {
    let mut debugger = AbductiveDebugger::new();
    
    // Example: Adding some debugging rules
    debugger.add_rule("Uninitialized variable", "Segmentation fault");
    debugger.add_rule("Missing function call", "Undefined symbol");
    
    // Example: Inferring the cause of an error
    if let Some(cause) = debugger.infer_cause("Segmentation fault") {
        println!("Possible cause: {}", cause);
    } else {
        println!("No known cause found.");
    }
}
