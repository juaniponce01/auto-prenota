import subprocess
import os

def schedule_script(script_path, cron_expression):
    # Create a unique identifier for this scheduled task
    task_identifier = "my_scheduled_task"

    # Get the current user's home directory
    home_dir = os.path.expanduser("~")

    # Define the command to run the script
    command = f"python3 {script_path}"

    # Create the crontab entry
    crontab_entry = f"{cron_expression} {command} >> {home_dir}/{task_identifier}.log 2>&1"

    # Write the crontab entry to a temporary file
    temp_file_path = f"/tmp/{task_identifier}_temp_crontab"
    with open(temp_file_path, "w") as temp_file:
        temp_file.write(crontab_entry)

    # Install the crontab entry
    subprocess.run(["crontab", temp_file_path])

    print(f"Script scheduled successfully with cron expression: {cron_expression}")

if __name__ == "__main__":
    script_path = "/path/to/your_script.py"
    cron_expression = "2 0 * * *"

    schedule_script(script_path, cron_expression)
