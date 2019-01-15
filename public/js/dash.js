$(document).ready(function() { 

var elements = [];

function dragUser(element, event) {
    var index = elements.indexOf(element);
    var thisID = element.id
    console.log(index)
    if (index == -1) {
        // not already existing in the array, add it now
        elements.push(element);
        index = elements.length - 1;
    }

    event.dataTransfer.setData('index', index);
} 

function dropUser(target, event) {
    var element = elements[event.dataTransfer.getData('index')];
    target.appendChild(element);
    if (target.id == "saved") {
      console.log(element.id);
      ajaxPin(element);      
    }
}

function ajaxPin(element) {
      var this_id = element.id
      console.log("I'm working")
      $.ajax({
            type: "PUT",
            url: '/dash/PUT',
            data: {'pin_or_unpin':'pin', 'id':this_id}
            dataType: 'json',
            success : function(data) {
                         console.log(data);
                    } 
                });
    }

function ajaxUnPin(element) {
      var this_id = element.id
      console.log("I'm working")
      $.ajax({
            type: "PUT",
            url: '/dash/PUT',
            dataType: 'json',
            success : function(data) {
                         console.log(data);
                    } 
                });
    }
