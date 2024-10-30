import numpy as np
from PySide6.QtCore import QObject, Signal,Property, QTimer, Slot
import csv

from typing import List, Tuple

class SensorBackend(QObject):
    point_added = Signal(list)
    changed_time_chart = Signal(float, float)

    def __init__(self):
        """
        Initializes the SensorBackend instance, setting up a timer to generate data points
        at regular intervals, initializing sensor settings, and loading CSV data for sensor 4.
        """
        
        super().__init__()
        self._timer = QTimer()
        self._timer.timeout.connect(self._generate_data)
        self._timer.start(100)
        self._time = 0
        self._graph_position = [0, 3]
        self._chart_pause = False
        
        self._frequency = 1
        self._amplitude = 1
        self._running = False
        
        self._sensor4_data = self.load_csv_data('data/sensor4.csv')
        self._sensor4_index = 0
        

    def load_csv_data(self,file_name: str) -> List[float]:
        """
        Loads data from a CSV file and returns it as a list of floats.

        Parameters:
            file_name (str): The name of the CSV file to load.

        Returns:
            List[float]: A list of sensor data values.
        """

        try:
            with open(file_name, 'r') as f:
                reader = csv.reader(f)
                return [float(value[0]) for value in reader]

        except FileNotFoundError:
            return []

    @Slot(float)
    def set_frequency(self,value: float):
        """
        Sets the frequency for data generation.

        Parameters:
            value (float): The frequency to set.
        """

        self._frequency = value

    @Slot(float)
    def set_amplitude(self,value: float):
        """
        Sets the amplitude for data generation.

        Parameters:
            value (float): The amplitude to set.
        """

        self._amplitude = value

    @Slot()
    def start(self):
        """
        Starts data generation.
        """

        self._running = True
    
    @Slot()
    def stop(self):
        """
        Stops data generation.
        """

        self._running = False

    @Property(bool)
    def running(self):
        """
        Indicates if data generation is currently running.

        Returns:
            bool: True if running, False otherwise.
        """

        return self._running
    

    @Slot(float, float)
    def _add_points(self, sensors: List[Tuple[float, float]]):
        """
        Emits signal to add points for the sensors at GUI.

        Parameters:
            sensors (List[Tuple[float, float]]): List of sensor values to add as points.
        """

        self.point_added.emit(sensors)

    @Slot(float, float)
    def change_time_chart(self):
        """
        Emits a signal to update the visible range of the chart based on the current graph position.
        """
        
        self.changed_time_chart.emit(self._graph_position[0],self._graph_position[1])


    @Slot()
    def scale_time_down(self):
        """
        Move the visible range of chart to the right
        """

        self._graph_position[0] += 0.1
        self._graph_position[1] += 0.1
        self.change_time_chart()

    @Slot()
    def scale_time_up(self):
        """
        Move the visible range of chart to the left
        """

        if self._graph_position[0] > 0:
            self._graph_position[0] -= 0.1
            self._graph_position[1] -= 0.1
        else:
            self._graph_position[0] = 0
            self._graph_position[1] = 3
        if self._graph_position[1] < self._time:
            self._chart_pause = True
        self.change_time_chart()

 
    def _get_sensor_1_value(self):
        """
        Generates a sine wave value for sensor 1 based on the current time, frequency, and amplitude.

        Returns:
            float: Sensor 1 value.
        """

        return float(self._amplitude * (np.sin(2 * np.pi * self._frequency * self._time)))
    
    def _get_sensor_2_value(self):
        """
        Generates a square wave value for sensor 2 based on the current time, frequency, and amplitude.

        Returns:
            float: Sensor 2 value.
        """

        return self._amplitude * (1 if (self._time * self._frequency) % 2 < 1 else -1)
    
    def _get_sensor_3_value(self):
        """
        Generates a triangle wave value for sensor 3 based on the current time, frequency, and amplitude.

        Returns:
            float: Sensor 3 value.
        """

        return self._amplitude * (2 * abs((self._time * self._frequency) % 1 - 0.5) - 1)
    
    def _get_sensor_4_value(self):
        """
        Retrieves the next value from sensor 4 data loaded from a CSV file. If no data, returns 0.

        Returns:
            float: Sensor 4 value.
        """

        if self._sensor4_data:
            value = (self._amplitude * (self._sensor4_data[self._sensor4_index] *  self._frequency) 
            if self._sensor4_index < len(self._sensor4_data) else 0)

            self._sensor4_index += 1
        else:
            value = 0
        return value
    
    def _get_all_sensors_values(self):
        """
        Retrieves values from all sensors.

        Returns:
            List[float]: List of values from each sensor.
        """

        return [self._get_sensor_1_value(), 
                self._get_sensor_2_value(), 
                self._get_sensor_3_value(),
                self._get_sensor_4_value()]
    
    def _move_chart_to_current_pos(self):
        """
        Adjusts the visible chart range to follow the current time if not paused.
        """

        if self._time > self._graph_position[1] and not self._chart_pause:
            self._graph_position[1] = self._time
            self._graph_position[0] = self._time - 3
            self.change_time_chart()
        elif self._chart_pause:
            if self._graph_position[1] > self._time:
                self._chart_pause = False

    def _generate_data(self):
        """
        Generates and emits sensor data points periodically when running.
        """

        if self._running:
            sensors_values = self._get_all_sensors_values()
            self._add_points([[self._time, sensor] for sensor in sensors_values])
            self._time += 0.1
            self._move_chart_to_current_pos()
            
