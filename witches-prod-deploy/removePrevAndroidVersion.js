if (typeof version === "undefined"){
    throw "Bad Parameters";
}


var ENV_PROD = 'prod';
var ANDROID = 'Android';


function removeProdVersion(version){
	removePrevAndroidVersion(ENV_PROD, version);
}


function removePrevAndroidVersion(environment, version){
	db.Environment.remove({'description':environment,'build_version':version, 'device':ANDROID});
}

removeProdVersion(version);