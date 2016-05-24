if (typeof database === "undefined") {
    throw "Bad Parameters";
}

InitRemove(database);

function InitRemove()
{
	var start = new Date().getTime();
	
	db = db.getSiblingDB(database);

	var unread_gift_mails = GetUnreadMailsWithGifts();
	UpdateMailGifts(unread_gift_mails);

	// stop timer	
	var end = new Date().getTime();
	var time = end - start;
	print(":::::end: " + time);
}


function GetUnreadMailsWithGifts()
{
	return db.UserMailBox.find({"delete_flag":false, "gifts.id":{$exists:true}});
}


function UpdateMailGifts(mails)
{
	var avatar_item_ids = db.AvatarItems.find({},{"_id":1});

	mails.forEach(function(mail){
		Update(mail, avatar_item_ids);
	});
}

function Update(mail, avatar_item_ids)
{
	var clothing_gifts = [];
	mail.gifts.forEach(function(gift){
		if(IsAvatarItem(gift, avatar_item_ids))
		{
			var avatar_gift = {"id":gift.id, "received_flag":false};
			clothing_gifts.push(avatar_gift)
		}
	});

	db.UserMailBox.update({"_id":mail._id}, {$set:{gifts:clothing_gifts}});
}


function IsAvatarItem(gift, avatar_item_ids)
{	
	var index = avatar_item_ids.count() - 1;
	while(index > 0)
	{
		var is_avatar = false;
		if( avatar_item_ids[index]['_id'] == gift.id)
		{
			is_avatar = true;
			break;
		}
		index--;
	}
	return is_avatar;
}