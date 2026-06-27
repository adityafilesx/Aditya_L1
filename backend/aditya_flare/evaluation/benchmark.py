from backend.aditya_flare.evaluation.metrics import compute_all_metrics

class BenchmarkSuite:
    def __init__(self):
        self.models = {}
        self.results = {}
        
    def add_model(self, name: str, y_true, y_prob):
        self.models[name] = (y_true, y_prob)
        
    def run_benchmarks(self):
        for name, (y_true, y_prob) in self.models.items():
            self.results[name] = compute_all_metrics(y_true, y_prob)
        return self.results
