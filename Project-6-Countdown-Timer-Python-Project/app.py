import time
import sys
import msvcrt
def countdown_timer(seconds):
    print(f"Starting countdown for {seconds} seconds...\nPress 'p' to pause, 'r' to resume, 's' to stop.\n")
    
    paused = False

    while seconds:
        if not paused:
            mins, secs = divmod(seconds, 60)
            timer = f'{mins:02d}:{secs:02d}'
            progress = '█' * (30 * (countdown_time - seconds) // countdown_time) 
            sys.stdout.write(f"\r{timer} | {progress:<30}")
            sys.stdout.flush()

            time.sleep(1)
            seconds -= 1

        if msvcrt.kbhit():  
            user_input = msvcrt.getch().decode('utf-8').strip().lower()
            if user_input == 'p':
                paused = True
                print("\nPaused. Press 'r' to resume.")
            elif user_input == 'r':
                paused = False
                print("Resuming countdown...")
            elif user_input == 's':
                print("\nCountdown stopped.")
                return

    print("\nTime's up! 🔔🔔🔔")

countdown_time = 10  
countdown_timer(countdown_time)
