$("#field").change(function () {
    var changeVal = $("#field").val();
    if (changeVal.charAt(0) == '=' && changeVal.length >= 13) {
        //Extract the changeVal Number.
        changeVal = changeVal.substr(1, 13);
    }
    $("#field").val(changeVal);
});

$("#prNum").change(function () {
    var changePc = $("#prNum").val();
    if (changePc.charAt(0) == '=' && changePc.charAt(1) == "<") {
        //Extract the changeVal Number.
        changePc = changePc.substr(2, 5);
    }
    $("#prNum").val(changePc);
});

$("#typeNum").change( function(){

    var newType = $("#typeNum").val();
    if(newType.charAt(0) == "=" && newType.charAt(1) == "%"){
    
    newType = newType.substr(2,2);
    }

    if (newType == 51) {
    
     newType = 'O POS';
    
     }else if (newType == 95) {
    
     newType = 'O NEG'; 
    
     } else if (newType == 62) {
    
     newType = 'A POS'; 
    
     } else if (newType == 06) {
    
     newType = 'A NEG';
    
     } else if (newType == 73) {
    
     newType = 'B POS';
   
     } else if (newType == 17) {
    
     newType = 'B NEG';    
    
     } else if (newType == 84) {
    
     newType = 'AB POS';
    
     } else if (newType == 28) {
    
     newType = 'AB NEG';
    
     }             
    
    $("#typeNum").val(newType);

});

$("#dateNum").change(function () {

    var fixDate = $("#dateNum").val();
    if (fixDate.charAt(0) == '&' && fixDate.charAt(1) == '>') {
        fixDate = fixDate.substr(3, 5);
    };

    var yy = fixDate.slice(0, 2);
    var jDate = fixDate.slice(2, 5);
    var someDate = new Date("jan 0");

    someDate.setDate(parseFloat(someDate.getDate()) + parseFloat(jDate));
    someDate.setFullYear(parseFloat(someDate.getFullYear()) + parseFloat(yy));

    var dd = someDate.getDate();
    var mm = someDate.getMonth() + 1;
    var y = someDate.getFullYear();

    var someFormattedDate = mm + '/' + dd + '/' + y;


    $("#dateNum").val(someFormattedDate);
});

