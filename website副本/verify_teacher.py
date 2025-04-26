from app import app, db, User, Event

def verify_teacher_and_events():
    with app.app_context():
        # Check if teacher exists
        teacher = User.query.filter_by(username='1234', role='teacher').first()
        print(f'Teacher exists: {teacher is not None}')
        
        if not teacher:
            return
        
        # Check events
        events = Event.query.filter_by(user_id=teacher.id).all()
        print(f'Number of events: {len(events)}')
        
        # Display first few events
        for i, event in enumerate(events[:5]):
            print(f'Event {i+1}: {event.title} on {event.event_date} at {event.start_time}-{event.end_time}')

if __name__ == '__main__':
    verify_teacher_and_events() 