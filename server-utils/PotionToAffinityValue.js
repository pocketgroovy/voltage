if (typeof database === "undefined") {
    throw "Bad Parameters";
}

InitConversion(database);

function InitConversion(database)
{
	var start = new Date().getTime();
	db = db.getSiblingDB(database);
	
	// find user mails for minigame
	var minigame_mails = GetMinigameMail();

	// sort mail for each player
	var sorted_mail = SortMailByPlayer(minigame_mails);
	
	var user_ids = sorted_mail[0];
	var potion_list = sorted_mail[1];
	var potion_ids = Object.keys(potion_list); // only potions users needs to convert

	// get the affinity values for each potion in dict. potion id as a key and value as a value
	var potion_effect_map = GetPotionEffectMap(potion_ids);
	
	// give the values to users in each backet
	UpdatePlayerAffinity(user_ids, potion_effect_map);

	// stop timer
	var end = new Date().getTime();
	var time = end - start;
	print(":::::end: " + time);

}

function GetMinigameMail()
{
	var minigame_mails = db.UserMailBox.find({message_body:"Minigame Result Potion", "gifts.received_flag":false, "delete_flag":false});
	return minigame_mails;
}

function GetPotionEffectMap(potion_ids)
{
	var potion_values = {};
	for (var i = 0; i < potion_ids.length; i++)
	{
		var potion_id = potion_ids[i];
		var potion = db.Potions.find({_id: ObjectId(potion_id), "delete_flag":false})[0];
		potion_values[potion_id] = potion.effect_list[0];
	}

	return potion_values;
}

function UpdatePlayerAffinity(user_ids, potion_effect_map) 
{	
	Object.keys(user_ids).forEach(function(user_id)
	{			
		var user_doc = db.WUsers.findOne({_id:ObjectId(user_id), "delete_flag":false});
		if (user_doc !== null)
		{ 
			var updated_affinity = UpdateAffinities(user_id, user_ids, potion_effect_map);

			db.WUsers.update({_id:ObjectId(user_id)}, {$set:{"affinity_update":updated_affinity, update_client:true}});
			db.UserMailBox.remove({"user_id":user_id, "message_body":"Minigame Result Potion"});
		}
		else
		{
			print("User: " + user_id + ", not found in WUsers table");
		}
	});
}

function UpdateAffinities(user_id, user_ids, potion_effect_map)
{
	var updated_affinity = {"A":0, "R":0, "M":0, "T":0, "N":0};

	Object.keys(user_ids[user_id]).forEach(function(potion)
	{
		var quantity = user_ids[user_id][potion];

		var effect_keys = Object.keys(potion_effect_map[potion]);
		effect_keys.forEach(function(character)
		{
			var value = potion_effect_map[potion][character];
			updated_affinity[character] += (value * quantity);
		});
	});

	return updated_affinity;
}

function SortMailByPlayer(mails)
{	
	var user_ids = {};
	var potion_list = {};
	mails.forEach(function(mail)
	{	
		// modify 2 lists as side effect
		UserMails(mail, user_ids, potion_list);	
	});
	return [user_ids, potion_list];
}

function UserMails(mail, user_ids, potion_list)
{	
	var potion_id = mail.gifts[0].id;
	CreatePotionSet(potion_id, potion_list);

	var id = mail.user_id;

	if(!(id in user_ids))
	{
		user_ids[id] = {};
	}

	if(!(potion_id in user_ids[id]))
	{
		user_ids[id][potion_id] = 0;
	}

	user_ids[id][potion_id]++;
}

function CreatePotionSet(potion_id, potion_list)
{
	if (!(potion_id in potion_list))
	{
		potion_list[potion_id] = true;
	}
	return potion_list
}




