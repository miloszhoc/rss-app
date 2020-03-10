function delete_ajax(id, url) {
    $.ajax({
        type: "DELETE",
        url: url + "/urls/" + id,
        dataType: "text",
        contentType: "text/plain",
        success: function () {
            alert("URL Deleted.");
            $("#urls").load(location.href + " #urls");
        }
    });
}

function put_ajax(id, data, url) {
    let full_url = url + '/urls/' + id;

    console.log(full_url);
    return $.ajax({
        type: 'PUT',
        url: full_url,
        data: {'url': data},
        success: function () {
            alert("URL modified");
            $("#urls").load(location.href + " #urls");
        }
    });
}

function show_hide(element_id) {

    let update_section = document.getElementById(element_id);

    if (update_section.style.display === "none") {
        update_section.style.display = 'block';
    } else {
        update_section.style.display = 'none';
    }
}

function fill_frame(content) {
    document.querySelector('iframe').contentDocument.write(content);
    document.close();
}
