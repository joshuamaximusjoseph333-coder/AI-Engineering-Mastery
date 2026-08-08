import src.data_loader.logger

from src.data_loader.config import DATA_PATH
from src.data_loader.loader import count_lines


result = count_lines(DATA_PATH)

print(result)
