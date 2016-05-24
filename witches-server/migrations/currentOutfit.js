// Add current outfit to the player model


function up() {
    db = db.getSiblingDB('witches');
    db.WUsers.update({}, {$set: { current_outfit: [] }}, { multi: true })
}

function down() {
    db = db.getSiblingDB('witches');
    db.WUsers.update({}, {$unset: { current_outfit: '' }}, { multi: true })
}

var revert = revert || false;

if (revert) {
    down();
} else {
    up();
}
    
