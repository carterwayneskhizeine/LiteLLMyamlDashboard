Write-Host "Activating Conda environment 'litellm'..."
conda activate litellm

Write-Host "cd D:\Code\LiteLLMyamlDashboard\"
cd D:\Code\LiteLLMyamlDashboard\

Write-Host "streamlit run"
streamlit run app.py