from datetime import datetime, timedelta

from models.event import Event  # chị cần định nghĩa model Event (nếu có)

def get_future_events_this_week(db):
    """
    Truy vấn các sự kiện việc làm, hội thảo diễn ra trong tuần này (chỉ dùng cho tiêu chí 9).
    Giả định có bảng Event và cột start_time.
    """
    now = datetime.now()
    end_of_week = now + timedelta(days=(6 - now.weekday()))
    events = db.query(Event).filter(Event.start_time >= now, Event.start_time <= end_of_week).all()
    return [f"{event.title} - {event.start_time.strftime('%d/%m/%Y')}" for event in events]