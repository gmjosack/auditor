var auditor = {

    atBottom: function(elem){
        return (elem[0].scrollHeight - elem.scrollTop()) === elem.innerHeight();
    }

}
