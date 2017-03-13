    var main = function() {
        var getVisitorData = function(purpose, area) {
            var showVisitorData = function() {
                $('#chart-container').highcharts({
                        xAxis: {
                            categories: visitorsArray.responseJSON.categories
                        },
                        series: visitorsArray.responseJSON.series,
                        title: {
                            text: '來臺旅客目的統計(按月分)',
                            x: -200 
                        }
                    });
            }
            var url = 'http://localhost:8000/visitors/highchart/' + purpose + '/' + area
            console.log(url)
            var visitorsArray = $.get({
                                    dataType: "json",
                                    url: url,
                                    success: showVisitorData
                                });

        }
        /*
        $('.purpose ul').children().click(function() {
                var purpose = $(this).children('a').attr('data-purpose');
                var area = $('.area ul').children('.active').children('a').attr('data-purpose');
                getVisitorData(purpose, area);
                });
        $('.area ul').children().click(function() {
                var purpose = $('.area ul').children('.active').children('a').attr('data-purpose');
                var area = $(this).children('a').attr('data-purpose');
                getVisitorData(purpose, area);
                });
        */
        $("#chartCTR").click(function() {
            purpose = $('.purpose option:selected').text()
            area = $('.area option:selected').text()
            var setting = function() {
                console.log('success')
                console.log(new_array)
                $('#chart-container').highcharts({
                    chart: {
                        type: 'area',
                        zoomType: 'x'
                    },
                    xAxis: {
                        type: 'category'
                        //categories: new_array.responseJSON.categories_year,
                        //min: 0,
                        //max: 36
                    },
                    series: new_array.responseJSON.series_drilldown_lv1,
                    drilldown: {
                    series: new_array.responseJSON.series_drilldown_lv2
                    },
                    title: new_array.responseJSON.title,
                    credits: false,
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'middle',
                        borderWidth: 0,
                        itemMarginBottom: 5,
                        itemStyle: {
                            fontSize: '14px',
                            fontFamily: "Helvetica Neue"
                        }
                    },
                    scrollbar: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            fillOpacity: 0.7,
                            //stacking: 'normal'
                        }
                    },
                    exporting: {
                        buttons: {
                            customButton: {
                                text: 'Custom Button',
                                onclick: function () {
                                    alert('You pressed the button!');
                                }
                            }
                        }
                    }
                });
            }
            var url = 'http://localhost:8000/visitors/api/' + purpose + '/' + area + '/'
            var new_array = 
            $.get({
            dataType: "json",
            url: url,
            success: setting
            });
        });
    }

    $(function () {
        $('#chart-container').highcharts({
            title: {
                text: 'Monthly Average Temperature',
                x: -20 //center
            },
            subtitle: {
                text: 'Source: WorldClimate.com',
                x: -20
            },
            xAxis: {
                type: 'category'
                //categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },
            yAxis: {
                title: {
                    text: 'Temperature (°C)'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: '°C'
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [{
                name: 'Tokyo',
                data: [{name: 'Jan', y: 7.0, drilldown: 'Tokyo_Jan'}, 
                    {name: 'Feb', y: 6.9, drilldown: 'Tokyo_Feb'},
                    {name: 'Mar', y: 9.5, drilldown: 'Tokyo_Mar'},
                    {name: 'Apr', y: 14.5, drilldown: 'Tokyo_Apr'},
                    {name: 'May', y: 18.2, drilldown: 'Tokyo_May'},
                    {name: 'Jun', y: 21.5, drilldown: 'Tokyo_Jun'},
                    {name: 'Jul', y: 25.2, drilldown: 'Tokyo_Jul'},
                    {name: 'Aug', y: 26.5, drilldown: 'Tokyo_Aug'},
                    {name: 'Sep', y: 23.3, drilldown: 'Tokyo_Sep'},
                    {name: 'Oct', y: 18.3, drilldown: 'Tokyo_Oct'},
                    {name: 'Nov', y: 13.9, drilldown: 'Tokyo_Nov'},
                    {name: 'Dec', y: 9.6, drilldown: 'Tokyo_Dec'}
                    ]
            },
            {
                name: 'New_York',
                data: [{name: 'Jan', y: -0.2, drilldown: 'New_York_Jan'}, 
                    {name: 'Feb', y: 0.8, drilldown: 'New_York_Feb'},
                    {name: 'Mar', y: 5.7, drilldown: 'New_York_Mar'},
                    {name: 'Apr', y: 11.3, drilldown: 'New_York_Apr'},
                    {name: 'May', y: 17.0, drilldown: 'New_York_May'},
                    {name: 'Jun', y: 22.0, drilldown: 'New_York_Jun'},
                    {name: 'Jul', y: 24.8, drilldown: 'New_York_Jul'},
                    {name: 'Aug', y: 24.1, drilldown: 'New_York_Aug'},
                    {name: 'Sep', y: 20.1, drilldown: 'New_York_Sep'},
                    {name: 'Oct', y: 14.1, drilldown: 'New_York_Oct'},
                    {name: 'Nov', y: 8.6, drilldown: 'New_York_Nov'},
                    {name: 'Dec', y: 2.5, drilldown: 'New_York_Dec'}
                    ]
            }/*, {
                name: 'New York',
                data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
            }, {
                name: 'Berlin',
                data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
            }, {
                name: 'London',
                data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
            }*/],
            drilldown: {
                series: [{
                    id: 'Tokyo_Jan',
                    name: 'Tokyo',
                    //categories: ['a', 'b', 'c', 'd'],
                    data: [['a', 1],
                        ['b', 1],
                        ['c', 1],
                        ['d', 1]
                    ]
                },
                {
                    id: 'Tokyo_Feb',
                    data: [['a', 4],
                        ['b', 3],
                        ['c', 2],
                        ['d', 1]
                    ]
                },
                {
                    id: 'New_York_Jan',
                    data: [['a', 7],
                        ['b', 8],
                        ['c', 7],
                        ['d', 8]
                    ]
                }]
            }
        });
    });

    $(document).ready(main);