import os

class ConsoleLogger:
    def __init__(self, update_rate):
        self.update_rate = update_rate
        self.frame_count = 0

    def log(self, objects):
        self.frame_count += 1
        if self.frame_count % self.update_rate != 0:
            return

        os.system('cls' if os.name == 'nt' else 'clear')

        print(f"{'ID':<4} | {'Тип':<10} | {'X':<6} | {'Y':<6}")
        print("-" * 30)
        
        if not objects:
            print("  -- Нет объектов --")
        else:
            for obj in objects:
                print(f"  {obj['id']:<2} | {obj['name']:<10} | {obj['center'][0]:<6} | {obj['center'][1]:<6}")
        print("-" * 30)