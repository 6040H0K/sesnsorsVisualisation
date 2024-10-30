import pytest
from unittest.mock import patch
from PySide6.QtCore import QTimer
from src import SensorBackend

@pytest.fixture
def sensor_backend() -> SensorBackend:
    """Fixture for initializing SensorBackend instance."""
    return SensorBackend()

@patch("src.backend.csv")
def test_load_csv_data(mock_csv, sensor_backend: SensorBackend) -> None:
    """Test loading CSV data into the SensorBackend instance."""

    mock_csv.reader.return_value = [["1.0"], ["2.5"], ["3.75"]]
    data = sensor_backend.load_csv_data('data/sensor4.csv')
    expected_data = [1.0, 2.5, 3.75]
    assert data == expected_data

def test_set_frequency(sensor_backend: SensorBackend) -> None:
    """Test setting the frequency in the SensorBackend instance."""

    sensor_backend.set_frequency(5.0)
    assert sensor_backend._frequency == 5.0

def test_set_amplitude(sensor_backend: SensorBackend) -> None:
    """Test setting the amplitude in the SensorBackend instance."""

    sensor_backend.set_amplitude(2.0)
    assert sensor_backend._amplitude == 2.0

def test_start(sensor_backend: SensorBackend) -> None:
    """Test starting the SensorBackend instance."""

    sensor_backend.start()
    assert sensor_backend.running is True

def test_stop(sensor_backend: SensorBackend) -> None:
    """Test stopping the SensorBackend instance."""

    sensor_backend.start()  
    sensor_backend.stop()
    assert sensor_backend.running is False

def test_get_sensor_1_value(sensor_backend: SensorBackend) -> None:
    """Test getting the value from sensor 1 based on amplitude and frequency."""

    sensor_backend.set_amplitude(2.0)
    sensor_backend.set_frequency(1.0)
    sensor_backend._time = 0.25  
    result = sensor_backend._get_sensor_1_value()
    assert isinstance(result, float)  
    assert result == pytest.approx(2.0 * 1.0, 0.01)  

def test_get_sensor_2_value(sensor_backend: SensorBackend) -> None:
    """Test getting the value from sensor 2, ensuring it returns valid values."""

    sensor_backend.set_amplitude(2.0)
    sensor_backend.set_frequency(1.0)
    sensor_backend._time = 0.5  
    result = sensor_backend._get_sensor_2_value()
    assert result == -2.0 or result == 2.0  

def test_get_sensor_3_value(sensor_backend: SensorBackend) -> None:
    """Test getting the value from sensor 3, checking the output against expected tolerance."""

    sensor_backend.set_amplitude(1.0)
    sensor_backend.set_frequency(1.0)
    sensor_backend._time = 0
    result = sensor_backend._get_sensor_3_value()
    assert isinstance(result, float)
    assert abs(result - 1.0) == 1.0 

@patch("src.backend.SensorBackend.change_time_chart")
def test_scale_time_down(mock_change_time_chart, sensor_backend: SensorBackend) -> None:
    """Test scaling the time down in the SensorBackend instance."""

    sensor_backend.scale_time_down()
    assert sensor_backend._graph_position[0] == 0.1
    assert sensor_backend._graph_position[1] == 3.1
    mock_change_time_chart.assert_called_once()

@patch("src.backend.SensorBackend.change_time_chart")
def test_scale_time_up(mock_change_time_chart, sensor_backend: SensorBackend) -> None:
    """Test scaling the time up in the SensorBackend instance."""

    sensor_backend._graph_position = [1.0, 4.0]
    sensor_backend.scale_time_up()
    assert sensor_backend._graph_position[0] == 0.9
    assert sensor_backend._graph_position[1] == 3.9
    mock_change_time_chart.assert_called_once()

@pytest.mark.parametrize("index, expected_value", [(0, 1.0), (1, 2.0), (2, 0.0)])
def test_get_sensor_4_value(sensor_backend: SensorBackend, index: int, expected_value: float) -> None:

    """Test getting the value from sensor 4 for different index values."""
    sensor_backend._sensor4_data = [1.0, 2.0]  
    sensor_backend._sensor4_index = index
    result = sensor_backend._get_sensor_4_value()
    assert result == expected_value

def test_point_added_signal(sensor_backend: SensorBackend, qtbot) -> None:
    """Test that the point_added signal is emitted with the correct arguments."""

    with qtbot.waitSignal(sensor_backend.point_added, timeout=500) as blocker:
        sensor_backend._add_points([[0, 1.0], [1, 2.0]])
    assert blocker.args == [[[0, 1.0], [1, 2.0]]]

def test_changed_time_chart_signal(sensor_backend: SensorBackend, qtbot) -> None:
    """Test that the changed_time_chart signal is emitted with the correct arguments."""

    with qtbot.waitSignal(sensor_backend.changed_time_chart, timeout=500) as blocker:
        sensor_backend.change_time_chart()
    assert blocker.args == [sensor_backend._graph_position[0], sensor_backend._graph_position[1]]
