// fetch("https://100096.pythonanywhere.com/room_list/login")
//   .then(response => response.json())
//   .then(data => {
//     console.log(data.rooms)
//     const roomList = data.rooms;
//     const roomContainer = document.getElementById("room-container");
//     const roomListUl = document.createElement("ul");

//     for (let i = 0; i < roomList.length; i++) {
//       const roomName = roomList[i].room_name;
//       const roomListItem = document.createElement("li");
//       roomListItem.innerText = roomName;
//       roomListUl.appendChild(roomListItem);
//     }

//     roomContainer.appendChild(roomListUl);
//   })
//   .catch(error => console.error(error));


// fetch(`https://100096.pythonanywhere.com/room_list/login`)
//   .then(response => response.json())
//   .then(data => {
//     console.log(data.rooms)
//     const element = document.createElement('div')
//     element.textContent = data.someProperty
//     document.body.appendChild(element)
//   })
//   .catch(error => console.error(error))

function loadRoom(){
fetch('https://100096.pythonanywhere.com/room_list/login')
.then (res =>res.json())
.then (data =>displayName(data.rooms))
}

const displayName = rooms =>{
const roomContainer = document.getElementById('room-container')
rooms.forEach(room =>{
console.log(room)
const roomDiv = document.createElement ('div')
roomDiv.innerHTML =`
<h1>Name : ${room. room_name}</h1>
<button onClick="loadRoomDetails(${room.room_id})">Id</button>
`;
roomContainer.appendChild(roomDiv)
})
}

const loadRoomDetails =(info)=>{
  
console.log('David',info)
}
loadRoom()