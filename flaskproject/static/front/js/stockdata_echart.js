var StockDataChart = function () {

}

StockDataChart.prototype.defaultDrawLineChart = function () {
    zyajax.get({
            url:"/default_chart",
            success:function (result) {
                if(result){
                     // 基于准备好的dom，初始化echarts实例
                    console.log(result['report_date'])
                    console.log(result['DEDUCT_PARENT_NETPROFIT'])
                    var myChart = echarts.init(document.getElementById('lineChartContainer'));
                    // 指定图表的配置项和数据
                    var option= {
                        title: {
                            text: result['default_name']+'( '+result['default_code']+')'+
                                ' 更新日期:'+result['default_klines_time'][result['default_klines_time'].length - 1]+' /www.jiucaiger.cn',
                            textStyle: {
                                    fontSize: 12 // 设置字体大小为 30
                            },
                            left: 'center'
                        },
                        legend: {
                            top: "55%"
                        },
                        dataZoom: {
                            start: 0,
                            type: "inside",
                            xAxisIndex: [0, 1]
                          },
                        tooltip: {axisPointer: {
                          type: 'cross'
                        }},
                        axisPointer: {
                            link: [
                              {
                                xAxisIndex: 'all'
                              }
                            ],
                            label: {
                              backgroundColor: '#777'
                            }
                        },
                        toolbox: {
                            show: true,
                            feature: {
                              dataZoom: {
                                yAxisIndex: "none"
                              }
                            },
                            top: '10%'
                        },
                        grid: [{ bottom: '50%' }, { top: '62%' }],
                        xAxis: [
                            { type:'category',gridIndex: 0,xAxisIndex:0,data: result['default_klines_time']},
                            { type:'category',gridIndex: 1,xAxisIndex:1,data: result['report_date']}
                        ],
                        yAxis: [
                            { type:'value',gridIndex: 0,name: '日线/收盘价'},
                            { type:'value',gridIndex: 1,name: '经营数据/百万'}
                        ],
                        // xAxis: {
                        //     type: 'category',
                        //     data: result['default_klines_time']
                        // },
                        // yAxis: {
                        //     type: 'value',
                        //     name: '日线/收盘价',
                        // },
                        series: [
                            {
                                type: 'line',
                                xAxisIndex: 0,
                                yAxisIndex: 0,
                                data: result['default_klines_price'],
                                markLine: {
                                data: [{
                                    type: "average",
                                    name: "Avg"
                                }]
                                },
                                markPoint: {
                                data: [
                                  { type: 'max', name: 'Max' },
                                  { type: 'min', name: 'Min' }
                                ]
                                }
                            },
                            {
                                name: '扣非净利润',
                                type: 'bar',
                                xAxisIndex: 1,
                                yAxisIndex: 1,
                                data: result['DEDUCT_PARENT_NETPROFIT'],
                                markLine: {
                                data: [{
                                    type: "average",
                                    name: "Avg"
                                }]
                                },
                            },
                            {
                                name: '营业收入',
                                type: 'bar',
                                xAxisIndex: 1,
                                yAxisIndex: 1,
                                data: result['OPERATE_INCOME'],
                                markLine: {
                                data: [{
                                    type: "average",
                                    name: "Avg"
                                }]
                                },
                            },
                             {
                                name: '营业利润',
                                type: 'bar',
                                xAxisIndex: 1,
                                yAxisIndex: 1,
                                data: result['OPERATE_PROFIT'],
                                markLine: {
                                data: [{
                                    type: "average",
                                    name: "Avg"
                                }]
                                },
                            },
                        ],
                        // grid: {
                        //     left: '6%', // 设置图表距离容器左侧的距离
                        //     right: '5%', // 设置图表距离容器右侧的距离
                        //     bottom: '10%', // 设置图表距离容器底部的距离
                        //     top: '20%' // 设置图表距离容器顶部的距离
                        // }

                    };
                    // 使用刚指定的配置项和数据显示图表。
                    myChart.setOption(option);
                }else {
                    alert('主页默认数据加载失败');
                }
            }
        })
}

// StockDataChart.prototype.updateDrawLineChart = function () {
//     zyajax.get({
//             url:"/update_chart",
//             success:function (result) {
//                 if(result){
//                      // 基于准备好的dom，初始化echarts实例
//                     var myChart = echarts.init(document.getElementById('lineChartContainer'));
//                     // 指定图表的配置项和数据
//                     var option = {
//                         title: {
//                             text: result['default_name']+'( '+result['default_code']+')'+
//                                 ' 更新日期:'+result['default_klines_time'][result['default_klines_time'].length - 1]+' /www.jiucaiger.cn',
//                             textStyle: {
//                                     fontSize: 12 // 设置字体大小为 30
//                             },
//                             left: 'center'
//                         },
//                         dataZoom: {
//                             start: 0,
//                             type: "inside"
//                           },
//                         toolbox: {
//                             show: true,
//                             feature: {
//                               dataZoom: {
//                                 yAxisIndex: "none"
//                               }
//                             },
//                             right: '5%',
//                             top: '10%'
//                         },
//                         // tooltip: {
//                         //     trigger: 'axis'
//                         // },
//                         xAxis: {
//                             type: 'category',
//                             data: result['default_klines_time']// 假设后端传入的数据中包含了 categories 数组作为x轴的数据
//                         },
//                         yAxis: {
//                             type: 'value',
//                             name: '日线',
//                             // nameLocation: 'middle',
//                             // nameGap: 30,
//                             // nameTextStyle: {
//                             //      color: "rgb(0,0,0)"
//                             // }
//                         },
//                         series: [{
//                             data: result['default_klines_price'], // 假设后端传入的数据中包含了 values 数组作为y轴的数据
//                             type: 'line',
//                             markLine: {
//                               data: [{
//                                 type: "average",
//                                 name: "Avg"
//                               }]
//                             }
//                         }],
//                         grid: {
//                             left: '6%', // 设置图表距离容器左侧的距离
//                             right: '5%', // 设置图表距离容器右侧的距离
//                             bottom: '10%', // 设置图表距离容器底部的距离
//                             top: '20%' // 设置图表距离容器顶部的距离
//                         }
//                     };
//                     // 使用刚指定的配置项和数据显示图表。
//                     myChart.setOption(option);
//                 }else {
//                     alert('主页默认数据加载失败');
//                 }
//             }
//         })
// }

StockDataChart.prototype.run = function () {
    // this.updateDrawLineChart();
    this.defaultDrawLineChart();
}

$(function(){
    var handler = new StockDataChart();
    handler.run()
});