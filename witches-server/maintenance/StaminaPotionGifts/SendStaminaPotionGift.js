

function getSender(){
	db = db.getSiblingDB('witches');
	return db.Characters.findOne({"first_name":"K&C"});
}

function sendStaminaPotionMail(potionCount, message){
	var sender = getSender();
	var currentDate = new Date()
	db.WUsers.find({"tutorial_flag":false}).forEach(function(user){db.UserMailBox.insert({"user_id":user._id.valueOf(), 
		"stamina_potion":NumberInt(potionCount), gifts:[], "title":"", "sender_flag":false, "message_body":message, "sender_id":sender._id.valueOf(),
		"read_flag":false,
		"premium_currency":null, "free_currency":null, "login_bonus_id":"", "stamina_potion_received_flag":false, "premium_received_flag":false, 
		"free_currency_received_flag":false, "multiply_bonus_flag":false, "sender_type_for_metrics":sender.first_name, "delete_flag":false, 
		"install_date":currentDate, "last_updated":currentDate})});
}

sendStaminaPotionMail(potionCount, message);