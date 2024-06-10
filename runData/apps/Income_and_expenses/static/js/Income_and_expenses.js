document.addEventListener("DOMContentLoaded", function() {
    // 獲取數據
    var years = JSON.parse(document.getElementById('chart-data').getAttribute('data-years'));
    var data = JSON.parse(document.getElementById('chart-data').getAttribute('data-chart'));
    var growthRates = JSON.parse(document.getElementById('chart-data').getAttribute('data-growth-rates'));
    var avgDiff = JSON.parse(document.getElementById('chart-data').getAttribute('data-avg-diff'));

    var container = document.getElementById('charts-container');

    Object.keys(data.expenditure).forEach(function (key) {
        var colDiv = document.createElement('div');
        colDiv.className = 'col-md-6 pb-1 pb-md-0';

        var cardDiv = document.createElement('div');
        cardDiv.className = 'card';

        var chartDiv = document.createElement('div');
        chartDiv.setAttribute('id', 'chart-' + key);
        chartDiv.style.width = '100%';
        chartDiv.style.height = '300px';

        var cardBodyDiv = document.createElement('div');
        cardBodyDiv.className = 'card-body text-start'; 

        var cardTitle = document.createElement('h5');
        cardTitle.className = 'card-title';
        cardTitle.innerText = key;

        var cardText = document.createElement('p');
        cardText.className = 'card-text';
        cardText.innerText = '單位: 元' + '\n' + '成長幅度: ' + growthRates[key] + '%' + '\n' +'平均: ' + avgDiff[key];

        cardBodyDiv.appendChild(cardTitle);
        cardBodyDiv.appendChild(cardText);
        cardDiv.appendChild(chartDiv);
        cardDiv.appendChild(cardBodyDiv);
        colDiv.appendChild(cardDiv);
        container.appendChild(colDiv);

        // 配置圖表選項
        var option = {
            title: {
                text: key
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                data: years
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: '支出',
                    type: 'line',
                    stack: 'total',
                    data: data.expenditure[key],
                    areaStyle: {} // 填充顏色
                },
                {
                    name: '收入',
                    type: 'line',
                    stack: 'total',
                    data: data.revenue[key],
                    areaStyle: {} // 填充顏色
                }
            ]
        };

        var currentChart = echarts.init(chartDiv);
        currentChart.setOption(option);
    });
});
