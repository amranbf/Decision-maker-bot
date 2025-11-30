class Decision:
    
    def __init__(self, question, options):
        """
        Initialize a decision
        question: str - The decision question (e.g., "Which job should I take?")
        options: list - List of option names (e.g., ["Job A", "Job B"])
        """
        self.question = question
        self.options = options
        self.factors = {}  # Dictionary: {factor_name: importance_weight}
        self.ratings = {}  # Dictionary: {option: {factor: rating}}
        self.analysis_result = None
        
    def add_factor(self, factor_name, importance):
        """Add a factor with importance weight (1-10)"""
        self.factors[factor_name] = importance
        
    def add_rating(self, option, factor, rating):
        """Rate an option for a specific factor (1-10)"""
        if option not in self.ratings:
            self.ratings[option] = {}
        self.ratings[option][factor] = rating
        
    def get_option_score(self, option):
        """Calculate weighted score for an option"""
        if option not in self.ratings:
            return 0
        
        total_score = 0
        for factor, rating in self.ratings[option].items():
            importance = self.factors.get(factor, 1)
            total_score += rating * importance
            
        return total_score
    
    def __str__(self):
        """String representation of the decision"""
        return f"Decision: {self.question} | Options: {', '.join(self.options)}" 