if ((typeof fromVersion === "undefined") || (typeof toVersion === "undefined")) {
    throw "Bad Parameters";
}

var ANDROID = 'Android';
var IOS = 'IPhonePlayer';
var ENV_PROD = 'prod';
var ENV_STAGING = 's';

function updateEnvironment(fromVersion, toVersion, futureVersion){
	db = db.getSiblingDB("witches");
	createAndroidProdEnvironment(fromVersion, toVersion);
	updateCurrentApiFlag(ENV_PROD, fromVersion, ANDROID);
}

function updateCurrentApiFlag(environment, version, device){
	db.Environment.update({'description':environment, 'build_version':version, 'device':device}, {$set:{'current_api': false}})
}

function createAndroidProdEnvironment(fromVersion, toVersion){
	if ( getProdVersionCount(toVersion, ANDROID) <= 0){
		var prod = getEnvironment(ENV_PROD, ANDROID, fromVersion);
		prod.build_version = toVersion;
		prod.current_api = true;
		db.Environment.insert(prod);
	}
}

function getEnvironment(environment, device, version){
	found_environment = db.Environment.findOne({'description':environment, 'device':device, 'build_version':version}, {_id:0})
	if ( ! found_environment ){
		print("Error: No Environment found for " + found_environment + ", " + device + ", version " + version);
    	quit(1);
	}
	return found_environment
}

function getProdVersionCount(version, device) {
    return db.Environment.find({'description':ENV_PROD, 'build_version': version, 'device':device}).count();
}

updateEnvironment(fromVersion, toVersion, futureVersion);