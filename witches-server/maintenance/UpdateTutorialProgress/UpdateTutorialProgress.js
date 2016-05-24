const MENDING_LUNA = "Prologue/Prologue/Mending Luna"

function getUsers(){
	db = db.getSiblingDB('witches');
	users = db.WUsers.find({"tutorial_flag":true});
	return users;
}

function findCompletedScenes(user_id){
	completedScenes = db.UserCompletedScenes.find({"user_id":user_id});
	return completedScenes;
}

function isMendingLunaFinished(completed_scenes){
	while(completed_scenes.hasNext()){
		scene = completed_scenes.next();
		if (scene.scene_id == MENDING_LUNA){
			return true;
		}
	}
	return false;
}

function updateUserTutorialProgress(){
	var users = getUsers();
	while(users.hasNext()){
		user = users.next();
		var completedScenes = findCompletedScenes(user._id.valueOf());
		if (isMendingLunaFinished(completedScenes)){
			print("switching off tutorial for user >>>>>> " + user._id);
			db.WUsers.update({_id:user._id}, {$set:{tutorial_flag:false}})
		}
	}
}

updateUserTutorialProgress();