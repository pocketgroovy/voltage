if (typeof version === "undefined"){
    throw "Bad Parameters";
}


var ENV_PROD = 'prod';
var IOS = 'IPhonePlayer';


function removeProdVersion(version){
	removePrevIOSVersion(ENV_PROD, version);
}


function removePrevIOSVersion(environment, version){
	db.Environment.remove({'description':environment,'build_version':version, 'device':IOS});
}

removeProdVersion(version);