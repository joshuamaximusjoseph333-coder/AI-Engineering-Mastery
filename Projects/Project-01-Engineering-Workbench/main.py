import src.data_loader.logger

from src.data_loader.config import DATA_PATH
from src.data_loader.loader import load_csv
from src.data_loader.profiler import profile_data
from src.data_loader.validator import validate_required_columns


data = load_csv(DATA_PATH)

validate_required_columns(data)

profile = profile_data(data)

for key, value in profile.items():
    print(f"{key}: {value}")
