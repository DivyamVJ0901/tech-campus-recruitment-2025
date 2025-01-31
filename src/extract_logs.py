import sys
import os
from datetime import datetime


def find_date_boundaries(file_path, target_date):
    target_date_str = target_date.strftime('%Y-%m-%d')
    file_size = os.path.getsize(file_path)
    low, high = 0, file_size
    start_pos, end_pos = None, None

    with open(file_path, 'rb') as f:
        while low <= high:
            mid = (low + high) // 2
            f.seek(mid)
            f.readline()  
            line = f.readline().decode('utf-8')
            if not line:
                break
            current_date = line.split()[0]
            if current_date < target_date_str:
                low = mid + 1
            else:
                high = mid - 1
        start_pos = f.tell()

        low, high = start_pos, file_size
        while low <= high:
            mid = (low + high) // 2
            f.seek(mid)
            f.readline()  
            line = f.readline().decode('utf-8')
            if not line:
                break
            current_date = line.split()[0]
            if current_date <= target_date_str:
                low = mid + 1
            else:
                high = mid - 1
        end_pos = f.tell()

    return start_pos, end_pos


def extract_logs(file_path, target_date, start_pos, end_pos):
    target_date_str = target_date.strftime('%Y-%m-%d')
    output_file = f"output/output_{target_date_str}.txt"
    os.makedirs("output", exist_ok=True)

    with open(file_path, 'rb') as f, open(output_file, 'w') as out_f:
        f.seek(start_pos)
        while f.tell() < end_pos:
            line = f.readline().decode('utf-8')
            if not line:
                break
            if line.startswith(target_date_str):
                out_f.write(line)


def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_logs.py YYYY-MM-DD")
        sys.exit(1)

    target_date_str = sys.argv[1]
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
    file_path = 'logs_2024.log'

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    start_pos, end_pos = find_date_boundaries(file_path, target_date)
    extract_logs(file_path, target_date, start_pos, end_pos)


if __name__ == "__main__":
    main()
