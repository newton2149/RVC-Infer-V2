from pydantic import BaseModel
from typing import Optional


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
    gpu: int
    pitch_guidance: bool
    pretrained: bool
    custom_pretrained: bool
    g_pretrained_path: Optional[str] = None
    d_pretrained_path: Optional[str] = None
    
class TrainRequest(BaseModel):
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
    input_path:Optional[str] = None  
    output_path: Optional[str] = None
    pth_path:Optional[str] = None
    index_path:Optional[str] = None
    split_audio:bool
    f0autotune:bool
    clean_audio:bool
    clean_strength:float
    export_format:str
    
    
class InputRequest(BaseModel):
    f0up_key: int
    filter_radius: int
    index_rate : float
    rms_mix_rate:float
    protect : float
    hop_length: int
    f0method:str
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
    output_folder: Optional[str] = None
    pth_path:Optional[str] = None
    index_path:Optional[str] = None
    split_audio:bool
    f0autotune:bool
    clean_audio:bool
    clean_strength:float
    export_format:str

class BatchRequest(BaseModel):
    f0up_key: int
    filter_radius: int
    index_rate : float
    rms_mix_rate:float
    protect : float
    hop_length: int
    f0method:str
    input_folder:str
    split_audio:bool
    f0autotune:bool
    clean_audio:bool
    clean_strength:float
    export_format:str