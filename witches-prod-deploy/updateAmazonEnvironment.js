if ((typeof fromVersion === "undefined") || (typeof toVersion === "undefined") || (typeof futureVersion === "undefined")) {
    throw "Bad Parameters";
}

var ENV_SEPARATOR = '_';

var ENV_PROD = 'prod';
var ENV_STAGING = 's';
var ENV_DEV = 'd';
var OS = 'Amazon';

var ENV_SUFFIX_MAP = {};
ENV_SUFFIX_MAP[ENV_PROD] = '';
ENV_SUFFIX_MAP[ENV_STAGING] = '';
ENV_SUFFIX_MAP[ENV_DEV] = ENV_SEPARATOR + "d";


function updateDBOnRelease(from, to, future){
	updateAmazonDevVersions(to, future);
    createNewProdEnvironment(from, to)
    updateProdCurrentApiFlag(from);
}

function updateAmazonDevVersions(from, to) {
    print("Moving dev versions from " + from + " to " + to);
    
    var environments = getDevEnvironments();
    environments.forEach(function(environment) {
    updateVersionEntries(environment, from, to, OS);
    });
    
    print("Amazon Dev versions upgraded");
}


function getDevEnvironments() {
    return [ ENV_DEV, ENV_STAGING ];
}


function updateVersionEntries(environment, fromBase, toBase, device) {
    var from = fromBase + ENV_SUFFIX_MAP[environment];
    var to = toBase + ENV_SUFFIX_MAP[environment];

    db.Environment.update({'description':environment, 'build_version': from, 'device':device}, { $set: { 'build_version': to } }, { multi: true });
}

function createNewProdEnvironment(fromVersion, toVersion){
    if ( getProdVersionCount(toVersion, OS) <= 0){
        var prod = getProdEnvironment(OS, fromVersion);
        prod.build_version = toVersion;
        prod.current_api = true;
        db.Environment.insert(prod);
        print("inserting new prod environment")
    }
}

function getProdVersionCount(version, device) {
    return db.Environment.find({'description':ENV_PROD, 'build_version': version, 'device':device}).count();
}

function getProdEnvironment(device, version){
    found_environment = db.Environment.findOne({'description':ENV_PROD, 'device':device, 'build_version':version}, {_id:0})
    if ( ! found_environment ){
        print("Error: No Environment found for " + found_environment + ", " + device + ", version " + version);
        quit(1);
    }
    return found_environment
}

function updateProdCurrentApiFlag (version) {
    db.Environment.update({'description': ENV_PROD, 'device':OS, 'build_version': version}, {$set:{'current_api':false}})
}



updateDBOnRelease(fromVersion, toVersion, futureVersion);