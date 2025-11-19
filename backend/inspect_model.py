import joblib
import os

# Load and inspect the model
model_path = os.path.join(os.path.dirname(__file__), 'best_model.pkl')
try:
    model = joblib.load(model_path)
    print("Model type:", type(model))
    print("Model:", model)
    
    # Check if it's a pipeline
    if hasattr(model, 'named_steps'):
        print("\nPipeline steps:")
        for name, step in model.named_steps.items():
            print(f"  {name}: {type(step)}")
    
    # Check for attributes
    if hasattr(model, 'classes_'):
        print("\nClasses:", model.classes_)
    
except Exception as e:
    print(f"Error loading model: {e}")
