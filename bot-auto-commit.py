from datetime import datetime

# Open file and append current date/time
with open("log.txt", "a") as file:
    file.write(f"Updated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
