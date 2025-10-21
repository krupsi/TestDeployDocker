import schedule
import time
import subprocess
import sys
import os
from datetime import datetime
from art import tprint


class ProjectManager:
    def __init__(self):
        self.scripts = ["p1.py", "p2.py", "p3.py"]
        self.running = True

    def run_script(self, script_name):
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Запуск {script_name}...")

        try:
            # Запускаем скрипт как отдельный процесс
            result = subprocess.run([sys.executable, script_name],
                                    capture_output=True, text=True, cwd=os.getcwd())

            if result.returncode == 0:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {script_name} завершен успешно")
                if result.stdout:
                    print(f"Вывод {script_name}:\n{result.stdout}")
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ошибка в {script_name}:")
                if result.stderr:
                    print(f"Ошибка: {result.stderr}")
                if result.stdout:
                    print(f"Вывод: {result.stdout}")

        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Исключение при запуске {script_name}: {e}")

    def run_all_scripts(self): #запускает все скрипт
        print(f"\n{'=' * 50}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Начало цикла выполнения")
        print(f"{'=' * 50}")

        for script in self.scripts:
            if not self.running:
                break
            self.run_script(script)
            time.sleep(1)

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Цикл выполнения завершен")
        print(f"{'=' * 50}")

    def start_once(self): #запускает все скрипт один раз
        self.run_all_scripts()

    def run_single_script(self): #запускает выбранный срипт один раз
        print("\nДоступные скрипты:")
        for i, script in enumerate(self.scripts, 1):
            print(f"{i}. {script}")

        try:
            choice = int(input("Выберите номер скрипта: ")) - 1
            if 0 <= choice < len(self.scripts):
                self.run_script(self.scripts[choice])
            else:
                print("Неверный номер скрипта.")
        except ValueError:
            print("Введите корректный номер.")

    def start_scheduled(self): #запуск режима планировщика с выбором промежутка для старта
        delay = input("Введите промежуток для повторения запуска скрипта в формате {0h or 0m or 0s}: ")
        if delay[-1] == 'm':
            schedule.every(int(delay[:-1])).minutes.do(self.run_all_scripts)
        elif delay[-1] == 'h':
            schedule.every(int(delay[:-1])).hours.do(self.run_all_scripts)
        elif delay[-1] == 's':
            schedule.every(int(delay[:-1])).seconds.do(self.run_all_scripts)
        else:
            print("Неверный формат ввода промежутка!!!")
            print("\n\nЗавершение работы менеджера...")
            self.running = False

        print(f"\nМенеджер запущен. Скрипты будут выполняться каждый(ыe) {delay}.")
        print("Нажмите Ctrl+C для выхода.")

        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nЗавершение работы менеджера...")
            self.running = False

    def interactive_mode(self): #интерактивное меню
        while self.running:
            tprint("SCRIPT MANAGER")
            print("1. Запустить все скрипты один раз")
            print("2. Запустить в режиме планировщика")
            print("3. Запустить отдельный скрипт")
            print("4. Выход")
            print("=" * 50)

            choice = input("Выберите действие (1-4): ").strip()

            if choice == "1":
                self.start_once()
            elif choice == "2":
                self.start_scheduled()
            elif choice == "3":
                self.run_single_script()
            elif choice == "4":
                self.running = False
                print("Выход из менеджера...")
            else:
                print("Неверный выбор. Попробуйте снова.")




def main():
    manager = ProjectManager()

    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        if sys.argv[1] == "--once":
            manager.start_once()
        elif sys.argv[1] == "--scheduled":
            manager.start_scheduled()
        elif sys.argv[1] == "--interactive":
            manager.interactive_mode()
        else:
            print("Использование:")
            print("python manager.py              # Интерактивный режим")
            print("python manager.py --once       # Запуск один раз")
            print("python manager.py --scheduled  # Режим планировщика")
            print("python manager.py --interactive# Интерактивный режим")
    else:
        # По умолчанию запускаем интерактивный режим
        manager.interactive_mode()


if __name__ == "__main__":
    main()