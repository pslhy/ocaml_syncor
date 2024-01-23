import make_data_set
import subprocess
import os
import sys

# parso로 generate 할것인지 선택
parso_on = sys.argv[1]


gen = "/home/wangao/lab_work/checkml/syncor/syncor2.py"
# tmux : 몇 번째 도는지, subprocess, sys.arg

file = "/home/wangao/lab_work/checkml/syncor/sanitized-mbpp.json"

data_set = make_data_set.make_data_set(file)

for index, data in enumerate(data_set):

    
    # 종료 상태를 기록하기 위해 파일 경로를 파악한다.
    # 디렉터리 경로
    directory_path = f"/home/wangao/lab_work/checkml/syncor/log/syncor3"
    # 파일명 생성
    file_name = f"log_{index}_case.txt"
    # 파일 경로
    file_path = os.path.join(directory_path, file_name)

    
    print(f"{index} case test!")
    
    
    # 정상 종료된 경우
    try:
        
        result = subprocess.run(["python", gen, f"{index}", f"{data}"], timeout=300, stdout=subprocess.PIPE, text=True, check=True)
        
        with open(file_path, "a") as file:
                file.write("\n\n<<<<<<<<<<<<< End : In Time >>>>>>>>>>>>")
                
        print(result.stdout)
        
        
    # 타임 아웃으로 종료된 경우
    except subprocess.TimeoutExpired as e:
        with open(file_path, "a") as file:
                file.write("\n\n<<<<<<<<<<<<< End : Timeout >>>>>>>>>>>>")
    
        print("time-out")
    # 에러로 종료된 경우    
    except subprocess.CalledProcessError as e:
        with open(file_path, "a") as file:
                file.write("\n\n<<<<<<<<<<<<< End : Other Error >>>>>>>>>>>>")
    
