import os
import sys
import argparse
import subprocess

now_dir = os.getcwd()
sys.path.append(now_dir)

from rvc.configs.config import Config


config = Config()
current_script_directory = os.path.dirname(os.path.realpath(__file__))
logs_path = os.path.join(current_script_directory, "logs")

# Check for prerequisites
subprocess.run(
    ["python", os.path.join("rvc", "lib", "tools", "prerequisites_download.py")]
)

# Infer
def run_infer_script(
    f0up_key,
    filter_radius,
    index_rate,
    rms_mix_rate,
    protect,
    hop_length,
    f0method,
    input_path,
    output_path,
    pth_path,
    index_path,
    split_audio,
    f0autotune,
    clean_audio,
    clean_strength,
    export_format,
):
    infer_script_path = os.path.join("rvc", "infer", "infer.py")
    command = [
        "python",
        *map(
            str,
            [
                infer_script_path,
                f0up_key,
                filter_radius,
                index_rate,
                hop_length,
                f0method,
                input_path,
                output_path,
                pth_path,
                index_path,
                split_audio,
                f0autotune,
                rms_mix_rate,
                protect,
                clean_audio,
                clean_strength,
                export_format,
            ],
        ),
    ]
    subprocess.run(command)
    return f"File {input_path} inferred successfully.", output_path


# Batch infer
def run_batch_infer_script(
    f0up_key,
    filter_radius,
    index_rate,
    rms_mix_rate,
    protect,
    hop_length,
    f0method,
    input_folder,
    output_folder,
    pth_path,
    index_path,
    split_audio,
    f0autotune,
    clean_audio,
    clean_strength,
    export_format,
):
    infer_script_path = os.path.join("rvc", "infer", "infer.py")

    audio_files = [
        f for f in os.listdir(input_folder) if f.endswith((".mp3", ".wav", ".flac"))
    ]
    print(f"Detected {len(audio_files)} audio files for inference.")

    for audio_file in audio_files:
        if "_output" in audio_file:
            pass
        else:
            input_path = os.path.join(input_folder, audio_file)
            output_file_name = os.path.splitext(os.path.basename(audio_file))[0]
            output_path = os.path.join(
                output_folder,
                f"{output_file_name}_output{os.path.splitext(audio_file)[1]}",
            )
            print(f"Inferring {input_path}...")

        command = [
            "python",
            *map(
                str,
                [
                    infer_script_path,
                    f0up_key,
                    filter_radius,
                    index_rate,
                    hop_length,
                    f0method,
                    input_path,
                    output_path,
                    pth_path,
                    index_path,
                    split_audio,
                    f0autotune,
                    rms_mix_rate,
                    protect,
                    clean_audio,
                    clean_strength,
                    export_format,
                ],
            ),
        ]
        subprocess.run(command)

    return f"Files from {input_folder} inferred successfully."


# Parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run the main.py script with specific parameters."
    )
    subparsers = parser.add_subparsers(
        title="subcommands", dest="mode", help="Choose a mode"
    )

    # Parser for 'infer' mode
    infer_parser = subparsers.add_parser("infer", help="Run inference")
    infer_parser.add_argument(
        "--f0up_key",
        type=str,
        help="Value for f0up_key",
        choices=[str(i) for i in range(-24, 25)],
        default="0",
    )
    infer_parser.add_argument(
        "--filter_radius",
        type=str,
        help="Value for filter_radius",
        choices=[str(i) for i in range(11)],
        default="3",
    )
    infer_parser.add_argument(
        "--index_rate",
        type=str,
        help="Value for index_rate",
        choices=[str(i / 10) for i in range(11)],
        default="0.3",
    )
    infer_parser.add_argument(
        "--rms_mix_rate",
        type=str,
        help="Value for rms_mix_rate",
        choices=[str(i / 10) for i in range(11)],
        default="1",
    )
    infer_parser.add_argument(
        "--protect",
        type=str,
        help="Value for protect",
        choices=[str(i / 10) for i in range(6)],
        default="0.33",
    )
    infer_parser.add_argument(
        "--hop_length",
        type=str,
        help="Value for hop_length",
        choices=[str(i) for i in range(1, 513)],
        default="128",
    )
    infer_parser.add_argument(
        "--f0method",
        type=str,
        help="Value for f0method",
        choices=[
            "pm",
            "harvest",
            "dio",
            "crepe",
            "crepe-tiny",
            "rmvpe",
            "fcpe",
            "hybrid[crepe+rmvpe]",
            "hybrid[crepe+fcpe]",
            "hybrid[rmvpe+fcpe]",
            "hybrid[crepe+rmvpe+fcpe]",
        ],
        default="rmvpe",
    )
    infer_parser.add_argument("--input_path", type=str, help="Input path")
    infer_parser.add_argument("--output_path", type=str, help="Output path")
    infer_parser.add_argument("--pth_path", type=str, help="Path to the .pth file")
    infer_parser.add_argument(
        "--index_path",
        type=str,
        help="Path to the .index file",
    )
    infer_parser.add_argument(
        "--split_audio",
        type=str,
        help="Enable split audio",
        choices=["True", "False"],
        default="False",
    )
    infer_parser.add_argument(
        "--f0autotune",
        type=str,
        help="Enable autotune",
        choices=["True", "False"],
        default="False",
    )
    infer_parser.add_argument(
        "--clean_audio",
        type=str,
        help="Enable clean audio",
        choices=["True", "False"],
        default="False",
    )
    infer_parser.add_argument(
        "--clean_strength",
        type=str,
        help="Value for clean_strength",
        choices=[str(i / 10) for i in range(11)],
        default="0.7",
    )
    infer_parser.add_argument(
        "--export_format",
        type=str,
        help="Export format",
        choices=["WAV", "MP3", "FLAC", "OGG", "M4A"],
        default="WAV",
    )

    # Parser for 'batch_infer' mode
    batch_infer_parser = subparsers.add_parser(
        "batch_infer", help="Run batch inference"
    )
    batch_infer_parser.add_argument(
        "--f0up_key",
        type=str,
        help="Value for f0up_key",
        choices=[str(i) for i in range(-24, 25)],
        default="0",
    )
    batch_infer_parser.add_argument(
        "--filter_radius",
        type=str,
        help="Value for filter_radius",
        choices=[str(i) for i in range(11)],
        default="3",
    )
    batch_infer_parser.add_argument(
        "--index_rate",
        type=str,
        help="Value for index_rate",
        choices=[str(i / 10) for i in range(11)],
        default="0.3",
    )
    batch_infer_parser.add_argument(
        "--rms_mix_rate",
        type=str,
        help="Value for rms_mix_rate",
        choices=[str(i / 10) for i in range(11)],
        default="1",
    )
    batch_infer_parser.add_argument(
        "--protect",
        type=str,
        help="Value for protect",
        choices=[str(i / 10) for i in range(6)],
        default="0.33",
    )
    batch_infer_parser.add_argument(
        "--hop_length",
        type=str,
        help="Value for hop_length",
        choices=[str(i) for i in range(1, 513)],
        default="128",
    )
    batch_infer_parser.add_argument(
        "--f0method",
        type=str,
        help="Value for f0method",
        choices=[
            "pm",
            "harvest",
            "dio",
            "crepe",
            "crepe-tiny",
            "rmvpe",
            "fcpe",
            "hybrid[crepe+rmvpe]",
            "hybrid[crepe+fcpe]",
            "hybrid[rmvpe+fcpe]",
            "hybrid[crepe+rmvpe+fcpe]",
        ],
        default="rmvpe",
    )
    batch_infer_parser.add_argument("--input_folder", type=str, help="Input folder")
    batch_infer_parser.add_argument("--output_folder", type=str, help="Output folder")
    batch_infer_parser.add_argument(
        "--pth_path", type=str, help="Path to the .pth file"
    )
    batch_infer_parser.add_argument(
        "--index_path",
        type=str,
        help="Path to the .index file",
    )
    batch_infer_parser.add_argument(
        "--split_audio",
        type=str,
        help="Enable split audio",
        choices=["True", "False"],
        default="False",
    )
    batch_infer_parser.add_argument(
        "--f0autotune",
        type=str,
        help="Enable autotune",
        choices=["True", "False"],
        default="False",
    )
    batch_infer_parser.add_argument(
        "--clean_audio",
        type=str,
        help="Enable clean audio",
        choices=["True", "False"],
        default="False",
    )
    batch_infer_parser.add_argument(
        "--clean_strength",
        type=str,
        help="Value for clean_strength",
        choices=[str(i / 10) for i in range(11)],
        default="0.7",
    )
    batch_infer_parser.add_argument(
        "--export_format",
        type=str,
        help="Export format",
        choices=["WAV", "MP3", "FLAC", "OGG", "M4A"],
        default="WAV",
    )

    

    return parser.parse_args()

def main():
    if len(sys.argv) == 1:
        print("Please run the script with '-h' for more information.")
        sys.exit(1)

    args = parse_arguments()

    try:
        if args.mode == "infer":
            run_infer_script(
                str(args.f0up_key),
                str(args.filter_radius),
                str(args.index_rate),
                str(args.rms_mix_rate),
                str(args.protect),
                str(args.hop_length),
                str(args.f0method),
                str(args.input_path),
                str(args.output_path),
                str(args.pth_path),
                str(args.index_path),
                str(args.split_audio),
                str(args.f0autotune),
                str(args.clean_audio),
                str(args.clean_strength),
                str(args.export_format),
            )
        elif args.mode == "batch_infer":
            run_batch_infer_script(
                str(args.f0up_key),
                str(args.filter_radius),
                str(args.index_rate),
                str(args.rms_mix_rate),
                str(args.protect),
                str(args.hop_length),
                str(args.f0method),
                str(args.input_folder),
                str(args.output_folder),
                str(args.pth_path),
                str(args.index_path),
                str(args.split_audio),
                str(args.f0autotune),
                str(args.clean_audio),
                str(args.clean_strength),
                str(args.export_format),
            )
       
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
