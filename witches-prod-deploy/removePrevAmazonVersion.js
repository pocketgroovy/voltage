if (typeof version === "undefined"){
    throw "Bad Parameters";
}


var ENV_PROD = 'prod';
var OS = 'Amazon';


function removeProdVersion(version){
	removePrevAmazonVersion(ENV_PROD, version);
}

function removePrevAmazonVersion(environment, version){
	db.Environment.remove({'description':environment,'build_version':version, 'device':OS});
}

removeProdVersion(version);