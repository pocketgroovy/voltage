if ((typeof fromVersion === "undefined") || (typeof toVersion === "undefined") || (typeof futureVersion === "undefined")) {
    throw "Bad Parameters";
}

var ENV_SEPARATOR = '_';

var ENV_PROD = 'prod';
var ENV_STAGING = 's';
var ENV_DEV = 'd';

var ENV_SUFFIX_MAP = {};
ENV_SUFFIX_MAP[ENV_PROD] = '';
ENV_SUFFIX_MAP[ENV_STAGING] = '';
ENV_SUFFIX_MAP[ENV_DEV] = ENV_SEPARATOR + "d";

var ANDROID = 'Android'
var IOS = 'IPhonePlayer'
var OSX = 'OSXEditor'
var WIN = 'WindowsEditor'


function upgradeVersion(from, to, future) {
    db = db.getSiblingDB("witches");
    validateOldProductionVersion(from);
    validateFutureVersion(to, future);
    // upgrade any previous versions that exist for the desired new production version
    var toBase = getBaseVersion(to);
    var futureBase = getBaseVersion(future);

    updateDevVersions(toBase, futureBase);
    updateiOSCurrentApiFlag(ENV_PROD, from);
}

function updateDevVersions(fromBase, toBase) {
    print("Moving dev versions from " + fromBase + " to " + toBase);
    
    var environments = getDevEnvironments();
    environments.forEach(function(environment) {
    updateVersionEntries(environment, fromBase, toBase, ANDROID);
    updateVersionEntries(environment, fromBase, toBase, OSX);
    updateVersionEntries(environment, fromBase, toBase, WIN);
    });
    
    print("Dev versions upgraded");
}

function updateiOSCurrentApiFlag (environment, version) {
    db.Environment.update({'description':environment, 'build_version':version, 'device':IOS}, {$set:{'current_api':false}});
}

function updateVersionEntries(environment, fromBase, toBase, device) {
    var from = fromBase + ENV_SUFFIX_MAP[environment];
    var to = toBase + ENV_SUFFIX_MAP[environment];

    db.Environment.update({'description':environment, 'build_version': from, 'device':device}, { $set: { 'build_version': to } }, { multi: true });
}

function getBaseVersion(version) {
    return version.split(ENV_SEPARATOR);
}

function validateOldProductionVersion(version) {
    if (getVersionCount(version) <= 0) {
        print("Error: No versions found matching " + version);
        quit(1);
    }
}

function validateFutureVersion(prodVersion, futureVersion) {
    if (prodVersion == futureVersion) {
        print("Error: Attempting to migrate to a future version which is the same as the desired production version!");
        quit(1);
    }
}

function getDevEnvironments() {
    return [ ENV_DEV, ENV_STAGING ];
}

function getVersionCount(version) {
    return db.Environment.find({'build_version': version}).count();
}

upgradeVersion(fromVersion, toVersion, futureVersion);
