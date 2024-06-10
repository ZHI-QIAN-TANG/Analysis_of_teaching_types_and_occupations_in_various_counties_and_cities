document.addEventListener("DOMContentLoaded", function() {
    // 確保 cityData 正確傳遞並解析
    if (typeof cityData === 'undefined') {
        console.error('cityData 未定義。');
        return;
    }

    // 初始化 ECharts
    var chartDom = document.getElementById('pie-chart');
    var myChart = echarts.init(chartDom);

    // 初始化時顯示第一個城市的數據
    var initialCity = Object.keys(cityData)[0];
    updateChart(initialCity);

    // 監聽縣市選擇框的變化
    var citySelect = document.getElementById('city-select');
    if (citySelect) {
        citySelect.addEventListener('change', function() {
            var selectedCity = this.value;
            updateChart(selectedCity);
        });
    } else {
        console.error('未找到 city-select 元素。');
    }

    function updateChart(city) {
        if (!cityData[city]) {
            console.error('未找到選擇的城市數據：' + city);
            return;
        }

        var data = cityData[city];

        // 構建 ECharts 所需的數據格式
        var seriesData = [];
        data.forEach(function(item) {
            for (var key in item) {
                if (key !== '縣市') {
                    seriesData.push({
                        name: key,
                        value: item[key]
                    });
                }
            }
        });

        // 設置 ECharts 配置
        var option = {
            title: {
                text: city + ' 各行業類別分布',
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b} : {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 'left'
            },
            series: [
                {
                    name: '行業類別',
                    type: 'pie',
                    radius: '50%',
                    data: seriesData,
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };

        // 使用指定的配置和數據顯示圖表
        myChart.setOption(option);
    }
});
