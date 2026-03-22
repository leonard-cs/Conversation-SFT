from huggingface_hub import login, upload_folder

# (optional) Login with your Hugging Face credentials
login()

# Push your model files
upload_folder(folder_path="../checkpoint_models", repo_id="leonard-milo/Qwen3.5-2B-SFT-AutoConv-InstagramChat-Smart", repo_type="model")
