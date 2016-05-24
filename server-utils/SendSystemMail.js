if (typeof database === "undefined") {
    throw "Bad Parameters";
}

InitSendMail(database);

function InitSendMail(database)
{
	var start = new Date().getTime();

	var start = new Date().getTime();
	db = db.getSiblingDB(database);

	var users_with_mail = GetUserWithMail();
	var users_without_mail = GetUserWithoutMail(users_with_mail);
	SendUserSystemMail(users_without_mail);

	// stop timer
	var end = new Date().getTime();
	var time = end - start;
	print(":::::end: " + time);
}

function GetUserWithMail()
{
	print("GetUserWithMail");
	var user_with_mail = db.UserMailBox.find({message_body:"We apologize for the issues people have experienced with our daily login bonus. These issues should now be resolved, and to thank you for your patience, please accept these gifts!", "delete_flag":false});
	return user_with_mail;
}


function GetUserWithoutMail(users_with_mail)
{
	print("GetUserWithoutMail");
	users_without_mail_id = []
	users_with_mail.forEach(function(user_mail){
		print("user id : " + user_mail.user_id);
		users_without_mail_id.push(ObjectId(user_mail.user_id));
	});

	
	print(users_without_mail_id);
	var users_without_mail = db.WUsers.find({"_id":{$nin:users_without_mail_id}});
	print("users_without_mail: "+users_without_mail);

	return users_without_mail;
}

// function SendUserSystemMail(users_without_mail)
// {

// 	users_without_mail.forEach(function(user){
// 				print("user " + user._id);
// 				user_id = user._id.valueOf();

// 		db.UserMailBox.insert({message_body:"Sorry I couldn't clear up the storm, but this should make up for it!", 
// 			stamina_potion:NumberInt(5), premium_currency:NumberInt(5), sender_id:"555b8d63a310ff3a35ebba05", stamina_potion_received_flag:false, sender_flag:false, gifts:[], 
// 			premium_received_flag:false, free_currency_received_flag:false, free_currency:null, sender_type_for_metrics:"K&C", user_id:user_id, read_flag:false})
// 	});


// }

function SendUserSystemMail(users_without_mail)
{
	users_without_mail.forEach(function(user){
		print("user " + user._id);
		user_id = user._id.valueOf();
		var bulk = db.UserMailBox.initializeUnorderedBulkOp();
		var today = new Date();
		bulk.insert({message_body:"We apologize for the issues people have experienced with our daily login bonus. These issues should now be resolved, and to thank you for your patience, please accept these gifts!", 
			stamina_potion:NumberInt(5), premium_currency:NumberInt(5), sender_id:"555b8d63a310ff3a35ebba05", stamina_potion_received_flag:false, sender_flag:false, gifts:[], 
			premium_received_flag:false, free_currency_received_flag:false, free_currency:null, sender_type_for_metrics:"K&C", user_id:user_id, read_flag:false, delete_flag:false,
			title:"", multiply_bonus_flag:false, login_bonus_id:"", EI:null, install_date:today, last_updated:today});
		bulk.execute();
	});
}