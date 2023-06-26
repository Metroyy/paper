$(document).ready(function () {
    //加载表
    spe_select();

    function spe_select() {
        // 显示专业逻辑
        // ajax返回数据并生成表格
        //清空表
        $("#custom").empty();
        // 加表头
        var tableHTML = "<thead><tr><td>id</td><td>专业</td></tr></thead>";
        // 传递选项并返回数据
        $.ajax({
            url: "/speselect/",
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

    //根据id查询专业名
    $("#spe_id").change(function () {
        var input_id = $("#spe_id").val();
        $.ajax({
            url: "/speselid/",
            type: "GET",
            dataType: "json",
            data: {
                input_id: input_id
            },
            success: function (response) {
                console.log(response.data[0][0])
                $("#spe_name").val(response.data[0][0]);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });

    //修改逻辑
    $("#modifySpeBtn").click(function () {
        var spe_id = $("#spe_id").val();
        var spe_name = $("#spe_name").val();
        $.ajax({
            url: "/modifyspe/",
            type: "GET",
            dataType: "json",
            data: {
                spe_id: spe_id,
                spe_name: spe_name
            },
            success: function (response) {
                //重新查询
                //加载表
                spe_select();
                alert("修改成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("修改失败")
            }
        });
    })

    //新增逻辑
    $("#insertSpeBtn").click(function () {
        var spe_name = $("#insert_spe_name").val();
        $.ajax({
            url: "/insertspe/",
            type: "GET",
            dataType: "json",
            data: {
                spe_name: spe_name
            },
            success: function (response) {
                //重新查询
                //加载表
                spe_select();
                alert("添加成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("添加失败")
            }
        });
    });

    //删除专业
    $("#delSpeBtn").click(function () {
        var spe_id = $("#del_spe_id").val();
        $.ajax({
            url: "/deletespe/",
            type: "GET",
            dataType: "json",
            data: {
                spe_id: spe_id
            },
            success: function (response) {
                //重新查询
                //加载表
                spe_select();
                alert("删除成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("删除失败")
            }
        });
    })
});