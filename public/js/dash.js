
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
    } else if (target.id == "unassigned") {
      console.log(element.id);
      ajaxUnPin(element);
    } 
}

function ajaxPin(element) {
      var this_id = element.id
      console.log("I'm working")
      $.ajax({
            type: "PUT",
            url: '/update/PUT',
            data: {'pinit':'pin', 'item':this_id},
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
            url: '/update/PUT',
            data: {'pinit':'unpin', 'item':this_id},
            dataType: 'json',
            success : function(data) {
                         console.log(data);
                    } 
                });
    }


$('#hideshow').hide();

$('.options').click(function () {
    $("#hideshow").toggle("slide");
});
