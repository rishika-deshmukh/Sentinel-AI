import numpy as np
import shap
from app.ml.feature_pipeline import FEATURE_ORDER

class ModelExplainer:
    def __init__(self, model, background_data: np.ndarray):
        # Using TreeExplainer for Isolation Forest
        self.explainer = shap.TreeExplainer(model, background_data[:100])

    def explain(self, sample: np.ndarray) -> dict[str, float]:
        shap_values = self.explainer.shap_values(sample)
        # Handle 1D or 2D array output from shap
        vals = shap_values[0] if len(shap_values.shape) > 1 else shap_values
        
        attribution = {}
        for idx, col in enumerate(FEATURE_ORDER):
            attribution[col] = round(float(vals[idx]), 4)
            
        return attribution