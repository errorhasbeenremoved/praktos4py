import os
import threading
from datetime import datetime, timedelta

def delete_temp_files(folder_path, max_age_days):
    try:
        print(f"Поток {threading.current_thread().name} начал работу")  
        now = datetime.now()
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if filename.endswith('.tmp') or filename.startswith('~'):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if now - file_time > timedelta(days=max_age_days):
                    os.remove(file_path)
                    print(f"Удален файл: {file_path}")
                    
    except Exception as e:
        print(f"Ошибка в потоке {threading.current_thread().name}: {e}")
    finally:
        print(f"Поток {threading.current_thread().name} завершил работу")

def main():
    folder_path = input("Введите путь к папке для очистки: ").strip()
    
    if not os.path.isdir(folder_path):
        print("Указанный путь не является папкой или папка не существует")
        return
    try:
        max_age_days = int(input("Введите максимальный возраст временных файлов (в днях): "))
    except ValueError:
        print("Неверный формат числа")
        return
    
    threads = []
    num_threads = 3  
    for i in range(num_threads):
        thread = threading.Thread(target=delete_temp_files, 
                                  args=(folder_path, max_age_days), 
                                  name=f"Cleaner-{i+1}",
                                  daemon=True)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    
    print("Очистка завершена")
if __name__ == "__main__":
    main()
    