from app import app, db, User, Event
from datetime import datetime, timedelta

def add_teacher_events():
    with app.app_context():
        # Check if teacher exists
        teacher = User.query.filter_by(username='1234', role='teacher').first()
        
        if not teacher:
            print('Teacher with username 1234 does not exist')
            return
        
        # Create events for next 7 days
        today = datetime.now().date()
        
        for i in range(7):
            event_date = today + timedelta(days=i)
            
            # Morning slot (9:00 - 10:00)
            morning_event = Event(
                user_id=teacher.id,
                title='Free Time',
                description='Available for booking',
                event_date=event_date,
                start_time=datetime.strptime('09:00', '%H:%M').time(),
                end_time=datetime.strptime('10:00', '%H:%M').time()
            )
            
            # Afternoon slot (14:00 - 15:00)
            afternoon_event = Event(
                user_id=teacher.id,
                title='Free Time',
                description='Available for booking',
                event_date=event_date,
                start_time=datetime.strptime('14:00', '%H:%M').time(),
                end_time=datetime.strptime('15:00', '%H:%M').time()
            )
            
            db.session.add(morning_event)
            db.session.add(afternoon_event)
        
        db.session.commit()
        print('Added availability events for teacher 1234 for the next 7 days')

if __name__ == '__main__':
    add_teacher_events() 