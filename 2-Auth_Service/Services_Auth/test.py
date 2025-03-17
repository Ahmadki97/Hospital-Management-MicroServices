from datetime import datetime, timedelta

def calculateUpcomingWorkDays(work_days: list, current_date=None):
    try:
        current_date = datetime.now().date()
        print(f"Current date is {current_date}")
        upcoming_workdays = []
        for day in work_days:
            print(f"Days is {day}")
            print(f"Current day is {current_date.weekday()}")
            days_ahead = (day - current_date.weekday() + 7) % 7
            if days_ahead == 0:
                days_ahead = 7
            next_workdays = current_date + timedelta(days=days_ahead)
            upcoming_workdays.append(next_workdays)
        return upcoming_workdays
    except Exception as err:
        print(f"Error in calculateUpcomingWorkDays() Method: {err}")
        

if __name__ == "__main__":
    work_days = [5, 6]  # Monday and Tuesday
    upcoming_workdays = calculateUpcomingWorkDays(work_days)
    print(upcoming_workdays)
    