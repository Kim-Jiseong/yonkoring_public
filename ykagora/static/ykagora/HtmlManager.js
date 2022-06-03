function changeToMatchingPage() {
    // 프로필 안보이게
    document.querySelector('.call').style.display = 'none';
    document.querySelector('.footer').style.display = 'none';
    // 프로필 초기화
    document.querySelector('.info1').style.visibility = 'hidden';
    document.querySelector('.info2').style.visibility = 'hidden';
    document.querySelector('.info3').style.visibility = 'hidden';
    document.querySelector('#friend').style.visibility = 'hidden';
    document.querySelector('.another_friend').style.visibility = 'hidden';
    document.querySelector('.remainTime').style.visibility = 'visible';
    document.querySelector('.img').style.filter = 'blur(10px)';
    document.querySelector('.remainTime').innerText = '7:00'
    // 통화 연결 중
    document.querySelector('.lobbyContainer').style.display = "block";
    document.querySelector('.fa-arrow-left').style.display = "block";

    setStateOfCallFinished(false);
}

function changeToCallFinishPage() {
    // 친구요청, 다른 친구와 통화하기 보이게
    document.querySelector('#friend').style.visibility = 'visible';
    document.querySelector('.another_friend').style.visibility = 'visible';
    //푸터 살리고 끊기 버튼, 남은 시간 사라지게
    document.querySelector('.footer').style.display = "flex";
    document.querySelector('.closeCallBtn').style.visibility = 'hidden';
    document.querySelector('.remainTime').style.visibility = 'hidden';

    setStateOfCallFinished(true);
}

function makeRemainTime(time) {
    remainTime = 423;
    remainTime = 423 - time;
    remainMin = Math.floor(remainTime / 60);
    remainSec = remainTime - remainMin * 60;

    // 7분 남았을 때부터 화면에 보이게
    if(remainTime <= 420){
        if (remainSec.toString().length == 1) remainSec = "0" + remainSec;
        document.querySelector('.remainTime').innerText = remainMin + ":" + remainSec;
    }
    return remainTime;
}

function callModal() {
    const modal = document.querySelector(".modal_wrap")
    const bg = document.querySelector(".black_bg")
    modal.style.display = "flex"
    bg.style.display = "flex"
    let second=0;
    // 모달창 3초만 띄우기
    var interval = setInterval(() => {
        second += 1;
        if (second >= 3)
        {
            modal.style.display = "none"
            bg.style.display = "none"
            clearInterval(interval);
        }
    }, 1000);
}

function incomingCallModal() {
  incomingCallSound();
  const modal = document.getElementById("incoming_modal")
  const bg = document.querySelector(".black_bg")
  const acceptBtn = document.querySelector(".acceptBtn")
  const declineBtn = document.querySelector(".declineBtn")
  const modalTimer = document.querySelector("#modalTimer")
  modal.style.display = "flex"
  bg.style.display = "flex"
  acceptBtn.innerText = "확인"
  acceptBtn.style.backgroundColor = "#25D482";
  declineBtn.style.display = "block"

  acceptBtn.disabled = false;
  declineBtn.disabled = false;
  let second = 10;
  modalTimer.innerText = second;
  // 모달창 10초만 띄우기
  var interval = setInterval(() => {
      second -= 1;
      if (second >= 0)
      {
          modalTimer.innerText = second;
      }
      if (second <= 0) //0초 되면 버튼 클릭 못하게 막고
      {
          acceptBtn.disabled = true;
          acceptBtn.style.backgroundColor = "grey";
          declineBtn.style.display = "none"
      }
      if (second <= -3) //5초 동안은 상대의 지연된 응답을 기다림
      {
          ReleaseCallSearch();
          delete_incomingCallModal();
          clearInterval(interval);
      }
  }, 1000);
}

function delete_incomingCallModal() {
  const modal = document.getElementById("incoming_modal")
  const bg = document.querySelector(".black_bg")
  modal.style.display = "none"
  bg.style.display = "none"
}

function disableAcceptButton() {
  const acceptBtn = document.querySelector(".acceptBtn")
  const declineBtn = document.querySelector(".declineBtn")
  acceptBtn.innerText = "상대를 기다리는 중..."
  declineBtn.style.display = "none"
}

function makeProfile(res) {
    document.querySelector('.nickname').innerHTML = `${res.calleeNICKNAME}`;
    document.querySelector('.selfInfoJob').innerHTML = `${res.calleeSELFINFO}`;
    document.querySelector('.bio').innerHTML = `${res.calleeBIO}`;
    document.querySelector('.gender').innerHTML = `<strong>성별:</strong>${res.calleeGENDER}`;
    document.querySelector('.info2').innerHTML 
      = `<p class="info">${res.calleeGOAL}</p>`;
    document.querySelector('.info1').innerHTML 
      = `<p class="info"><strong>나이:</strong>${res.calleeAGE}</p>
      <p class="info"><strong>학교:</strong>${res.calleeSCHOOL}</p>
      <p class="info"><strong>MBTI:</strong>${res.calleeMBTI}</p>`;
    if(!res.calleeCLUB){
      document.querySelector('.info3').innerHTML 
      = `<p class="info"><strong>위치:</strong>${res.calleeADDRESS}</p>`;
    }
    else{
      document.querySelector('.info3').innerHTML 
        = `<p class="info"><strong>위치:</strong>${res.calleeADDRESS}</p>
        <p class="info"><strong>활동이력:</strong>${res.calleeCLUB}</p>`;
    }
    if(res.calleeINTEREST){
      document.querySelector('.interest').innerHTML 
        = `<p class="info">${res.calleeINTEREST}</p>`;
    }
    document.querySelector('.img').setAttribute('src', res.calleeIMG);
    if (res.check_friend == 'yes') {
      document.getElementById('friend').innerText 
      = '이미친구'
      document.getElementById('friend').disabled = true;
      document.getElementById('friend').style.backgroundColor = '#EAECEE';
      document.getElementById('friend').style.color = '#929DA9';
      console.log('이미친구')

    }
    else if(res.my_request == 0){
      document.getElementById('friend').innerText
      = '친구요청'
      document.getElementById('friend').disabled = false;
      document.getElementById('friend').style.backgroundColor = '#25D482';
      document.getElementById('friend').style.color = '#FFFFFF';
      console.log('친구요청')
    }
    else{
      document.getElementById('friend').innerText
      = '요청취소'
      document.getElementById('friend').disabled = false;
      document.getElementById('friend').style.backgroundColor = '#EAECEE';
      document.getElementById('friend').style.color = '#929DA9';
      console.log('요청취소')
    }
    document.getElementById('friend_pk').innerText
    = res.friend_pk
  } 

  function TimeUp(remainTime) {
    if (remainTime === 390) {
      let array1 = document.querySelectorAll('.info1');
      for (let i = 0; i < array1.length; i++) {
          array1[i].style.visibility = 'visible';
      }
      document.querySelector('.img').style.filter = 'blur(10px)'
    }
    if (remainTime === 330) {
        let array2 = document.querySelectorAll('.info2');
        for (let i = 0; i < array2.length; i++) {
            array2[i].style.visibility = 'visible';
        }
        document.querySelector('.img').style.filter = 'blur(8px)';
    }
    if (remainTime === 300) {
      document.querySelector('.img').style.filter = 'blur(6px)'
    }
    if (remainTime === 240) {
      document.querySelector('.img').style.filter = 'blur(4px)'
    }
    if (remainTime === 180) {
        let array3 = document.querySelectorAll('.info3');
        for (let i = 0; i < array3.length; i++) {
            array3[i].style.visibility = 'visible';
        }
        document.querySelector('.img').style.filter = 'blur(3px)'
    }
    if (remainTime === 120) {
      document.querySelector('.img').style.filter = 'blur(2px)'
    }
    if (remainTime === 60) {
      document.querySelector('.img').style.filter = 'blur(1px)'
    }
    if (remainTime === 5) {
      document.querySelector('.img').style.filter = 'blur(0px)'
    }
  }

  function CreateCallMainUI(onlineUsers, callerID) {
    delete_incomingCallModal();
    document.querySelector('.lobbyContainer').style.display = "none";
    callModal();             

    // console.log(onlineUsers[callerIndex]["id"]);
    // let callerID = onlineUsers[callerIndex]["id"]

    fetch('/call/', {
      method: "POST",
      body: JSON.stringify({ calleeID: callerID})
    })
    .then(document.querySelector('.call').style.display = 'block')
    .then(response => response.json())
    .then(res => {
      makeProfile(res);
    })
    .catch(error => console.error(error))
  }