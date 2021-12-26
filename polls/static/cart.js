//xu ly su kien khi nhan nut add to cart
var updateBtns = document.getElementsByClassName("update-cart") //create an event handler for each button-query all the car items

//create loop through all button and add an event listener on click
//get Product Id that we just set the action
for( var i=0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',  productId, 'action:', action)
        //authentication user
        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action){
    console.log('Not logged in ...')

    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] +=1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            console.log('remove Item')
            delete cart[productId]
        }
    }

    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=; path=/"
    location.reload()
}

//send productId and action to the Backend to our view 
function updateUserOrder(productId, action){
    console.log('User is logged in, sending data...')

    //to send data we're gonna use the fetch API
    // before we're gonna set the URL that we want to send the post data
    var url = '/update_item/'  //this is URL and view that we just created so this's where we want to send the data to

    // to fetch to send data
    fetch(url, {
        method:'POST', 
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action':action})

    })
    .then((response) =>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })
}
