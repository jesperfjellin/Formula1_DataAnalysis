import fastf1 as ff1
from fastf1 import plotting
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Skru på cache
ff1.Cache.enable_cache('cache')

plotting.setup_mpl()

# Try except for å sjekke om data har blitt tilgjengeliggjort

try: 
    session = ff1.get_session(2023, 'Saudi Arabia', 'FP3')
    session.load()
    
    driver = 'LEC'
    driver2 = 'SAI'
    fastest_driver = session.laps.pick_driver(driver).pick_fastest()
    fastest_driver2 = session.laps.pick_driver(driver2).pick_fastest()
    telemetry_driver = fastest_driver.get_telemetry().add_distance()
    telemetry_driver2 = fastest_driver2.get_telemetry().add_distance()
    
    # Regn tid hvor hver driver
    time_float = telemetry_driver['Time'] / np.timedelta64(1, 's')
    time_float2 = telemetry_driver2['Time'] / np.timedelta64(1, 's')
    
    # Regn longitudinal acceleration 
    v = telemetry_driver['Speed'] / 3.6
    ax = np.gradient(v) / np.gradient(time_float)
    ax_smooth = np.convolve(ax, np.ones((3,))/3, mode = 'same')
    
    # Lag plot
    fig, axes = plt.subplots(2, 1, figsize=(12, 12,))
    axes[0].plot(telemetry_driver['Distance'], telemetry_driver['Speed'], label=driver, linewidth=2, color='blue')
    axes[0].plot(telemetry_driver2['Distance'], telemetry_driver2['Speed'], label=driver2, linewidth=2, color='red')
    axes[0].set_xlabel('Distance (m)')
    axes[0].set_ylabel('Speed (km/h)')
    axes[0].legend()
    
    axes[1].plot(telemetry_driver['Distance'], time_float, label=driver, color='blue')
    axes[1].plot(telemetry_driver2['Distance'], time_float2, label=driver2, color='red')
    axes[1].set_xlabel('Distance (m)')
    axes[1].set_ylabel('Time (s)')
    axes[1].legend()
    plt.show()
    
    lap_time = fastest_driver.loc['LapTime']
    lap_time_seconds = lap_time.total_seconds()
    lap_time_str = str(datetime.timedelta(seconds=lap_time_seconds))[3:-3]
    
    lap_time2 = fastest_driver2.loc['LapTime']
    lap_time2_seconds = lap_time2.total_seconds()
    lap_time_str2 = str(datetime.timedelta(seconds=lap_time2_seconds))[3:-3]
    
    tires = fastest_driver.loc['Compound']
    tires2 = fastest_driver2.loc['Compound']
    lap_number = fastest_driver.loc['LapNumber']
    lap_number2 = fastest_driver.loc['LapNumber']
    
    
    print('Driver: ' + driver2 + ' Lap time: ' + lap_time_str2)
    print('Driver: ' + driver + ' Lap time: ' + lap_time_str)
    if lap_time > lap_time2:
        diff = lap_time - lap_time2
        diff_seconds = diff.total_seconds()
        diff_str = '{:.3f}'.format(diff_seconds)
        #print(driver2 + " was " + diff_str + " seconds faster than " + driver + " on " + tires.lower() + " tires during lap number " + str(lap_number) + ".")
        print(f"{driver2} was {diff_str} seconds faster than {driver} on {tires.lower()} tires during lap number {str(lap_number)}.")
    else:
        diff = lap_time2 - lap_time
        diff_seconds = diff.total_seconds()
        diff_str = '{:.3f}'.format(diff_seconds)
        #print(driver + " was " + diff_str + " seconds faster than " + driver2 + " on " + tires2.lower() + " tires during lap number " + str(lap_number2) + ".")
        print(f"{driver} was {diff_str} seconds faster than {driver2} on {tires2.lower()} tires during lap number {str(lap_number2)}.")
except Exception:
    print("-----------------------------------------------")
    print("The data has not been made available as of yet!")
    print("-----------------------------------------------")








