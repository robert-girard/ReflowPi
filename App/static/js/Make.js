/*
ReflowPi

Copyright © <2019> <Robert Girard>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

var chartEvent = new CustomEvent(
	"chartEvent", 
	{
		detail: {
			message: "chartEvent",
			time: new Date(),
		},
		bubbles: true,
		cancelable: true
	}
);

function buildChart(mychart) {
    var time = 0
    var data1 = []
    var labels = []
    $('#sortableList > tr').each(function(index) {
        var Y1 = parseInt($(this).find(".startTemp").text());
        var Y2 = parseInt($(this).find(".endTemp").text());
        var X1 = time;
        time += parseInt($(this).find(".Duration").text());
        var X2 = time;
        data1.push({x: X1, y: Y1});
        data1.push({x: X2, y: Y2});
        labels.push(X1)
        labels.push(X2)
    });
    //document.getElementById("dummy").innerHTML = JSON.stringify(data1);
    
    var ctx = $('#ProfileChart')
    var myLineChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Votes',
                data: data1,
                borderWidth: 1,
                showLine: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                    }
                }],
                xAxes: [{
                    display: true,
                    ticks: {
                        beginAtZero: true,
                    }
                }]
            },
            elements: {
                line: {
                    tension: 0
                }
            }
        }

    });
    console.log(data1);
    return myLineChart;
}

function updateChart() {
    var time = 0
    var data1 = []
    var labels = []
    $('#sortableList > tr').each(function(index) {
        var Y1 = parseInt($(this).find(".startTemp").text());
        var Y2 = parseInt($(this).find(".endTemp").text());
        var X1 = time;
        time += parseInt($(this).find(".Duration").text());
        var X2 = time;
        data1.push({x: X1, y: Y1});
        data1.push({x: X2, y: Y2});
        labels.push(X1)
        labels.push(X2)
    });
    console.log(ChartCTX.data)
    console.log(data1)
    var newChart = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Votes',
                data: data1,
                borderWidth: 1
            }]
        }
    };
    ChartCTX.data.datasets[0].data = data1
    ChartCTX.update();
    //ChartCTX.update();
    //ChartCTX.update();
}

function ParseTable() {
    var Steps = [];
    $("#sortableList tr").each(function(index){
        var Step = {
            stepNum : $(this).find("td.step").html(),
            startTemp : $(this).find("td.startTemp").html(),
            endTemp : $(this).find("td.endTemp").html(),
            Duration : $(this).find("td.Duration").html()
        };
        Steps.push(Step);
    });
    return Steps;
}

function packProfile(steps) {
    var ProfileJSON = { 
        "ProfileName" : $("#ProfileName_In").val(),
        "Steps" : steps
    };
    return ProfileJSON;
}


function postProfile(Profile) {
    var xmlhttp = new XMLHttpRequest();
    var theUrl = "/Save";
    xmlhttp.open("POST", theUrl);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify(Profile));
}

function renumberTable() {
    var Steps = [];
    $("#Table-Steps tr").each(function(index){
        var stepIndex = index;
        $(this).find("td.step").html(stepIndex.toString());
    });
    return Steps;
}

function addStep(sT, eT, Dur) {
    var entry = `<tr>
    <td class="step">999</td>
    <td class="startTemp">${sT}</td>
    <td class="endTemp">${eT}</td>
    <td class="Duration">${Dur}</td>
</tr>`;
    
    $Selected = $("#sortableList td.Selected")
    if ($Selected.length) {
        $Selected.after(entry);
    } else {
        $("#sortableList").append(entry);
    }
    return entry
}

function validate() {
    var inputs = [document.getElementById("StartTemp_In"), document.getElementById("EndTemp_In"), document.getElementById("Duration_In")];
    
    isValid = true;

    inputs.forEach(function(entry) {
        if (entry.checkValidity() == true) {
            entry.parentElement.style.outline = "none";
        } else {
            isValid = false;
            entry.parentElement.style.outline = "2px solid red";
        }
    });
    return isValid
}