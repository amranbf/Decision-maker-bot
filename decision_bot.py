from decision import Decision
from analyzer import Analyzer
import json
import os

class DecisionBot:
    
    def __init__(self):
        self.analyzer = Analyzer()
        self.current_decision = None
        self.history_file = "data/decisions.json"
        self._load_history()
    
    def create_decision(self, question, options):
        self.current_decision = Decision(question, options)
        return self.current_decision
    
    def add_factor(self, factor_name, importance):
        if self.current_decision:
            self.current_decision.add_factor(factor_name, importance)
    
    def add_rating(self, option, factor, rating):
        if self.current_decision:
            self.current_decision.add_rating(option, factor, rating)
    
    def analyze(self):
        if not self.current_decision:
            return None
        
        analysis = self.analyzer.analyze_decision(self.current_decision)
        self.analyzer.add_to_history(self.current_decision, analysis)
        self._save_decision()
        
        return analysis
    
    def get_formatted_analysis(self, analysis):
        if not analysis:
            return "No analysis available"
        
        report = []
        report.append(f"\n{'='*50}")
        report.append("DECISION ANALYSIS REPORT")
        report.append(f"{'='*50}\n")
        
        report.append("SCORES:")
        for option, score in analysis['scores'].items():
            report.append(f"  {option}: {score} points")
        
        report.append(f"\nRECOMMENDED OPTION: {analysis['recommended']}")
        report.append(f"CONFIDENCE LEVEL: {analysis['confidence']}%")
        
        if analysis['is_close_call']:
            report.append("\n⚠️  CLOSE CALL: Top options are very similar!")
        
        report.append(f"\nKEY FACTORS: {', '.join(analysis['key_factors'])}")
        
        if analysis['warnings']:
            report.append("\n⚠️  WARNINGS:")
            for warning in analysis['warnings']:
                report.append(f"  - {warning}")
        
        report.append(f"\n{'='*50}\n")
        
        return '\n'.join(report)
    
    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                 data = json.load(f)
                self.analyzer.past_decisions = data
            except:
             pass

    def _save_decision(self):
        os.makedirs("data", exist_ok=True)
        
        with open(self.history_file, 'w') as f:
            json.dump(self.analyzer.past_decisions, f, indent=2)
    
    def get_history(self):
        return self.analyzer.past_decisions
    
    def get_statistics(self):
        return self.analyzer.get_statistics()    