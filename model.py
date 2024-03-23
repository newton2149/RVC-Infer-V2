from pydantic import BaseModel


#Train V2
class TrainInputData(BaseModel):
    model_name: str
    rvc_version: str
    save_every_epoch: bool
    save_only_latest: bool
    save_every_weights: bool
    total_epoch: int
    sampling_rate: int
    batch_size: int
    gpu: str
    pitch_guidance: bool
    pretrained: bool
    custom_pretrained: bool
    g_pretrained_path: str
    d_pretrained_path: str
    
    
class IndexInputData(BaseModel):
    model_name: str
    rvc_version: str
    
    

class PreprocessInputData(BaseModel):
    model_name: str
    dataset_path: str
    sampling_rate: int

class ExtractInputData(BaseModel):
    model_name: str
    rvc_version: str
    f0method: str
    hop_length: int
    sampling_rate: int
    

#Infer V2

class InputData(BaseModel):
    f0up_key: int
    filter_radius: int
    index_rate : float
    rms_mix_rate:float
    protect : float
    hop_length: int
    f0method:str
    input_path:str
    output_path:str
    pth_path:str
    index_path:str
    split_audio:bool
    f0autotune:bool
    clean_audio:bool
    clean_strength:float
    export_format:str

class BatchInputData(BaseModel):
    f0up_key: int
    filter_radius: int
    index_rate : float
    rms_mix_rate:float
    protect : float
    hop_length: int
    f0method:str
    input_folder:str
    output_folder:str
    pth_path:str
    index_path:str
    split_audio:bool
    f0autotune:bool
    clean_audio:bool
    clean_strength:float
    export_format:str
