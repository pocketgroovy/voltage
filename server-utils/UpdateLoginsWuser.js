if (typeof database === "undefined") {
    throw "Bad Parameters";
}

InitUpdate();

function InitUpdate()
{
	var start = new Date().getTime();
	
	db = db.getSiblingDB(database);

	var users = db.WUsers.find({"delete_flag":false});
	UpdateLoginBonus(users);

	// stop timer
	var end = new Date().getTime();
	var time = end - start;
	print(":::::end: " + time);
}

function UpdateLoginBonus(users)
{
	users.forEach(function(user)
	{	print("updating user " + user._id);
		var bonus_reset = [{"id": "stamina_potion", "qty":NumberInt(5)},{"id": "coin", "qty":NumberInt(2500)},{"id": "starstone", "qty":NumberInt(5)},{"id": "stamina_potion", "qty":NumberInt(5)}];
		db.WUsers.update({"_id":user._id}, {$set:{"login_bonus_items":bonus_reset, "next_login_bonus_index":NumberInt(0)}});
	});
}