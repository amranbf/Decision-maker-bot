class Analyzer:
    
    def __init__(self):
        self.past_decisions = []
    
    def analyze_decision(self, decision):
        analysis = {}
        
        scores = {}
        for option in decision.options:
            scores[option] = decision.get_option_score(option)
        
        analysis['scores'] = scores
        analysis['recommended'] = max(scores, key=scores.get) if scores else None
        analysis['highest_score'] = max(scores.values()) if scores else 0
        analysis['confidence'] = self._calculate_confidence(scores)
        analysis['key_factors'] = self._get_key_factors(decision)
        analysis['is_close_call'] = self._is_close_call(scores)
        analysis['warnings'] = self._check_biases(decision, scores)
        
        return analysis
    
    def _calculate_confidence(self, scores):
        if not scores or len(scores) < 2:
            return 0
        
        score_list = list(scores.values())
        max_score = max(score_list)
        min_score = min(score_list)
        
        if max_score == 0:
            return 0
        
        spread = max_score - min_score
        confidence = min(100, (spread / max_score) * 100)
        
        return round(confidence, 2)
    
    def _get_key_factors(self, decision):
        sorted_factors = sorted(decision.factors.items(), 
                               key=lambda x: x[1], 
                               reverse=True)
        
        top_factors = [factor[0] for factor in sorted_factors[:3]]
        
        return top_factors
    
    def _is_close_call(self, scores):
        if len(scores) < 2:
            return False
        
        sorted_scores = sorted(scores.values(), reverse=True)
        
        if sorted_scores[0] > 0:
            difference_percent = ((sorted_scores[0] - sorted_scores[1]) / sorted_scores[0]) * 100
            return difference_percent < 10
        
        return False
    
    def _check_biases(self, decision, scores):
        warnings = []
        
        all_ratings = []
        for option_ratings in decision.ratings.values():
            all_ratings.extend(option_ratings.values())
        
        if all_ratings and len(set(all_ratings)) == 1:
            warnings.append("All ratings are identical - consider differentiating more")
        
        if decision.factors:
            importance_values = list(decision.factors.values())
            if len(set(importance_values)) == 1:
                warnings.append("All factors have same importance - consider prioritizing")
        
        if scores:
            max_score = max(scores.values())
            min_score = min(scores.values())
            if min_score == 0 and max_score > 0:
                warnings.append("One option scored 0 - is it really being considered?")
        
        return warnings
    
    def add_to_history(self, decision, analysis):
        self.past_decisions.append({
            'question': decision.question,
            'options': decision.options,
            'chosen': analysis['recommended'],
            'confidence': analysis['confidence']
        })
    
    def get_statistics(self):
        if not self.past_decisions:
            return "No past decisions to analyze"
        
        total = len(self.past_decisions)
        avg_confidence = sum(d['confidence'] for d in self.past_decisions) / total
        
        return {
            'total_decisions': total,
            'average_confidence': round(avg_confidence, 2)
        }