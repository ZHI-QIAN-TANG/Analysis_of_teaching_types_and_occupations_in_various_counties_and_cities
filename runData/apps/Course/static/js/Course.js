document.addEventListener('DOMContentLoaded', function () {
    var citySelect = document.getElementById('city-select');
    var totalCountElement = document.getElementById('total-count');

    function updateCharts(city) {
        if (!cityData[city]) {
            console.error(`No data available for city: ${city}`);
            return;
        }

        var categoryData = cityData[city].category_counts;

        // 更新課程總數
        totalCountElement.textContent = '總課程數: ' + cityData[city].total_count;

        // 長條圖
        var barChart = echarts.init(document.getElementById('bar-chart'));
        var barOption = {
            title: {
                text: city + '課程類別統計'
            },
            tooltip: {},
            xAxis: {
                type: 'category',
                data: Object.keys(categoryData)
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: Object.values(categoryData),
                type: 'bar'
            }]
        };
        barChart.setOption(barOption);

        // 圓餅圖
        var pieChart = echarts.init(document.getElementById('pie-chart'));
        var pieOption = {
            title: {
                text: city + '課程類別分布',
                left: 'center'
            },
            tooltip: {
                trigger: 'item'
            },
            series: [{
                type: 'pie',
                radius: '50%',
                data: Object.keys(categoryData).map(function (key) {
                    return { value: categoryData[key], name: key };
                })
            }]
        };
        pieChart.setOption(pieOption);
    }

    // 初始化圖表
    if (citySelect.value) {
        updateCharts(citySelect.value);
    }

    // 當縣市選擇變化時更新圖表
    citySelect.addEventListener('change', function () {
        updateCharts(this.value);
    });
});
