source_url = "http://127.0.0.1:8000/"

function get_chain() {
    $("#transaction-details").css("display","None");
    $.ajax({
        url: source_url+"get_chain",
        type: "GET",
        success: function(data) {
            console.log(data);
            if(data.length === 0) {
                $("#result").html("No records found");
            } else {
                $("#result").html("The length of the chain is: "+data['length']);
                let chain = data['chain']
                for(let block in data['chain']) {
                    $("#result").append("<br><br><br><br>index: "+chain[block]['index']);
                    $("#result").append("<br><br>timestamp: "+chain[block]['timestamp']);
                    $("#result").append("<br><br>transaction: ");
                    let transactions = chain[block]['transactions'];
                    if(transactions.length==0) $("#result").append("None");
                    else {
                        for(let i=0;i<transactions.length;++i) {
                            $("#result").append("<br><br>sender: "+transactions[i]['sender']);
                            $("#result").append("<br>receiver: "+transactions[i]['receiver']);
                            $("#result").append("<br>amount: "+transactions[i]['amount']);
                        }
                    }
                    $("#result").append("<br><br>nonce: "+chain[block]['nonce']);
                    $("#result").append("<br><br>previous hash: "+chain[block]['previous_hash']);
                }
            }
        },
        error: function(data) {
            console.log(data);
            $("#result").html(data.responseJSON.message);
        }
    });
}

function verify_chain() {
    $("#transaction-details").css("display","None");
    $.ajax({
        url: source_url+"is_valid",
        type: "GET",
        success: function(data) {
            console.log(data);
            if(data.length === 0) {
                $("#result").html("No records found");
            } else {
                $("#result").html(data['message']);
            }
        },
        error: function(data) {
            console.log(data);
            $("#result").html(data.responseJSON.message);
        }
    });
}

function mine_block() {
    $("#transaction-details").css("display","None");
    $.ajax({
        url: source_url+"mine_block",
        type: "GET",
        success: function(data) {
            console.log(data);
            if(data.length === 0) {
                $("#result").html("No records found");
            } else {
                $("#result").html(data['message']);
            }
        },
        error: function(data) {
            console.log(data);
            $("#result").html(data.responseJSON.message);
        }
    });
}

function new_transaction() {
    $("#transaction-details").css("display","Block");
}

function add_transaction() {
    let sender = $("#transaction-sender").val();
    let receiver = $("#transaction-receiver").val();
    let amount = $("#transaction-amount").val();
    $.ajax({
        url: source_url+"add_transaction",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({"sender":sender,"receiver":receiver,"amount":amount}),
        success: function(data) {
            console.log(data);
            if(data.length === 0) {
                $("#result").html("No records found");
            } else {
                $("#result").html(data['message']);
            }
        },
        error: function(data) {
            console.log(data);
            $("#result").html(data.responseJSON.message);
        }
    });
}