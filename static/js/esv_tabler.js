function formatOutput(resultID, fillerID) {
    document.getElementById(resultID).innerHTML = "";
    var dumpString = document.getElementById("dump").value;

    var box_re = /[Bb]\d{2,4}/;
    var row_re = /\d,/;
    var col_re = /,\d/;
    var esv_re = /\d\d\d\d/;
    splitString = dumpString.replace(/^\n$/g, "").split("\n");

    var current_box_num = 0;
    var current_row_num = 0;
    var current_col_num = 0;
    var boxes_store = {};

    function processLine(line) {
        var box_match = box_re.exec(line);
        var row_match = row_re.exec(line);
        var col_match = col_re.exec(line);
        var esv_match = esv_re.exec(line);

        var box_num, row_num, col_num;

        if (box_match) {
            box_num = box_match[0];
            if (box_num != current_box_num) {
                current_box_num = box_num;
                boxes_store[box_num] = [];
            }
        }

        if (esv_match) {
            if (box_match && row_match && col_match) {
                row_num = parseInt(row_match[0][0]);
                col_num = parseInt(col_match[0].substring(1,3));

                boxes_store[box_num][(6 * (row_num - 1) + col_num)] = esv_match[0]
            }
        }
    }

    for (var i = 0; i < splitString.length; i++) {
        var line = splitString[i];
        processLine(line);
    }

    var blank = document.getElementById(fillerID).value;
    for (var box in boxes_store) {
        var str = "# Box " + box.substring(1,box.length) + "<br>| " + box +
                  " | C1 | C2 | C3 | C4 | C5 | C6 |<br>|:--:|:--:|:--:|:--:|:--:|:--:|:--:|";
        for (var i = 1; i <= 30; i++) {
            if (i % 6 == 1) {
                r = Math.floor(i / 6) + 1;
                str += "<br>|**R" + r + "**| ";
            }
            if (boxes_store[box][i]) {
                str += boxes_store[box][i] + " | ";
            }
            else {
                str += blank + " | ";
            }
        }
        str += "<br><br>";
        document.getElementById(resultID).innerHTML += str;
    }
}
