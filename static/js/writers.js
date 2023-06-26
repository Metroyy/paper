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

    //加载表
    wri_select();

    function wri_select() {
        // 显示专业逻辑
        // ajax返回数据并生成表格
        //清空表
        $("#custom").empty();
        // 加表头
        var tableHTML = "<thead><tr><td>id</td><td>写手</td><td>写手性质</td></tr></thead>";
        // 传递选项并返回数据
        $.ajax({
            url: "/writers/",
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

    //根据id查询写手名
    $("#modify_wri_id").change(function () {
        var wri_id = $("#modify_wri_id").val();
        $.ajax({
            url: "/wriselid/",
            type: "GET",
            dataType: "json",
            data: {
                wri_id: wri_id
            },
            success: function (response) {
                $("#wri_name").val(response.data[0][0]);
                $("#wri_class").val(response.data[0][1]);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });

    //修改逻辑
    $("#modifyWriBtn").click(function () {
        var wri_id = $("#modify_wri_id").val();
        var wri_name = $("#wri_name").val();
        var wri_class = $("#wri_class").val();
        $.ajax({
            url: "/modifywri/",
            type: "GET",
            dataType: "json",
            data: {
                wri_id: wri_id,
                wri_name: wri_name,
                wri_class: wri_class
            },
            success: function (response) {
                //重新查询
                //加载表
                wri_select();
                alert("修改成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("修改失败")
            }
        });
    })

    //新增逻辑
    $("#insertWriBtn").click(function () {
        var wri_name = $("#insert_wri_name").val();
        var wri_class = $("#insert_wri_class").val();
        $.ajax({
            url: "/insertwri/",
            type: "GET",
            dataType: "json",
            data: {
                wri_name: wri_name,
                wri_class: wri_class
            },
            success: function (response) {
                //重新查询
                //加载表
                wri_select();
                alert("添加成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("添加失败")
            }
        });
    });

    //删除专业
    $("#delWriBtn").click(function () {
        var wri_id = $("#del_wri_id").val();
        $.ajax({
            url: "/deletewri/",
            type: "GET",
            dataType: "json",
            data: {
                wri_id: wri_id
            },
            success: function (response) {
                //重新查询
                //加载表
                wri_select();
                alert("删除成功")
            },
            error: function (xhr, status, error) {
                console.log(error);
                alert("删除失败")
            }
        });
    })
});