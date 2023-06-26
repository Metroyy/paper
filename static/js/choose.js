$(document).ready(function () {
//单选下拉栏折叠逻辑
    $('.dropdown-toggle').click(function () {
        $(this).siblings('.dropdown-menu').toggle();
    });
    $('.dropdown-item').click(function () {
        var selectedValue = $(this).text();
        $(this).closest('.input-group').find('input').val(selectedValue);
        $(this).closest('.dropdown-menu').hide();
    });
//单选下拉栏数据逻辑
    // ajax返回数据并生成下拉栏选项
    $.ajax({
        url: "/bar/",
        dataType: "json",
        success: function (response) {
            // 清空下拉栏
            $("div[name='school_menu']").empty();
            $("div[name='spe_menu']").empty();
            $("div[name='wri_menu']").empty();
            $("div[name='age_menu']").empty();

            // 添加学校到下拉栏
            response.schools.forEach(function (item) {
                var dropdownItem = $('<a class="dropdown-item" href="#">' + item[0] + '</a>');
                dropdownItem.on('click', function () {
                    var selectedSchool = $(this).text();//获取点击值
                    $('input[name="sch.sch_name"]').val(selectedSchool);//将点击值添加到下拉栏
                    $("div[name='school_menu']").css("display", "none");//点击后关闭下拉栏
                });
                $("div[name='school_menu']").append(dropdownItem);//添加下拉栏值
            });

            // 添加专业到下拉栏
            response.specialists.forEach(function (item) {
                var dropdownItem = $('<a class="dropdown-item" href="#">' + item[0] + '</a>');
                dropdownItem.on('click', function () {
                    var selectedSpecialist = $(this).text();//获取点击值
                    $('input[name="spe.spe_name"]').val(selectedSpecialist);//将点击值添加到下拉栏
                    $("div[name='spe_menu']").css("display", "none");//点击后关闭下拉栏
                });
                $("div[name='spe_menu']").append(dropdownItem);//添加下拉栏值
            });

            // 添加写手到下拉栏
            response.writers.forEach(function (item) {
                var dropdownItem = $('<a class="dropdown-item" href="#">' + item[0] + '</a>');
                dropdownItem.on('click', function () {
                    var selectedWriters = $(this).text();//获取点击值
                    $('input[name="wri.wri_name"]').val(selectedWriters);//将点击值添加到下拉栏
                    $("div[name='wri_menu']").css("display", "none");//点击后关闭下拉栏
                });
                $("div[name='wri_menu']").append(dropdownItem);//添加下拉栏值
            });

            // 添加代理到下拉栏
            response.agents.forEach(function (item) {
                var dropdownItem = $('<a class="dropdown-item" href="#">' + item[0] + '</a>');
                dropdownItem.on('click', function () {
                    var selectedAgents = $(this).text();//获取点击值
                    $('input[name="age.age_name"]').val(selectedAgents);//将点击值添加到下拉栏
                    $("div[name='age_menu']").css("display", "none");//点击后关闭下拉栏
                });
                $("div[name='age_menu']").append(dropdownItem);//添加下拉栏值
            });

        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    });

// 显示列逻辑
    // ajax返回数据并生成表格
    $("#chooseBtn").click(function () {
        // 点击时，先清空表格
        $("#custom").empty();
        var selected = [];//用于存储多选框值
        var selectedTexts = [];//用于存储列表名
        var tableHTML = ""; // 用于存储表格的 HTML 结构
        $("input[name='choose']:checked").each(function () {
            selected.push($(this).val());
            var labelText = $(this).next('label').text(); // 获取多选框后面的标签文本
            selectedTexts.push(labelText);
        });
        if (selected.length > 0) {
            // 加表头
            tableHTML += "<thead><tr><td>id</td>";
            for (var i = 0; i < selectedTexts.length; i++) {
                tableHTML += "<td>" + selectedTexts[i] + "</td>";
            }
            tableHTML += "</tr></thead>";
            // 传递选项并返回数据
            $.ajax({
                url: "/choose/",
                type: "GET",
                dataType: "json",
                data: {
                    selected: selected
                },
                success: function (response) {
                    // 循环赋值
                    tableHTML += "<tbody>";
                    for (var i = 0; i < response.data.length; i++) {
                        tableHTML += "<tr>";
                        tableHTML += "<td>" + (i + 1) + "</td>";
                        for (var j = 0; j < response.data[0].length; j++) {
                            tableHTML += "<td>" + response.data[i][j] + "</td>";
                        }
                        tableHTML += "</tr>";
                    }
                    tableHTML += "</tbody>";

                    // 将完整的表格结构添加到元素中
                    $("#custom").html(tableHTML);
                },
                error: function (xhr, status, error) {
                    console.log(error);
                }
            });
        }
        //关闭下拉栏
        $("#collapseOne").collapse('toggle');
    });
    //点击全选时多选框全选，再次点击反选
    // 初始状态下，全选按钮未选中
    var selectAll = false;
    $("#chooseAll").click(function () {
        selectAll = !selectAll;  // 切换全选状态
        if (selectAll) {
            $("input[name='choose']").prop("checked", true);  // 全选
        } else {
            $("input[name='choose']").prop("checked", false);  // 反选
        }
    });

//查询逻辑
    // ajax返回数据并生成表格
    $("#selectBtn").click(function () {
        $("#custom").empty();// 点击时，先清空表格
        var inputCount = $('#showDiv input[type="text"]').length;// 统计输入框的数量
        var inputNames = $('#showDiv input[type="text"]').map(function () {//获取列名
            return $(this).attr('name');
        }).get();
        var selectData = [];//用于装输入框的输入值
        var selected = [];//用于存储多选框值
        var selectedTexts = [];//用于存储列表名
        var tableHTML = ""; // 用于存储表格的 HTML 结构
        $("input[name='choose']:checked").each(function () {
            selected.push($(this).val());//获取选中的多选框的值
            var labelText = $(this).next('label').text();// 获取列名
            selectedTexts.push(labelText);// 存储列名
        });
        //获取输入框的输入值
        for (var i = 0; i < inputCount; i++) {
            selectData[i] = $('#showDiv input[type="text"]').eq(i).val();
        }
        if (selectData.length > 0) {
            $.ajax({
                url: "/select/",
                type: "GET",
                dataType: "json",
                data: {
                    selected: selected,
                    inputNames: inputNames,
                    selectData: selectData
                },
                success: function (response) {
                    //如果啥也没选，则把默认列名加上，因为默认没选就显示全部列,如果输入框有值，但没选，也把默认列名加上
                    if ((selected.length === 0 && response.length === 0) || (selectData.length > 0 && selected.length === 0)) {
                        // 加表头
                        tableHTML += "<thead><tr><td>id</td>";
                        tableHTML += "<td>学生</td><td>学号</td><td>学生密码</td><td>学生号码</td><td>学生微信</td><td>专业</td><td>学校</td><td>题目</td><td>字数</td><td>查重率</td><td>论文性质</td><td>新增时间</td><td>开题时间</td><td>正文时间</td><td>写手</td><td>写手性质</td><td>代理</td>";
                    } else { //如果是既有选项，又有输入值，则按选项加列名
                        // 加表头
                        tableHTML += "<thead><tr><td>id</td>";
                        for (var i = 0; i < selectedTexts.length; i++) {
                            tableHTML += "<td>" + selectedTexts[i] + "</td>";
                        }
                    }
                    tableHTML += "</tr></thead>";

                    // 循环赋值
                    tableHTML += "<tbody>";
                    for (var i = 0; i < response.data.length; i++) {
                        tableHTML += "<tr>";
                        tableHTML += "<td>" + (i + 1) + "</td>";
                        for (var j = 0; j < response.data[0].length; j++) {
                            tableHTML += "<td>" + response.data[i][j] + "</td>";
                        }
                        tableHTML += "</tr>";
                    }
                    tableHTML += "</tbody>";

                    // 将完整的表格结构添加到元素中
                    $("#custom").html(tableHTML);
                },
                error: function (xhr, status, error) {
                    console.log(error);
                }
            });
        }
        //关闭下拉栏
        $("#collapseTwo").collapse('toggle');
    })

//新增论文逻辑
    //点击提交时获取所有输入框的值
    $("#insertBtn").click(function () {
        var input = [];//输入框的值
        var input_count = $("#insertDiv input").length;//输入框的数量
        var namesArray = $('#insertDiv input[name]').map(function () {// 创建数组来存储输入框name
            return $(this).attr('name');
        }).get();
        //动态提取输入框的val值
        for (var i = 0; i < input_count; i++) {
            input[i] = $("#insertDiv input[name='" + namesArray[i] + "']").val();// 根据name循环取值
        }

        if (input[0] === "") {
            alert("学生姓名不能为空！")
        } else if (input[5] == "") {
            alert("专业不能为空！")
        } else if (input[6] == "") {
            alert("学校不能为空！")
        } else if (input[10] == "") {
            alert("论文性质不能为空！")
        } else if (input[11] == "") {
            alert("新增时间不能为空！")
        } else if (input[14] == "") {
            alert("写手不能为空！")
        } else if (input[15] == "") {
            alert("代理不能为空！")
        } else {
            //ajax将数据提交到后台做处理
            $.ajax({
                url: "/insert/",
                type: "GET",
                dataType: "json",
                data: {
                    input: input
                },
                success: function (response) {
                    alert("添加成功")
                },
                error: function (xhr, status, error) {
                    console.log(error);
                }
            });
        }
        //关闭下拉栏
        $("#collapseThree").collapse('toggle');
    })

//修改论文信息逻辑
    var inputCount = $("#modifyDiv .modify").length-2;//输入框数量
    var oldInputData = [];
    //动态获取输入框的值
    $("#stu_name_input, #pap_title_input").change(function () {
        $(".modify").val("");//先清空数据
        var stu_name = $("#stu_name_input").val();
        var pap_title = $("#pap_title_input").val();
        $.ajax({
            url: "/modifyselect/",
            type: "GET",
            dataType: "json",
            data: {
                stu_name: stu_name,
                pap_title: pap_title
            },
            success: function (response) {
                oldInputData = response.data;
                for (var i=0;i<inputCount;i++){
                    $(".modify").eq(i).val(oldInputData[0][i+1]);
                }
                $(".modify").eq(16).val(oldInputData[0][17]); //代理单独赋值
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });
    $("#modifyBtn").click(function (){
        var modify = []; //存储修改过的数据
        var modifyIndex = 0; // 用于表示 modify 数组的索引位置
        var newInputData = []; //修改后的input值
        for (var i=0;i<inputCount;i++){ //获取修改后的数据
             newInputData[i] = $("#modifyDiv .modify").eq(i).val();
        }
        newInputData[16] = $("#modifyDiv .modify").eq(16).val(); //代理单独赋值
        // for (var i = 12; i <= 13; i++) { //如果开题时间和正文时间都为空则赋值null
        //     if (newInputData[i] === "") {
        //         newInputData[i] = null;
        //     }
        // }
        var rowName =[];//修改后数据的前缀
        for (var i = 0; i < inputCount; i++) {
            if (oldInputData[0][i+1] != newInputData[i]) { // 如果老数据不等于新数据则需要更新
                modify[modifyIndex] = newInputData[i];//修改过的数据存储
                rowName[modifyIndex] = $(".modify").eq(i).attr("name");//修改过数据的name存储
                modifyIndex++; // 递增索引位置
            }
        }
        if (oldInputData[0][17] != newInputData[16]) { // 代理单独判断
                modify[modifyIndex] = newInputData[16];//修改过的数据存储
                rowName[modifyIndex] = $(".modify").eq(i).attr("name");//修改过数据的name存储
            }

        var id = oldInputData[0][0];
        // 假设 modify 是前端传递的修改数据的数组
        for (let i = 0; i < modify.length; i++) {
          if (modify[i] === "") {
            modify[i] = null;
          }
        }

        $.ajax({
            url: "/modify/",
            type: "GET",
            dataType: "json",
            data: {
                id: id,
                rowName: rowName,
                modify: modify
            },
            success: function (response) {
                console.log(response)
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });
});