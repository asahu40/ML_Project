import logging
from datetime import datetime
import os

Log_Dir = "housing_logs"
Current_Time_Stamp = f"{datetime.now().strftime('%Y-%M-%D_%H-%M-%S')}"
Log_File_Name = f"log_{Current_Time_Stamp}.log"
os.makedirs(Log_Dir,exist_ok=True)
Log_File_Path = os.path.join(Log_Dir,Log_File_Name)

logging.basicConfig(
    filename=Log_File_Path,
    filemode="w",
    format='[%(sctine)s,] %(name)s,%(levelname)s,%(message)s',
    level=logging.INFO

)