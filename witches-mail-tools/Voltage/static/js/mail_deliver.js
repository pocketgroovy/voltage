/**
 * Created by yoshi.miyamoto on 9/4/15.
 */


window.onload = function () {
    document.getElementById('check_all_items').onclick = disableItems2and3;
};

function disableItems2and3() {
    var is_all_item_checked = document.getElementById('check_all_items').checked;
    if (is_all_item_checked) {
        document.getElementById("sel_ingredients").style.visibility = "hidden";
        document.getElementById("sel_potions").style.visibility = "hidden";
        document.getElementById("sel_avatarItems").style.visibility = "hidden";
        document.getElementById("item_type2").disabled = true;
        document.getElementById("item_type3").disabled = true;
        document.getElementById("quantity2").disabled = true;
        document.getElementById("quantity_label2").innerHTML = "disabled";
        document.getElementById("quantity3").disabled = true;
        document.getElementById("quantity_label3").innerHTML = "disabled";

        resetSelection("sel_item_ids1[]");
        resetSelection("sel_item_ids2[]");
        resetSelection("sel_item_ids3[]");
        disableItem2and3Selections();
    }
    else {
        document.getElementById("item_type2").disabled = false;
        document.getElementById("item_type3").disabled = false;
        document.getElementById("quantity2").disabled = false;
        document.getElementById("quantity_label2").innerHTML = "Quantity";
        document.getElementById("quantity3").disabled = false;
        document.getElementById("quantity_label3").innerHTML = "Quantity";
    }
}

function disableItem2and3Selections() {
    document.getElementById("sel_ingredients2").style.visibility = "hidden";
    document.getElementById("sel_potions2").style.visibility = "hidden";
    document.getElementById("sel_avatarItems2").style.visibility = "hidden";
    document.getElementById("sel_ingredients3").style.visibility = "hidden";
    document.getElementById("sel_potions3").style.visibility = "hidden";
    document.getElementById("sel_avatarItems3").style.visibility = "hidden";

}

function selection_switch(value) {
    if (value == "ingredients") {
        document.getElementById("check_all_items").checked = false;
        document.getElementById("check_all_items").style.visibility = "visible";
        document.getElementById("check_all_items_label").style.visibility = "visible";
        document.getElementsByClassName("quantity")[0].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[1].style.visibility = "hidden";

        document.getElementById("sel_ingredients").style.visibility = "visible";
        document.getElementById("sel_potions").style.visibility = "hidden";
        document.getElementById("sel_avatarItems").style.visibility = "hidden";
    }
    else if (value == "potions") {
        document.getElementById("check_all_items").checked = false;
        document.getElementById("check_all_items").style.visibility = "visible";
        document.getElementById("check_all_items_label").style.visibility = "visible";
        document.getElementsByClassName("quantity")[0].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[1].style.visibility = "hidden";

        document.getElementById("sel_ingredients").style.visibility = "hidden";
        document.getElementById("sel_potions").style.visibility = "visible";
        document.getElementById("sel_avatarItems").style.visibility = "hidden";
    }
    else if (value == "avatar_items") {
        document.getElementById("check_all_items").checked = false;
        document.getElementById("check_all_items").style.visibility = "visible";
        document.getElementById("check_all_items_label").style.visibility = "visible";

        document.getElementsByClassName("quantity")[0].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[1].style.visibility = "hidden";

        document.getElementById("sel_ingredients").style.visibility = "hidden";
        document.getElementById("sel_potions").style.visibility = "hidden";
        document.getElementById("sel_avatarItems").style.visibility = "visible";
    }
    else if (value == "starstones" || value == "coins" || value == "avatar_items" || value == "stamina_potions") {
        document.getElementById("check_all_items").style.visibility = "hidden";
        document.getElementById("check_all_items_label").style.visibility = "hidden";
        document.getElementsByClassName("quantity")[0].style.visibility = "visible";
        document.getElementsByClassName("quantity")[1].style.visibility = "visible";

        document.getElementById("sel_ingredients").style.visibility = "hidden";
        document.getElementById("sel_potions").style.visibility = "hidden";
        document.getElementById("sel_avatarItems").style.visibility = "hidden";
    }
    else {
        document.getElementById("check_all_items").checked = false;
        document.getElementsByClassName("quantity")[0].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[1].style.visibility = "hidden";

        document.getElementById("sel_ingredients").style.visibility = "hidden";
        document.getElementById("sel_potions").style.visibility = "hidden";
        document.getElementById("sel_avatarItems").style.visibility = "hidden";
        resetSelection("sel_item_ids1[]");
    }
}

function resetSelection(name) {
    var options = document.getElementsByName(name);
    for (var i = 0; i < options.length; i++) {
        options[i].value = "";
    }
}


function selection_switch2(value) {
    if (value == "ingredients") {
        document.getElementsByClassName("quantity")[3].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[2].style.visibility = "hidden";

        document.getElementById("sel_ingredients2").style.visibility = "visible";
        document.getElementById("sel_potions2").style.visibility = "hidden";
        document.getElementById("sel_avatarItems2").style.visibility = "hidden";
    }
    else if (value == "potions") {
        document.getElementsByClassName("quantity")[3].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[2].style.visibility = "hidden";

        document.getElementById("sel_ingredients2").style.visibility = "hidden";
        document.getElementById("sel_potions2").style.visibility = "visible";
        document.getElementById("sel_avatarItems2").style.visibility = "hidden";
    }
    else if (value == "avatar_items") {
        document.getElementsByClassName("quantity")[3].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[2].style.visibility = "hidden";

        document.getElementById("sel_ingredients2").style.visibility = "hidden";
        document.getElementById("sel_potions2").style.visibility = "hidden";
        document.getElementById("sel_avatarItems2").style.visibility = "visible";
    }
    else if (value == "starstones" || value == "coins" || value == "avatar_items" || value == "stamina_potions") {
        document.getElementsByClassName("quantity")[3].style.visibility = "visible";
        document.getElementsByClassName("quantity")[2].style.visibility = "visible";

        document.getElementById("sel_ingredients2").style.visibility = "hidden";
        document.getElementById("sel_potions2").style.visibility = "hidden";
        document.getElementById("sel_avatarItems2").style.visibility = "hidden";
    }
    else {
        document.getElementsByClassName("quantity")[3].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[2].style.visibility = "hidden";

        document.getElementById("sel_ingredients2").style.visibility = "hidden";
        document.getElementById("sel_potions2").style.visibility = "hidden";
        document.getElementById("sel_avatarItems2").style.visibility = "hidden";
        resetSelection("sel_item_ids2[]");
    }
}


function selection_switch3(value) {
    if (value == "ingredients") {
        document.getElementsByClassName("quantity")[5].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[4].style.visibility = "hidden";

        document.getElementById("sel_ingredients3").style.visibility = "visible";
        document.getElementById("sel_potions3").style.visibility = "hidden";
        document.getElementById("sel_avatarItems3").style.visibility = "hidden";
    }
    else if (value == "potions") {
        document.getElementsByClassName("quantity")[5].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[4].style.visibility = "hidden";

        document.getElementById("sel_ingredients3").style.visibility = "hidden";
        document.getElementById("sel_potions3").style.visibility = "visible";
        document.getElementById("sel_avatarItems3").style.visibility = "hidden";
    }
    else if (value == "avatar_items") {
        document.getElementsByClassName("quantity")[5].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[4].style.visibility = "hidden";

        document.getElementById("sel_ingredients3").style.visibility = "hidden";
        document.getElementById("sel_potions3").style.visibility = "hidden";
        document.getElementById("sel_avatarItems3").style.visibility = "visible";
    }
    else if (value == "starstones" || value == "coins" || value == "avatar_items" || value == "stamina_potions") {
        document.getElementsByClassName("quantity")[5].style.visibility = "visible";
        document.getElementsByClassName("quantity")[4].style.visibility = "visible";

        document.getElementById("sel_ingredients3").style.visibility = "hidden";
        document.getElementById("sel_potions3").style.visibility = "hidden";
        document.getElementById("sel_avatarItems3").style.visibility = "hidden";
    }
    else {
        document.getElementsByClassName("quantity")[5].style.visibility = "hidden";
        document.getElementsByClassName("quantity")[4].style.visibility = "hidden";

        document.getElementById("sel_ingredients3").style.visibility = "hidden";
        document.getElementById("sel_potions3").style.visibility = "hidden";
        document.getElementById("sel_avatarItems3").style.visibility = "hidden";
        resetSelection("sel_item_ids3[]");
    }
}