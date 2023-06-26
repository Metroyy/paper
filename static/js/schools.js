$(document).ready(function () {
    //加载表
    sch_select();

    function sch_select() {
        // 显示专业逻辑
        // ajax返回数据并生成表格
        //清空表
        $("#custom").empty();
        // 加表头
        var tableHTML = "<thead><tr><td>id</td><td>学校</td></tr></thead>";
        // 传递选项并返回数据
        $.ajax({
            url: "/schselect/",
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

    //根据id查询学校名
    $("#modify_sch_id").change(function () {
        var input_id = $("#modify_sch_id").val();
        $.ajax({
            url: "/schselid/",
            type: "GET",
            dataType: "json",
            data: {
                input_id: input_id
            },
            success: function (response) {
                console.log(response.data[0][0]);
                $("#sch_name").val(response.data[0][0]);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });

    //修改逻辑
    $("#modifySchBtn").click(function () {
        var sch_id = $("#modify_sch_id").val();
        var sch_name = $("#sch_name").val();
        $.ajax({
            url: "/modifysch/",
            type: "GET",
            dataType: "json",
            data: {
                sch_id: sch_id,
                sch_name: sch_name
            },
            success: function (response) {
                //重新查询
                //加载表
                sch_select();
                alert("修改成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("修改失败")
            }
        });
    })

    //新增逻辑
    $("#insertSchBtn").click(function () {
        var sch_name = $("#insert_sch_name").val();
        $.ajax({
            url: "/insertspe/",
            type: "GET",
            dataType: "json",
            data: {
                sch_name: sch_name
            },
            success: function (response) {
                //重新查询
                //加载表
                sch_select();
                alert("添加成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("添加失败")
            }
        });
    });

    //删除专业
    $("#delSchBtn").click(function () {
        var sch_id = $("#del_sch_id").val();
        $.ajax({
            url: "/deletesch/",
            type: "GET",
            dataType: "json",
            data: {
                sch_id: sch_id
            },
            success: function (response) {
                //重新查询
                //加载表
                sch_select();
                alert("删除成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("删除失败")
            }
        });
    })
});