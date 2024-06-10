document.addEventListener('DOMContentLoaded', function() {
    var chartDom = document.getElementById('population-chart');
    var myChart = echarts.init(chartDom);

    var years = JSON.parse(document.getElementById('chart-data').getAttribute('data-years'));
    var chartData = JSON.parse(document.getElementById('chart-data').getAttribute('data-chart'));
    var growthData = JSON.parse(document.getElementById('chart-data').getAttribute('data-growth'));

    var cities = Object.keys(chartData);

    // 填充下拉選單
    var citySelect = document.getElementById('city-select');
    cities.forEach(function(city) {
        var option = document.createElement('option');
        option.value = city;
        option.text = city;
        citySelect.appendChild(option);
    });

    function updateChart(city) {
        var cityData = chartData[city];

        var totalPopulation = [];
        for (var i = 0; i < years.length; i++) {
            totalPopulation.push(cityData["0-14歲"][i] + cityData["15-64歲"][i] + cityData["65歲以上"][i]);
        }

        var option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            legend: {
                data: ['0-14歲', '15-64歲', '65歲以上', '總人口數']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: years
            },
            yAxis: {
                type: 'value',
                name: '人數'
            },
            series: [
                {
                    name: '0-14歲',
                    type: 'bar',
                    stack: '總數',
                    data: cityData["0-14歲"]
                },
                {
                    name: '15-64歲',
                    type: 'bar',
                    stack: '總數',
                    data: cityData["15-64歲"]
                },
                {
                    name: '65歲以上',
                    type: 'bar',
                    stack: '總數',
                    data: cityData["65歲以上"]
                },
                {
                    name: '總人口數',
                    type: 'line',
                    data: totalPopulation
                }
            ]
        };

        myChart.setOption(option);
    }

    // 初始化圖表
    updateChart(cities[0]);

    // 當選擇不同縣市時更新圖表
    citySelect.addEventListener('change', function() {
        var selectedCity = citySelect.value;
        updateChart(selectedCity);
    });
});
