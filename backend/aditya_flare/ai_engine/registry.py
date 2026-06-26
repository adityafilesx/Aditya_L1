import mlflow
import mlflow.pytorch
import torch
import os

class ModelRegistry:
    """
    Handles logging, saving, and loading models using MLFlow.
    """
    def __init__(self, experiment_name="Aditya_L1_Temporal_AI", tracking_uri="file:./mlruns"):
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        
    def start_run(self, run_name=None):
        return mlflow.start_run(run_name=run_name)
        
    def log_params(self, params):
        mlflow.log_params(params)
        
    def log_metrics(self, metrics, step=None):
        mlflow.log_metrics(metrics, step=step)
        
    def log_model(self, model, artifact_path="model"):
        """ Logs the model to the current run """
        mlflow.pytorch.log_model(model, artifact_path)
        
    def load_model(self, run_id, artifact_path="model"):
        """ Loads a model from a specific run """
        model_uri = f"runs:/{run_id}/{artifact_path}"
        return mlflow.pytorch.load_model(model_uri)
        
    def save_local_checkpoint(self, model, optimizer, epoch, path="checkpoint.pth"):
        """ Simple local checkpoint saving as fallback """
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
        }, path)
        
    def load_local_checkpoint(self, model, optimizer, path="checkpoint.pth"):
        if os.path.exists(path):
            checkpoint = torch.load(path)
            model.load_state_dict(checkpoint['model_state_dict'])
            if optimizer is not None:
                optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            return checkpoint['epoch']
        return 0
