import json

def read_schedule_file():
    with open('appointments/schedule.py', 'r') as file:
        schedule_data = file.read()
    schedule_dict = json.loads(schedule_data)
    return schedule_dict

schedule = read_schedule_file()

