// A script to re-deliver bulk mail that failed to fully send to all users. The mail is identified by the message, in this case
// Run with a line like:
// mongo --host <host> <javascript path>

var MSG = "We apologize for the issues people have experienced with our daily login bonus. These issues should now be resolved, and to thank you for your patience, please accept these gifts!";

rs.slaveOk(); // allow distinct queries in a slave environment

db = db.getSiblingDB('witches');

var _bulk_operation;
var _affectedUsers = [];
var BULK_SIZE = 100;

function resendMail() {
    var users_with_mail = findUsersWithMail();
    var users_without_mail = db.WUsers.find({"_id": { $nin: users_with_mail } }, { "_id": 1 });

    var user_id;
    users_without_mail.forEach(function(row) {
	user_id = row._id.valueOf();
	sendMail(user_id);
    });

    processBulkOperation();
}

function findUsersWithMail() {
    var cursor = db.UserMailBox.find({ "message_body": MSG }, { "_id": 0, "user_id": 1 });
    var users = cursor.map(function(row) { return ObjectId(row.user_id); });
    return users;
}

function processBulkOperation() {
    if (!_bulk_operation) {
	return;
    }
    
    var numRecords = _affectedUsers.length;
    var results = _bulk_operation.execute();

    if (results.nInserted !== numRecords) {
	throw "Error occurred during insert!";
    }

    _affectedUsers.forEach(function(affectedUser) {
	print(affectedUser);
    });

    _bulk_operation = null;
    _affectedUsers = [];
}


function sendMail(userID) {
    var mailMessage = {
	"message_body": MSG,
	"read_flag": false,
	"EI": null,
	"stamina_potion": 5,
	"title": "",
	"premium_currency": null,
	"sender_id": "555b8d63a310ff3a35ebba05",
	"stamina_potion_received_flag": false,
	"sender_flag": false,
	"gifts": [
	    {
		"id": "54da8ad66f983f60ee01f7de",
		"received_flag": false
	    }
	],
	"premium_received_flag": false,
	"multiply_bonus_flag": false,
	"user_id": userID,
	"free_currency": 600,
	"sender_type_for_metrics": "K&C",
	"delete_flag": false,
	"install_date": new ISODate(),
	"last_updated": new ISODate()
    };

    _bulk_operation = _bulk_operation || db.UserMailBox.initializeUnorderedBulkOp();
    _bulk_operation.insert(mailMessage);
    _affectedUsers.push(userID)

    if (_affectedUsers.length >= BULK_SIZE) {
	processBulkOperation();
    }
}

resendMail();
