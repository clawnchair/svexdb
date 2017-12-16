var data = data_; // get json from template

$( document ).ready(function() {
    $('#more').on('show.bs.modal', function(e) {
        $('#mod_tbl_body').empty();
        var i = $(e.relatedTarget).data('nridx');
        var j = $(e.relatedTarget).data('nrsubidx');
        var slice = data[i];
        $('#mod_title').text(slice[j]['pkmn']);
        function bodyRow(label, info) {
            if (info)
                if (info == "JPN SV Share Sheet")
                    return "\n\t\t<tr><td><b>"+label+"</b></td> <td><a href=\"http://redd.it/2bmrg9\">"+info+"</a></td></tr>\n";
                else if (info == "GameFAQs")
                    return "\n\t\t<tr><td><b>"+label+"</b></td> <td><a href=\"http://redd.it/2cdwrg\">"+info+"</a></td></tr>\n";
                else
                    return "\n\t\t<tr><td><b>"+label+"</b></td> <td>"+info+"</td></tr>\n";
            else
                return "";
        }

        var tbl_str = "\n<table class=\"table table-condensed table-bordered table-hover\">\n<tbody>";
        tbl_str += bodyRow("Source", slice[j]['source']);
        tbl_str += bodyRow("Username", slice[j]['username']);
        tbl_str += bodyRow("Link", slice[j]['url']);
        tbl_str += bodyRow("TSV", slice[j]['tsv']);
        tbl_str += bodyRow("FC", slice[j]['fc']);
        tbl_str += bodyRow("IGN", slice[j]['ign']);
        tbl_str += bodyRow("Info", slice[j]['other']);
        tbl_str += bodyRow("Language", slice[j]['lang']);
        tbl_str += bodyRow("Timestamp", slice[j]['timestamp']);
        tbl_str += "\t</tbody>\n</table>\n";
        $('#mod_tbl_body').append(tbl_str);
    });
});
