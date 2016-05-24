if ((typeof fromVersion === "undefined") || (typeof toVersion === "undefined") || (typeof futureVersion === "undefined")) {
    throw "Bad Parameters";
}

var ENV_SEPARATOR = '_';

var ENV_PROD = 'prod';
var ENV_STAGING = 's';
var ENV_DEV = 'd';
var IOS = 'IPhonePlayer';

var ENV_SUFFIX_MAP = {};
ENV_SUFFIX_MAP[ENV_PROD] = '';
ENV_SUFFIX_MAP[ENV_STAGING] = '';
ENV_SUFFIX_MAP[ENV_DEV] = ENV_SEPARATOR + "d";


function updateDBOnRelease(from, to, future){
	updateiOSDevVersions(to, future);
    createNewProdEnvironment(from, to)
    updateProdCurrentApiFlag(from);
}

function updateiOSDevVersions(from, to) {
    print("Moving dev versions from " + from + " to " + to);
    
    var environments = getDevEnvironments();
    environments.forEach(function(environment) {
    updateVersionEntries(environment, from, to, IOS);
    });
    
    print("iOS Dev versions upgraded");
}


function updateProdCurrentApiFlag (version) {
    db.Environment.update({'description': ENV_PROD, 'device':IOS, 'build_version': version}, {$set:{'current_api':false}})
}

function createNewProdEnvironment(fromVersion, toVersion){
    print("before inserting new prod environment")
    if ( getProdVersionCount(toVersion, IOS) <= 0){
        var prod = getProdEnvironment(IOS, fromVersion);
        prod.build_version = toVersion;
        prod.current_api = true;
        db.Environment.insert(prod);
        print("inserting new prod environment")
    }
}

function updateVersionEntries(environment, fromBase, toBase, device) {
    var from = fromBase + ENV_SUFFIX_MAP[environment];
    var to = toBase + ENV_SUFFIX_MAP[environment];

    db.Environment.update({'description':environment, 'build_version': from, 'device':device}, { $set: { 'build_version': to } }, { multi: true });
}

function getDevEnvironments() {
    return [ ENV_DEV, ENV_STAGING ];
}

function getProdEnvironment(device, version){
    found_environment = db.Environment.findOne({'description':ENV_PROD, 'device':device, 'build_version':version}, {_id:0})
    if ( ! found_environment ){
        print("Error: No Environment found for " + found_environment + ", " + device + ", version " + version);
        quit(1);
    }
    return found_environment
}
function getProdVersionCount(version, device) {
    return db.Environment.find({'description':ENV_PROD, 'build_version': version, 'device':device}).count();
}

updateDBOnRelease(fromVersion, toVersion, futureVersion);