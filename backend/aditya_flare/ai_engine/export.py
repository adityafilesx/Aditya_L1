import torch

def export_to_torchscript(model, example_inputs, save_path="model_traced.pt"):
    """
    Exports the PyTorch model to TorchScript using tracing.
    example_inputs should be a tuple: (sxr_x, hxr_x, physics_x)
    """
    model.eval()
    with torch.no_grad():
        traced_model = torch.jit.trace(model, example_inputs)
        traced_model.save(save_path)
    print(f"Model successfully exported to TorchScript at {save_path}")
    return traced_model

def export_to_onnx(model, example_inputs, save_path="model.onnx"):
    """
    Exports the PyTorch model to ONNX format.
    example_inputs should be a tuple: (sxr_x, hxr_x, physics_x)
    """
    model.eval()
    
    # Optional dynamic axes for variable batch sizes or sequence lengths
    dynamic_axes = {
        'sxr_input': {0: 'batch_size', 1: 'seq_len'},
        'hxr_input': {0: 'batch_size', 1: 'seq_len'},
        'physics_input': {0: 'batch_size', 1: 'seq_len'},
        'prob_output': {0: 'batch_size'},
        'flux_output': {0: 'batch_size'},
        'class_output': {0: 'batch_size'}
    }
    
    with torch.no_grad():
        torch.onnx.export(
            model,
            example_inputs,
            save_path,
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=['sxr_input', 'hxr_input', 'physics_input'],
            output_names=['prob_output', 'flux_output', 'class_output'],
            dynamic_axes=dynamic_axes
        )
    print(f"Model successfully exported to ONNX at {save_path}")
