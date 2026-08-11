import src.data_loader.logger

from src.data_loader.config import DATA_PATH
from src.data_loader.loader import load_csv
from src.data_loader.profiler import profile_data


data = load_csv(DATA_PATH)

profile = profile_data(data)

print(profile)