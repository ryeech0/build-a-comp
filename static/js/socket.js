// Initialize socketio
const socket = io()

// Load data when DOM is ready
$(document).ready(function() {
    var map = $("#mapFilterBtn").html().trim().toLowerCase();
    // console.log(map);
    socket.emit("map_selected", map);
});

// Refresh table when new map is selected
$(".dropdown-menu .dropdown-item").on("click", function(e) {
    e.preventDefault();
    var map = $(this).html().trim().toLowerCase();
    // console.log(map);
    socket.emit("map_selected", map);
});

// Receive data from back-end and display in table
socket.on("map_data_sent", function(data) {
    $("#agent-stats-table > tbody").each(function(tb_idx) {
        $(this).find("tr").each(function(row_idx) {
            var agent = $(this).attr("data-agent");
            var pickrate = (data[agent]["pickrate"] * 100).toFixed(2);
            var winrate = (data[agent]["winrate"] * 100).toFixed(2);
            $(this).find("td[data-stat='pickrate']").text(pickrate.toString() + "%");
            $(this).find("td[data-stat='winrate']").text(winrate.toString() + "%");
        });
    });
    if (window.applyStatsSort) window.applyStatsSort();
});