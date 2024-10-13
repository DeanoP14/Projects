import datetime
import console

def countdown_timer():
    try:
        # Pop-up text box for date input (format: DD-MM-YY)
        target_date_str = console.input_alert('Enter target date (DD-MM-YY):')
        
        # Convert the input from DD-MM-YY format to a datetime object
        target_date = datetime.datetime.strptime(target_date_str, '%d-%m-%y')
        
        # Calculate the number of days left
        today = datetime.datetime.now()
        days_left = (target_date - today).days
        
        # Display the result in another pop-up with an OK button
        if days_left >= 0:
            message = f'{days_left} days left until {target_date_str}'
        else:
            message = f'{abs(days_left)} days since {target_date_str}'
        
        # Pop-up alert with the result and OK button to close the app
        console.alert('Countdown Result', message, 'OK', hide_cancel_button=True)
        
    except ValueError:
        # Handle invalid date formats
        console.alert('Error', 'Please enter a valid date in the format DD-MM-YY', 'OK')

if __name__ == '__main__':
    countdown_timer()
