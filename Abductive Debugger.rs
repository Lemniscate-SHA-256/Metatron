use std::collections::HashMap;

#[derive(Debug, Clone)]
struct DebugRule {
    pattern: String,          // Error message pattern
    probable_cause: String,  // Suggested cause
    confidence: f32,         // Confidence score (evolves over time)
}

struct Debugger {
    rules: Vec<DebugRule>,
    knowledge_base: HashMap<String, f32>, // Tracks known errors & probabilities
}

impl Debugger {
    fn new() -> Self {
        Self {
            rules: vec![
                DebugRule {
                    pattern: "Segmentation fault".to_string(),
                    probable_cause: "Possible uninitialized variable or memory corruption".to_string(),
                    confidence: 0.8,
                },
                DebugRule {
                    pattern: "IndexError".to_string(),
                    probable_cause: "Out-of-bounds array access".to_string(),
                    confidence: 0.9,
                },
            ],
            knowledge_base: HashMap::new(),
        }
    }

    fn analyze_error(&mut self, error_message: &str) -> Option<&DebugRule> {
        let mut best_match: Option<&DebugRule> = None;
        let mut highest_confidence = 0.0;

        for rule in &self.rules {
            if error_message.contains(&rule.pattern) {
                if rule.confidence > highest_confidence {
                    highest_confidence = rule.confidence;
                    best_match = Some(rule);
                }
            }
        }
        best_match
    }

    fn update_knowledge(&mut self, error: &str, confirmed_cause: &str) {
        let entry = self.knowledge_base.entry(error.to_string()).or_insert(0.5);
        *entry = (*entry + 1.0) / 2.0; // Simple confidence update (evolves with feedback)
        println!("Updated knowledge base: {:?}", self.knowledge_base);
    }
}

fn main() {
    let mut debugger = Debugger::new();
    let test_error = "Segmentation fault when accessing array";

    if let Some(rule) = debugger.analyze_error(test_error) {
        println!("Possible cause: {} (Confidence: {:.2})", rule.probable_cause, rule.confidence);
        debugger.update_knowledge(test_error, &rule.probable_cause);
    } else {
        println!("No matching rule found. Suggest adding this case to the system.");
    }
}
