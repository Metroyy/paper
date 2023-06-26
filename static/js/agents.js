$(document).ready(function () {
    //加载表
    age_select();

    function age_select() {
        // 显示专业逻辑
        // ajax返回数据并生成表格
        //清空表
        $("#custom").empty();
        // 加表头
        var tableHTML = "<thead><tr><td>id</td><td>代理</td></tr></thead>";
        // 传递选项并返回数据
        $.ajax({
            url: "/ageselect/",
            dataType: "json",
            success: function (response) {
                tableHTML += "<tbody>";
                var arr = response.data;
                for (var i = 0; i < arr.length; i++) {
                    tableHTML += "<tr>";
                    for (var j = 0; j < arr[0].length; j++) {
                        tableHTML += "<td>" + arr[i][j] + "</td>";
                    }
                    tableHTML += "</tr>";
                }
                tableHTML += "</tbody>";
                $("#custom").append(tableHTML);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    }

    //根据id查询代理名
    $("#modify_age_id").change(function () {
        var input_id = $("#modify_age_id").val();
        $.ajax({
            url: "/ageselid/",
            type: "GET",
            dataType: "json",
            data: {
                input_id: input_id
            },
            success: function (response) {
                $("#age_name").val(response.data[0][0]);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });

    //修改逻辑
    $("#modifyAgeBtn").click(function () {
        var age_id = $("#modify_age_id").val();
        var age_name = $("#age_name").val();
        $.ajax({
            url: "/modifyage/",
            type: "GET",
            dataType: "json",
            data: {
                age_id: age_id,
                age_name: age_name
            },
            success: function (response) {
                //重新查询
                //加载表
                age_select();
                alert("修改成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("修改失败")
            }
        });
    })

    //新增逻辑
    $("#insertAgeBtn").click(function () {
        var age_name = $("#insert_age_name").val();
        $.ajax({
            url: "/insertage/",
            type: "GET",
            dataType: "json",
            data: {
                age_name: age_name
            },
            success: function (response) {
                //重新查询
                //加载表
                age_select();
                alert("添加成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("添加失败")
            }
        });
    });

    //删除专业
    $("#delAgeBtn").click(function () {
        var age_id = $("#del_age_id").val();
        $.ajax({
            url: "/deleteage/",
            type: "GET",
            dataType: "json",
            data: {
                age_id: age_id
            },
            success: function (response) {
                //重新查询
                //加载表
                age_select();
                alert("删除成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("删除失败")
            }
        });
    })
});