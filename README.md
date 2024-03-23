## RVC_CLI: Retrieval-based Voice Conversion Command Line Interface



### Installation

Ensure that you have the necessary Python packages installed by following these steps (Python 3.9 is recommended):

#### Windows

Execute the [install.bat](./install.bat) file to activate a Conda environment. Afterward, launch the application using `env/python main.py` instead of the conventional `python main.py` command.

#### Linux

```bash
chmod +x install.sh
./install.sh
```

### Inference

#### Single Inference

```bash
python3 inferV2.py infer --f0up_key 12 --filter_radius 0 --index_rate 0.0 --hop_length 100 --rms_mix_rate 0.0 --protect 0.5  --f0autotune True --f0method rmvpe --input_path ./test-wavs/LJ001-0001.wav --output_path ./utput/test.wav --pth_path "./logs/models/weights/lj-ten.pth"  --index_path "./logs/models/weights/lj-ten.pth" --split_audio True --clean_audio True --clean_strength 0.7 --export_format WAV
```

| Parameter Name   | Required | Default | Valid Options                                                                                                                           | Description                                                                                                                                                                                                                                                                                                           |
| ---------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `f0up_key`       | No       | 0       | -24 to +24                                                                                                                              | Set the pitch of the audio, the higher the value, thehigher the pitch.                                                                                                                                                                                                                                                |
| `filter_radius`  | No       | 3       | 0 to 10                                                                                                                                 | If the number is greater than or equal to three, employing median filtering on the collected tone results has the potential to decrease respiration.                                                                                                                                                                  |
| `index_rate`     | No       | 0.3     | 0.0 to 1.0                                                                                                                              | Influence exerted by the index file; a higher value corresponds to greater influence. However, opting for lower values can help mitigate artifacts present in the audio.                                                                                                                                              |
| `hop_length`     | No       | 128     | 1 to 512                                                                                                                                | Denotes the duration it takes for the system to transition to a significant pitch change. Smaller hop lengths require more time for inference but tend to yield higher pitch accuracy.                                                                                                                                |
| `rms_mix_rate`   | No       | 1       | 0 to 1                                                                                                                                  | Substitute or blend with the volume envelope of the output. The closer the ratio is to 1, the more the output envelope is employed.                                                                                                                                                                                   |
| `protect`        | No       | 0.33    | 0 to 0.5                                                                                                                                | Safeguard distinct consonants and breathing sounds to prevent electro-acoustic tearing and other artifacts. Pulling the parameter to its maximum value of 0.5 offers comprehensive protection. However, reducing this value might decrease the extent of protection while potentially mitigating the indexing effect. |
| `f0autotune`     | No       | False   | True or False                                                                                                                           | Apply a soft autotune to your inferences, recommended for singing conversions.                                                                                                                                                                                                                                        |
| `f0method`       | No       | rmvpe   | pm, harvest, dio, crepe, crepe-tiny, rmvpe, fcpe, hybrid[crepe+rmvpe], hybrid[crepe+fcpe], hybrid[rmvpe+fcpe], hybrid[crepe+rmvpe+fcpe] | Pitch extraction algorithm to use for the audio conversion. The default algorithm is rmvpe, which is recommended for most cases.                                                                                                                                                                                      |
| `input_path`     | Yes      |         | Full path to the input audio file                                                                                                       | Full path to the input audio file                                                                                                                                                                                                                                                                                     |
| `output_path`    | Yes      |         | Full path to the output audio file                                                                                                      | Full path to the output audio file                                                                                                                                                                                                                                                                                    |
| `pth_path`       | Yes      |         | Full path to the pth file                                                                                                               | Full path to the pth file                                                                                                                                                                                                                                                                                             |
| `index_path`     | Yes      |         | Full index file path                                                                                                                    | Full index file path                                                                                                                                                                                                                                                                                                  |
| `split_audio`    | No       | False   | True or False                                                                                                                           | Split the audio into chunks for inference to obtain better results in some cases.                                                                                                                                                                                                                                     |
| `clean_audio`    | No       | False   | True or False                                                                                                                           | Clean your audio output using noise detection algorithms, recommended for speaking audios.                                                                                                                                                                                                                            |
| `clean_strength` | No       | 0.7     | 0.0 to 1.0                                                                                                                              | Set the clean-up level to the audio you want, the more you increase it the more it will clean up, but it is possible that the audio will be more compressed.                                                                                                                                                          |
| `export_format`  | No       | WAV     | WAV, MP3, FLAC, OGG, M4A                                                                                                                | File audio format                                                                                                                                                                                                                                                                                                     |
#### Batch Inference

```bash
python main.py batch_infer --f0up_key 12 --filter_radius 0 --index_rate 0.0 --hop_length 100 --rms_mix_rate 0.0 --protect 0.5 --f0autotune True --f0method rmvpe --input_folder_path ./test-wavs/ --output_folder_path ./output/results --pth_path "./logs/models/weights/lj-ten.pth" --index_path "./logs/models/weights/lj-ten.pth" --split_audio True --clean_audio True --clean_strength 0.7 --export_format WAV
```

| Parameter Name       | Required | Default | Valid Options                                                                                                                           | Description                                                                                                                                                                                                                                                                                                           |
| -------------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `f0up_key`           | No       | 0       | -24 to +24                                                                                                                              | Set the pitch of the audio, the higher the value, thehigher the pitch.                                                                                                                                                                                                                                                |
| `filter_radius`      | No       | 3       | 0 to 10                                                                                                                                 | If the number is greater than or equal to three, employing median filtering on the collected tone results has the potential to decrease respiration.                                                                                                                                                                  |
| `index_rate`         | No       | 0.3     | 0.0 to 1.0                                                                                                                              | Influence exerted by the index file; a higher value corresponds to greater influence. However, opting for lower values can help mitigate artifacts present in the audio.                                                                                                                                              |
| `hop_length`         | No       | 128     | 1 to 512                                                                                                                                | Denotes the duration it takes for the system to transition to a significant pitch change. Smaller hop lengths require more time for inference but tend to yield higher pitch accuracy.                                                                                                                                |
| `rms_mix_rate`       | No       | 1       | 0 to 1                                                                                                                                  | Substitute or blend with the volume envelope of the output. The closer the ratio is to 1, the more the output envelope is employed.                                                                                                                                                                                   |
| `protect`            | No       | 0.33    | 0 to 0.5                                                                                                                                | Safeguard distinct consonants and breathing sounds to prevent electro-acoustic tearing and other artifacts. Pulling the parameter to its maximum value of 0.5 offers comprehensive protection. However, reducing this value might decrease the extent of protection while potentially mitigating the indexing effect. |
| `f0autotune`         | No       | False   | True or False                                                                                                                           | Apply a soft autotune to your inferences, recommended for singing conversions.                                                                                                                                                                                                                                        |
| `f0method`           | No       | rmvpe   | pm, harvest, dio, crepe, crepe-tiny, rmvpe, fcpe, hybrid[crepe+rmvpe], hybrid[crepe+fcpe], hybrid[rmvpe+fcpe], hybrid[crepe+rmvpe+fcpe] | Pitch extraction algorithm to use for the audio conversion. The default algorithm is rmvpe, which is recommended for most cases.                                                                                                                                                                                      |
| `input_folder_path`  | Yes      |         | Full path to the input audio folder (The folder may only contain audio files)                                                           | Full path to the input audio folder                                                                                                                                                                                                                                                                                   |
| `output_folder_path` | Yes      |         | Full path to the output audio folder                                                                                                    | Full path to the output audio folder                                                                                                                                                                                                                                                                                  |
| `pth_path`           | Yes      |         | Full path to the pth file                                                                                                               | Full path to the pth file                                                                                                                                                                                                                                                                                             |
| `index_path`         | Yes      |         | Full path to the index file                                                                                                             | Full path to the index file                                                                                                                                                                                                                                                                                           |
| `split_audio`        | No       | False   | True or False                                                                                                                           | Split the audio into chunks for inference to obtain better results in some cases.                                                                                                                                                                                                                                     |
| `clean_audio`        | No       | False   | True or False                                                                                                                           | Clean your audio output using noise detection algorithms, recommended for speaking audios.                                                                                                                                                                                                                            |
| `clean_strength`     | No       | 0.7     | 0.0 to 1.0                                                                                                                              | Set the clean-up level to the audio you want, the more you increase it the more it will clean up, but it is possible that the audio will be more compressed.                                                                                                                                                          |
| `export_format`      | No       | WAV     | WAV, MP3, FLAC, OGG, M4A                                                                                                                | File audio format                                                                                                                                                                                                                                                                                                     |



### Training

#### Preprocess Dataset

```bash
python trainv2.py preprocess --model_name "lj-ten" --dataset_path ./test-wavs --sampling_rate 48000
```

| Parameter Name  | Required | Default | Valid Options                                                             | Description                     |
| --------------- | -------- | ------- | ------------------------------------------------------------------------- | ------------------------------- |
| `model_name`    | Yes      |         | Name of the model                                                         | Name of the model               |
| `dataset_path`  | Yes      |         | Full path to the dataset folder (The folder may only contain audio files) | Full path to the dataset folder |
| `sampling_rate` | Yes      |         | 32000, 40000, or 48000                                                    | Sampling rate of the audio data |

_Refer to `python main.py preprocess -h` for additional help._

#### Extract Features

```bash
python trainv2.py extract --model_name "lj-ten" --rvc_version "v2" --f0method rmvpe --hop_length 100 --sampling_rate 48000
```

| Parameter Name  | Required | Default | Valid Options                              | Description                                                                                                                                                                            |
| --------------- | -------- | ------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model_name`    | Yes      |         | Name of the model                          | Name of the model                                                                                                                                                                      |
| `rvc_version`   | No       | v2      | v1 or v2                                   | Version of the model                                                                                                                                                                   |
| `f0method`      | No       | rmvpe   | pm, harvest, dio, crepe, crepe-tiny, rmvpe | Pitch extraction algorithm to use for the audio conversion. The default algorithm is rmvpe, which is recommended for most cases.                                                       |
| `hop_length`    | No       | 128     | 1 to 512                                   | Denotes the duration it takes for the system to transition to a significant pitch change. Smaller hop lengths require more time for inference but tend to yield higher pitch accuracy. |
| `sampling_rate` | Yes      |         | 32000, 40000, or 48000                     | Sampling rate of the audio data                                                                                                                                                        |

#### Start Training

```bash
python trainv2.py train --model_name lj-ten --rvc_version v2 --save_every_epoch 20 --save_only_latest True --save_every_weights False --total_epoch 100 --sampling_rate 48000 --batch_size 16 --gpu 0 --pitch_guidance True --pretrained True --custom_pretrained True [--g_pretrained ./pretraineds/pretrained_v2/G48k.pth ] [--d_pretrained ./pretraineds/pretrained_v2/D48k.pth]
```

| Parameter Name       | Required | Default | Valid Options                                                           | Description                                                                                                                                                                                                                                                     |
| -------------------- | -------- | ------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model_name`         | Yes      |         | Name of the model                                                       | Name of the model                                                                                                                                                                                                                                               |
| `rvc_version`        | No       | v2      | v1 or v2                                                                | Version of the model                                                                                                                                                                                                                                            |
| `save_every_epoch`   | Yes      |         | 1 to 50                                                                 | Determine at how many epochs the model will saved at.                                                                                                                                                                                                           |
| `save_only_latest`   | No       | False   | True or False                                                           | Enabling this setting will result in the G and D files saving only their most recent versions, effectively conserving storage space.                                                                                                                            |
|                      |
| `save_every_weights` | No       | True    | True or False                                                           | This setting enables you to save the weights of the model at the conclusion of each epoch.                                                                                                                                                                      |
|                      |
| `total_epoch`        | No       | 1000    | 1 to 10000                                                              | Specifies the overall quantity of epochs for the model training process.                                                                                                                                                                                        |
|                      |
| `sampling_rate`      | Yes      |         | 32000, 40000, or 48000                                                  | Sampling rate of the audio data                                                                                                                                                                                                                                 |
| `batch_size`         | No       | 8       | 1 to 50                                                                 | It's advisable to align it with the available VRAM of your GPU. A setting of 4 offers improved accuracy but slower processing, while 8 provides faster and standard results.                                                                                    |
| `gpu`                | No       | 0       | 0 to ∞ separated by -                                                   | Specify the number of GPUs you wish to utilize for training by entering them separated by hyphens (-).                                                                                                                                                          |
|                      |
| `pitch_guidance`     | No       | True    | True or False                                                           | By employing pitch guidance, it becomes feasible to mirror the intonation of the original voice, including its pitch. This feature is particularly valuable for singing and other scenarios where preserving the original melody or pitch pattern is essential. |
|                      |
| `pretrained`         | No       | True    | True or False                                                           | Utilize pretrained models when training your own. This approach reduces training duration and enhances overall quality.                                                                                                                                         |
|                      |
| `custom_pretrained`  | No       | False   | True or False                                                           | Utilizing custom pretrained models can lead to superior results, as selecting the most suitable pretrained models tailored to the specific use case can significantly enhance performance.                                                                      |
| `g_pretrained`       | No       | None    | Full path to pretrained file G, only if you have used custom_pretrained | Full path to pretrained file G                                                                                                                                                                                                                                  |
| `d_pretrained`       | No       | None    | Full path to pretrained file D, only if you have used custom_pretrained | Full path to pretrained file D                                                                                                                                                                                                                                  |

#### Generate Index File

```bash
python trainv2 index --model_name "lj-ten" --rvc_version "v2"
```

| Parameter Name | Required | Default | Valid Options     | Description          |
| -------------- | -------- | ------- | ----------------- | -------------------- |
| `model_name`   | Yes      |         | Name of the model | Name of the model    |
| `rvc_version`  | Yes      |         | v1 or v2          | Version of the model |


#### Launch TensorBoard

```bash
python trainv2.py tensorboard
```


### API

```bash
python3 api.py 
```



To use the RVC CLI via the API, utilize the provided script. Make API requests to the following endpoints:

- **Docs**: `/docs`
- **Ping**: `/ping`
- **Infer**: `/infer`
- **Batch Infer**: `/batch_infer`
- **Preprocess**: `/preprocess`
- **Extract**: `/extract`
- **Train**: `/train`
- **Index**: `/index`


Make POST requests to these endpoints with the same required parameters as in CLI mode.

### Example for Infer

```bash

{
  "f0up_key": 0,
  "filter_radius": 3,
  "index_rate": 0.0,
  "rms_mix_rate": 1,
  "protect": 0.33,
  "hop_length": 128,
  "f0method": "rmvpe",
  "input_path": "./test-wavs/LJ001-0001.wav",
  "output_path": "./output/test3.wav",
  "pth_path": "./logs/models/weights/lj-ten.pth",
  "index_path": "./logs/models/weights/lj-ten.pth",
  "split_audio": true,
  "f0autotune": true,
  "clean_audio": true,
  "clean_strength": 0.7,
  "export_format": "WAV"
}

```


