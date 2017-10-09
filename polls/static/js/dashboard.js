$(document).ready(function () {

    var data_values = $("#dashboard").val();
    var values = JSON.parse(data_values);

    function ValLength(val) {
        var lst = [];
        var x = 4 / val.length;
        for (i = 0; i < val.length; i++) {
            lst.push(x)
        }
        return lst
    }


    var colors = Highcharts.getOptions().colors,
        categories = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],
        data = [{
            y: 4.16,
            color: colors[0],
            drilldown: {
                name: 'MSIE versions',
                categories: values[0],
                data: ValLength(values[0]),
                color: colors[0]
            }
        }, {
            y: 4.16,
            color: colors[1],
            drilldown: {
                name: 'Firefox versions',
                categories: values[1],
                data: ValLength(values[1]),
                color: colors[1]
            }
        }, {
            y: 4.16,
            color: colors[2],
            drilldown: {
                name: 'Chrome versions',
                categories: values[2],
                data: ValLength(values[2]),
                color: colors[2]
            }
        }, {
            y: 4.16,
            color: colors[3],
            drilldown: {
                name: 'Safari versions',
                categories: values[3],
                data: ValLength(values[3]),
                color: colors[3]
            }
        }, {
            y: 4.16,
            color: colors[4],
            drilldown: {
                name: 'Opera versions',
                categories: values[4],
                data: ValLength(values[4]),
                color: colors[4]
            }
        }, {
            y: 4.16,
            color: colors[5],
            drilldown: {
                name: 'Proprietary or Undetectable',
                categories: values[5],
                data: ValLength(values[5]),
                color: colors[5]
            }
        },
            {
                y: 4.16,
                color: colors[6],
                drilldown: {
                    name: 'Proprietary or Undetectable',
                    categories: values[6],
                    data: ValLength(values[6]),
                    color: colors[6]
                }
            },
            {
                y: 4.16,
                color: colors[7],
                drilldown: {
                    name: 'MSIE versions',
                    categories: values[7],
                    data: ValLength(values[7]),
                    color: colors[7]
                }
            }, {
                y: 4.16,
                color: colors[8],
                drilldown: {
                    name: 'Firefox versions',
                    categories: values[8],
                    data: ValLength(values[8]),
                    color: colors[8]
                }
            }, {
                y: 4.16,
                color: colors[9],
                drilldown: {
                    name: 'Chrome versions',
                    categories: values[9],
                    data: ValLength(values[9]),
                    color: colors[9]
                }
            }, {
                y: 4.16,
                color: colors[0],
                drilldown: {
                    name: 'Safari versions',
                    categories: values[10],
                    data: ValLength(values[10]),
                    color: colors[0]
                }
            }, {
                y: 4.16,
                color: colors[1],
                drilldown: {
                    name: 'Opera versions',
                    categories: values[11],
                    data: ValLength(values[11]),
                    color: colors[1]
                }
            }, {
                y: 4.16,
                color: colors[2],
                drilldown: {
                    name: 'Proprietary or Undetectable',
                    categories: values[12],
                    data: ValLength(values[12]),
                    color: colors[2]
                }
            },
            {
                y: 4.16,
                color: colors[3],
                drilldown: {
                    name: 'Proprietary or Undetectable',
                    categories: values[13],
                    data: ValLength(values[13]),
                    color: colors[3]
                }
            },
            {
                y: 4.16,
                color: colors[4],
                drilldown: {
                    name: 'MSIE versions',
                    categories: values[14],
                    data: ValLength(values[14]),
                    color: colors[4]
                }
            }, {
                y: 4.16,
                color: colors[5],
                drilldown: {
                    name: 'Firefox versions',
                    categories: values[15],
                    data: ValLength(values[15]),
                    color: colors[5]
                }
            }, {
                y: 4.16,
                color: colors[6],
                drilldown: {
                    name: 'Chrome versions',
                    categories: values[16],
                    data: ValLength(values[16]),
                    color: colors[6]
                }
            }, {
                y: 4.16,
                color: colors[7],
                drilldown: {
                    name: 'Safari versions',
                    categories: values[17],
                    data: ValLength(values[17]),
                    color: colors[7]
                }
            }, {
                y: 4.16,
                color: colors[18],
                drilldown: {
                    name: 'Opera versions',
                    categories: values[18],
                    data: ValLength(values[18]),
                    color: colors[8]
                }
            }, {
                y: 4.16,
                color: colors[19],
                drilldown: {
                    name: 'Proprietary or Undetectable',
                    categories: values[19],
                    data: ValLength(values[19]),
                    color: colors[9]
                }
            },
            {
                y: 4.16,
                color: colors[0],
                drilldown: {
                    name: 'Proprietary or Undetectable',
                    categories: values[20],
                    data: ValLength(values[20]),
                    color: colors[0]
                }
            },
            {
                y: 4.16,
                color: colors[1],
                drilldown: {
                    name: 'MSIE versions',
                    categories: values[21],
                    data: ValLength(values[21]),
                    color: colors[1]
                }
            }, {
                y: 4.16,
                color: colors[2],
                drilldown: {
                    name: 'Firefox versions',
                    categories: values[22],
                    data: ValLength(values[22]),
                    color: colors[2]
                }
            }, {
                y: 4.16,
                color: colors[3],
                drilldown: {
                    name: 'Chrome versions',
                    categories: values[23],
                    data: ValLength(values[23]),
                    color: colors[3]
                }
            }],
        browserData = [],
        versionsData = [],
        i,
        j,
        dataLen = data.length,
        drillDataLen,
        brightness;


    // Build the data arrays
    for (i = 0; i < dataLen; i += 1) {

        // add browser data
        browserData.push({
            name: categories[i],
            y: data[i].y,
            color: data[i].color
        });

        // add version data
        drillDataLen = data[i].drilldown.data.length;
        for (j = 0; j < drillDataLen; j += 1) {
            brightness = 0.2 - (j / drillDataLen) / 5;
            versionsData.push({
                name: data[i].drilldown.categories[j],
                y: data[i].drilldown.data[j],
                color: Highcharts.Color(data[i].color).brighten(brightness).get()
            });
        }
    }

    // Create the chart
    Highcharts.chart('container', {
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Итоги голосования'
        },

        plotOptions: {
            pie: {
                shadow: false,
                center: ['50%', '50%']
            }
        },

        tooltip: {
            pointFormat: '{series.name}'
        },

        series: [{
            name: 'Время',
            data: browserData,
            size: '60%',
            dataLabels: {
                formatter: function () {
                    return this.y > 5 ? this.point.name : null;
                },
                color: '#ffffff',
                distance: -30
            }
        }, {
            name: 'Мероприятия',
            data: versionsData,
            size: '80%',
            innerSize: '60%',
            dataLabels: {
                formatter: function () {
                    // display only if larger than 1
                    return this.y > 1 ? '<b>' + this.point.name + '</b>' : null;
                }
            },
            id: 'versions'
        }],
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 400
                },
                chartOptions: {
                    series: [{
                        id: 'versions',
                        dataLabels: {
                            enabled: false
                        }
                    }]
                }
            }]
        }
    });

});