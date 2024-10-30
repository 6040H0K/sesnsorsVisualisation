import QtQuick 2.15
import QtQuick.Controls 2.15
import QtCharts 2.8

ApplicationWindow {
    visible: true
    width: 800
    height: 700
    title: "Sensor Data"
    color: "#4c7187"
    Rectangle
    {
        width : 800
        height: 600
        clip:true

        ChartView {
            id: "chartView"
            title: "Line"
            anchors.fill: parent
            antialiasing: true

            ValueAxis {
                id: axisX
                min: 0
                max: 3
                titleText: "Time (s)"
            }
            ValueAxis {
                id: axisY
                min: -5
                max: 5
                titleText: "Sensor Value"
            }
            

            SplineSeries {
                id: "sensor1"
                name: "Sensor 1"
                pointsVisible: true

                axisX: axisX
                axisY: axisY
            }
            LineSeries {
                id: "sensor2"
                name: "Sensor 2"
                pointsVisible: true
                color: "#f0f"

                axisX: axisX
                axisY: axisY
            }
            LineSeries {
                id: "sensor3"
                name: "Sensor 3"
                pointsVisible: true
                color: "#ff1344"

                axisX: axisX
                axisY: axisY
            }
            LineSeries {
                id: "sensor4"
                name: "Sensor 4"
                pointsVisible: true
                color: "#F94"

                axisX: axisX
                axisY: axisY
            }
            MouseArea {
                anchors.fill: parent
                onWheel: {
                    if (wheel.angleDelta.y < 0) {
                        backend.scale_time_down()
                    } else {
                        backend.scale_time_up()
                    }
                }
            }
        }
    }
    Row{
        spacing: 10
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        topPadding: 100
        bottomPadding: 20

        Button {
            id: "startButton"
            text: "Start"
            background: Rectangle {
                color: "#0f6117"
            }
            onClicked: {
                if (backend.running) {
                    backend.stop()
                    startButton.text = "Start"
                    startButton.background.color = "#0f6117"
                } else{
                    backend.start()
                    startButton.text = "Stop"
                    startButton.background.color = "#f54242"
                }
            }
        }
        Button {
            text: "Save Graph"
            onClicked: {
                    chartView.grabToImage(function(result) {
                    const date = new Date();
                    const timestamp = date.getFullYear() + 
                                    ("0" + (date.getMonth() + 1)).slice(-2) + 
                                    ("0" + date.getDate()).slice(-2) + "_" + 
                                    ("0" + date.getHours()).slice(-2) + 
                                    ("0" + date.getMinutes()).slice(-2) + 
                                    ("0" + date.getSeconds()).slice(-2);
                    
                    const fileName = "charts/chart_" + timestamp + ".png";
                    result.saveToFile(fileName);
                       });
            }
            background: Rectangle {
                color: "#f5b942"
            }
        }
        Column {
            
            Slider {
                id: frequencySlider
                from: 0.1
                to: 100
                value: 1
                stepSize: 0.1
                onValueChanged: {
                    backend.set_frequency(value)
                    frequencyValue.text = value.toFixed(1)
                }
            }
            Row {
                Label {
                    text: "Frequency:"
                    color: "#000"
                }
                Label {
                    id: frequencyValue
                    text: "1"
                    color: "#000"
                }
            }
        }
        Column {
           Slider {
                id: amplitudeSlider
                from: 0.1
                to: 10
                value: 1
                stepSize: 0.1
                onValueChanged: {
                    backend.set_amplitude(value)
                    amplitudeValue.text = value.toFixed(1)
                }
            }
            Row {
                Label {
                    text: "Amplitude:"
                    color: "#000"
                }
                Label {
                    id: amplitudeValue
                    text: "1"
                    color: "#000"
                }
            }
        }
    }
    
    
    Component.onCompleted: {
        backend.point_added.connect(onPointAdded);

        backend.changed_time_chart.connect(onChangedTimeChart);
    }

    function onPointAdded(values) {
        const sensors = [sensor1, sensor2, sensor3, sensor4]
        for (let i = 0; i < sensors.length; i++) {
            sensors[i].append(values[i][0], values[i][1], values[i][2])
        }
    }
    function onPointAddedSensor2(x, y) {
        sensor2.append(x, y);
    }
    function onPointAddedSensor3(x, y) {
        sensor3.append(x, y);
    }
    function onPointAddedSensor4(x, y) {
        sensor4.append(x, y);
    }

    function onChangedTimeChart(min, max){
        axisX.min = min
        axisX.max = max
    }
    
}