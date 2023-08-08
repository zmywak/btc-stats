import pandas as pd
import datetime
import calendar

def load_data_from_file(filename):
    data = pd.read_csv(filename, header=None, names=["timestamp", "open", "high", "low", "close", "volume", "closetime", "quoteassetvolume", "trades", "takerbuybaseassetvolume", "takerbuyquoteassetvolume", "ignore"])
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit='ms')
    data.set_index("timestamp", inplace=True)
    return data
   
def calculate_statistics_for_a_given_day(data, given_day):
    stats_given_day = {'Monday': {'bigger': 0, 'lower': 0},
             'Tuesday': {'bigger': 0, 'lower': 0},
             'Wednesday': {'bigger': 0, 'lower': 0},
             'Thursday': {'bigger': 0, 'lower': 0},
             'Friday': {'bigger': 0, 'lower': 0},
             'Saturday': {'bigger': 0, 'lower': 0},
             'Sunday': {'bigger': 0, 'lower': 0}}

    prev_row = None
    
    for i in range(0, len(data)):
        current_row = data.iloc[ i ]
        day_of_week = int( current_row[ 'day_of_week' ] ) 
        
        if( day_of_week == given_day ):
            prev_row = current_row.copy()
            prev_high = prev_row[ 'high' ]
            for j in range( 1, 7 ):
                i += 1
                if i < len( data ):
                    current_row = data.iloc[i]
                    today_high = current_row['high']
                    day_of_week = int(current_row['day_of_week']) 
                    day_name = calendar.day_name[day_of_week]
                    
                    if prev_high > today_high:
                        stats_given_day[day_name]['lower'] += 1
                    else:
                        stats_given_day[day_name]['bigger'] += 1
                
    return stats_given_day

if __name__ == "__main__":
    file_name = 'BTCUSDT_trading_history.txt'

    data = load_data_from_file(file_name)
    data['day_of_week'] = data.index.dayofweek
    days = { 'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4, 'Saturday' : 5, 'Sunday' : 6 }
    
    if data is not None:     
        for day_name, day_number in days.items():
            print( f"\n==Stats for {day_name}==" )
            stats_given_day = calculate_statistics_for_a_given_day( data, day_number )
            for day, stat in stats_given_day.items():
                print(f"{day}s: {stat['bigger']} days had higher high, {stat['lower']} days had lower high.")       
    else:
        print(f"Failed to load data from {file_name}. Make sure the file exists and is correctly formatted.")