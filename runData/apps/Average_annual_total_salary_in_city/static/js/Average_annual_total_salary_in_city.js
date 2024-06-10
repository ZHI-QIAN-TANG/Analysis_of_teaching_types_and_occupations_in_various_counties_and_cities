document.addEventListener("DOMContentLoaded", function() {
    // 獲取數據
    var years = JSON.parse(document.getElementById('chart-data').getAttribute('data-years'));
    var data = JSON.parse(document.getElementById('chart-data').getAttribute('data-chart'));
    var growthRates = JSON.parse(document.getElementById('chart-data').getAttribute('data-growth-rates'));

    var container = document.getElementById('charts-container');

    // 生成圖表並且存在列表中
    var count = 0;
    Object.keys(data).forEach(function (key) {
        var colDiv = document.createElement('div');
        colDiv.className = 'col-md-4 pb-1 pb-md-0';

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
        cardText.innerText = '單位: 千' + '\n' + '成長幅度: ' + growthRates[key] + '%';

        cardBodyDiv.appendChild(cardTitle);
        cardBodyDiv.appendChild(cardText);
        cardDiv.appendChild(chartDiv);
        cardDiv.appendChild(cardBodyDiv);
        colDiv.appendChild(cardDiv);
        container.appendChild(colDiv);

        count++;
        if (count % 3 === 0) {
            var clearfixDiv = document.createElement('div');
            clearfixDiv.className = 'w-100 d-none d-md-block';
            container.appendChild(clearfixDiv);
        }

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
            series: [{
                name: key,
                type: 'line',
                data: data[key]
            }]
        };

        var currentChart = echarts.init(chartDiv);
        currentChart.setOption(option);
    });
});
