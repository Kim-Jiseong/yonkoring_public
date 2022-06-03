const app = new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
      callPlaced: false,
      client: null,
      localStream: null,
      mutedAudio: false,
      mutedVideo: false,
      userOnlineChannel: null,
      onlineUsers: [],
      incomingCall: false,
      incomingCaller: "",
      agoraChannel: null,
      isOneminutesPassed: false,
      isCallDeclined: false,
      isGotCallableStatMessage: false, 
      isWatingCall: false,
    },
    mounted() {
      this.initUserOnlineChannel();
    },
  
    methods: {
      initUserOnlineChannel() {
        const userOnlineChannel = pusher.subscribe("presence-online-channel");
  
        // Start Pusher Presence Channel Event Listeners
  
        userOnlineChannel.bind("pusher:subscription_succeeded", (data) => {
          // From Laravel Echo, wrapper for Pusher Js Client
          //alert(JSON.stringify(data));
          let members = Object.keys(data.members).map((k) => data.members[k]);
          this.onlineUsers = members;

        });
  
        userOnlineChannel.bind("pusher:member_added", (data) => {
          let user = data.info;
          // check user availability
          const joiningUserIndex = this.onlineUsers.findIndex(
            (data) => data.id === user.id
          );
          if (joiningUserIndex < 0) {
            this.onlineUsers.push(user);
          }
        });
  
        userOnlineChannel.bind("pusher:member_removed", (data) => {
          let user = data.info;
          const leavingUserIndex = this.onlineUsers.findIndex(
            (data) => data.id === user.id
          );
          this.onlineUsers.splice(leavingUserIndex, 1);
        });
  
        userOnlineChannel.bind("pusher:subscription_error", (err) => {
          console.log("Subscription Error", err);
        });
  
        userOnlineChannel.bind("an_event", (data) => {
          console.log("a_channel: ", data);
        });

        userOnlineChannel.bind("get-callable-state-from-callee", (data) => {
          if (parseInt(data.caller_id) === parseInt(AUTH_USER_ID)) {
            console.log("Callee's state : " , data.is_callPlaced);
            if (data.is_callPlaced === true) { //상대가 통화중이면 call decline
              console.log("Call Declined")
              this.isCallDeclined = true;
              this.isGotCallableStatMessage = true;
            }
            else {
              console.log("Call Accepted")
              this.isCallDeclined = false;
              this.isGotCallableStatMessage = true;
            }
          }
        });
  
        userOnlineChannel.bind("make-agora-call", (data) => {
          // Listen to incoming call. This can be replaced with a private channel
          
          if (parseInt(data.userToCall) === parseInt(AUTH_USER_ID)) {
            if (this.isWatingCall === true) { //내가 이미 전화를 거는 중 전화가 온다면
              console.log("이미 스테이터스 응답을 기다리는 중입니다");
              return;
            }
            this.sendCallableStateToCaller(data.from, this.callPlaced); //Caller에게 전화를 받을 수 있는 상태인지를 메시지 fetch
            if (this.callPlaced === true) {
              return;
            }
            else {
              this.callPlaced = true;
            }

            const callerIndex = this.onlineUsers.findIndex(
              (user) => user.id === data.from
            );

            this.incomingCaller = this.onlineUsers[callerIndex]["name"];
            this.incomingCall = true;
            // the channel that was sent over to the user being called is what
            // the receiver will use to join the call when accepting the call.
            this.agoraChannel = data.channelName;
            //통화 들어오면 바로 받게끔 acceptCall 추가함
            document.querySelector('.lobbyContainer').style.display = "none";
            this.acceptCall();
            
            console.log(this.onlineUsers[callerIndex]["id"]);
            let callerID = this.onlineUsers[callerIndex]["id"]
            

            fetch('/agora/', {
              method: "POST",
              body: JSON.stringify({ calleeID: callerID})
            })
            .then(document.querySelector('.call').style.display = 'block')
            .then(response => response.json())
            .then(res => {
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
              if(res.my_request == 0){
                document.getElementById('friend').innerText
                = '친구요청'
              }
              else{
                document.getElementById('friend').innerText
                = '요청취소'
              }
              document.getElementById('friend_pk').innerText
              = res.friend_pk
            })
            .catch(error => console.error(error))

          }
        });
      },
  
      getUserOnlineStatus(id) {
        const onlineUserIndex = this.onlineUsers.findIndex(
          (data) => data.id === id
        );
        if (onlineUserIndex < 0) {
          return "Offline";
        }
        return "Online";
      },

      getUserOnlineUserCount() {
        return this.onlineUsers.length;
      },
  
      async placeCall(callerId) {
        // 랜덤으로 현재 온라인인 사람들에게 전화하는 내용, 매개변수는 전화를 건 사람의 id (caller) 
        // document.querySelector('.lobbyContainer').style.display = "none";

        this.isWatingCall = true;
        
        
        let randNum;
        while (true) {
          randNum = Math.floor(Math.random() * this.onlineUsers.length);

          if (this.onlineUsers[randNum].id != callerId) break;
          if (this.onlineUsers.length <= 1) return;
        }
        const id = this.onlineUsers[randNum].id;
        const calleeName = this.onlineUsers[randNum].name;

        console.log("========== 전화 시도 : " + calleeName + "==========");
        //===================================================
        try {
          // channelName = the caller's and the callee's id. you can use anything. tho.
          const channelName = `${AUTH_USER}_${id}`;
          const tokenRes = await this.generateToken(channelName);
  
          // // Broadcasts a call event to the callee and also gets back the token
          // views에 json 형식으로 전화 수신인, 채널 이름 등의 정보를 보내줌. 
          // view에서는 그 정보로 'presence-online-channel', 'make-agora-call' 등 메서드를 trigger 시킴
          let placeCallRes = await axios.post(
            "/call-user/",
            {
              user_to_call: id,
              channel_name: channelName,
            },
            {
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": CSRF_TOKEN,
              },
            })

          //상대가 전화를 받을 수 있는 상태인지 알게 될때까지 Interval. 10초가 지나면 Timeout
          let connetionTimeoutCount = 0;

          var interval = setInterval(() => {
            if (this.isGotCallableStatMessage === false) {
              console.log("상대의 통화가능 상태 여부를 받아오기까지 대기합니다..", connetionTimeoutCount);
            }
            else if (this.isGotCallableStatMessage === true) {
              this.isGotCallableStatMessage = false;
              this.isWatingCall = false;

              if (this.callPlaced === true) {
                clearInterval(interval);
                throw ("내가 전화걸기 전 먼저 걸려온 전화가 있습니다!");
              }

              if (this.isCallDeclined === false) { //전화 성공시
                //통화 건 사람의 상대방의 프로필을 html에 넣어주는 함수
                document.querySelector('.lobbyContainer').style.display = "none";
                
                //전화 건 사람의 남은 시간을 보여줌
                setInterval(() => {
                  this.client.getSessionStats((stats) => {
                    // console.log(`Current Session Duration: ${420 - stats.Duration}`);
                    remainTime = 420 - stats.Duration;
                    remainMin = Math.floor(remainTime / 60);
                    remainSec = remainTime - remainMin * 60;
                    if (remainSec.toString().length == 1) remainSec = "0" + remainSec;
                    document.querySelector('.remainTime').innerText = remainMin + ":" + remainSec;
                    //7분 지나면 끊어지게
                    if(remainTime == 0) this.endCall();
                  });
                }, 1000)

                fetch('/agora/', {
                  method: "POST",
                  body: JSON.stringify({ calleeID: id})
                })
                .then(document.querySelector('.call').style.display = 'block')
                .then(response => response.json())
                .then(res => {
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
                  if(res.my_request == 0){
                    document.getElementById('friend').innerText
                    = '친구요청'
                  }
                  else{
                    document.getElementById('friend').innerText
                    = '요청취소'
                  }
                  document.getElementById('friend_pk').innerText
                  = res.friend_pk
                })
                .catch(error => console.error(error))

                this.initializeAgora(tokenRes.data.appID);
                this.joinRoom(tokenRes.data.token, channelName);
                clearInterval(interval);
              }
              else {
                clearInterval(interval);
                throw ("상대가 이미 통화중입니다! (Declined)");
              }
            }
            
            if (connetionTimeoutCount >= 10){ //10초가 지나도 연결안되면
              this.isWatingCall = false;
              clearInterval(interval);
              throw ("Connetion Timeout");
            }
            connetionTimeoutCount += 1;
          }, 1000)

        } catch (error) {
          console.log(error);
        }
      },
  
      async acceptCall() {
        const tokenRes = await this.generateToken(this.agoraChannel);
        this.initializeAgora(tokenRes.data.appID);
        let remainTime = 420;
        let remainMin = 0;
        let remainSec = 0;
  
        this.joinRoom(tokenRes.data.token, this.agoraChannel);
        this.incomingCall = false;
        this.callPlaced = true;

        //전화 받은 사람의 남은 시간 보여줌
        setInterval(() => {
          this.client.getSessionStats((stats) => {
            // console.log(`Current Session Duration: ${420 - stats.Duration}`);
            remainTime = 420 - stats.Duration;
            remainMin = Math.floor(remainTime / 60);
            remainSec = remainTime - remainMin * 60;
            if (remainSec.toString().length == 1) remainSec = "0" + remainSec;
            document.querySelector('.remainTime').innerText = remainMin + ":" + remainSec;
            //7분 되면 끊어지게 
            if(remainTime == 0) this.endCall();
          });
        }, 1000)
      },
  
      declineCall(caller_id) {
        // You can send a request to the caller to
        // alert them of rejected call
        this.incomingCall = false;
      },

      sendCallableStateToCaller (caller_id, callPlaced) {
          fetch('/check-callable-state/', {
            method: "POST",
            body: JSON.stringify({'caller_id': caller_id, 'is_callPlaced': callPlaced}),
            headers: {
                "X-CSRFToken": CSRF_TOKEN,
            },
          });
      },
  
      generateToken(channelName) {
        return axios.post(
          "/token/",
          {
            channelName,
          },
          {
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": CSRF_TOKEN,
            },
          }
        );
      },
  
      /**
       * Agora Events and Listeners
       */
      initializeAgora(agora_app_id) {
        this.client = AgoraRTC.createClient({ mode: "rtc", codec: "h264" });
        this.client.init(
          agora_app_id,
          () => {
            console.log("AgoraRTC client initialized");
          },
          (err) => {
            console.log("AgoraRTC client init failed", err);
          }
        );
      },
  
      async joinRoom(token, channel) {
        this.client.join(
          token,
          channel,
          AUTH_USER,
          (uid) => {
            console.log("User " + uid + " join channel successfully");
            this.callPlaced = true;

            this.createLocalStream();
            this.initializedAgoraListeners();
            
          },
          (err) => {
            console.log("Join channel failed", err);
          }
        );
      },

      initializedAgoraListeners() {
        //   Register event listeners
        this.client.on("stream-published", function (evt) {
          console.log("Publish local stream successfully");
          console.log(evt);
        });
        

        //subscribe remote stream
        this.client.on("stream-added", ({ stream }) => {
          console.log("New stream added: " + stream.getId());
          this.client.subscribe(stream, function (err) {
            console.log("Subscribe stream failed", err);
          });
        });
  
        this.client.on("stream-subscribed", (evt) => {
          // Attach remote stream to the remote-video div
  
          console.log("incoming remote stream event: ", evt);
  
          evt.stream.play("remote-video");
          this.client.publish(evt.stream);

          

        });
  
        this.client.on("stream-removed", ({ stream }) => {
          console.log(String(stream.getId()));
          stream.close();
        });
  
        this.client.on("peer-online", (evt) => {
          console.log("peer-online", evt.uid);
          
        });
  
        //상대가 나가면
        this.client.on("peer-leave", (evt) => {
          var uid = evt.uid;
          var reason = evt.reason;
          console.log("remote user left ", uid, "reason: ", reason);
          // 상대가 전화 끊으며 나도 끊어지게
          this.endCall();
          
                   
        });
  
        this.client.on("stream-unpublished", (evt) => {
          console.log(evt);
        });
      },

      createLocalStream() {
        this.localStream = AgoraRTC.createStream({
          audio: true,
          video: false, //비디오는 해제
        });
  
        // Initialize the local stream
        this.localStream.init(
          () => {F
            // Play the local stream
            this.localStream.play("local-video");
            // Publish the local stream
            this.client.publish(this.localStream, (err) => {
              console.log("publish local stream", err);
            });
          },
          (err) => {
            console.log(err);
          }
        );
      },
  
      endCall() {
        this.localStream.close();
        this.client.leave(
          () => {
            console.log("Leave channel successfully");
            this.callPlaced = false;

          },
          (err) => {
            console.log("Leave channel failed");
          }
        );
        window.pusher.unsubscribe();
        //전화 끊으면 정보 사라지게

        let remainTime;
        this.client.getSessionStats((stats) => {
          remainTime = 420 - stats.Duration;
        });
        //중간에 전화 끊었을 때 상대방 정보 사라짐
        if(remainTime > 0){
          document.querySelector('.call').style.display = 'none';
          document.querySelector('.info1').style.visibility = 'hidden';
          document.querySelector('.info2').style.visibility = 'hidden';
          document.querySelector('.info3').style.visibility = 'hidden';
          document.querySelector('.lobbyContainer').style.display = "block";
        }
      },
  
      handleAudioToggle() {
        if (this.mutedAudio) {
          this.localStream.unmuteAudio();
          this.mutedAudio = false;
        } else {
          this.localStream.muteAudio();
          this.mutedAudio = true;
        }
      },
  
      handleVideoToggle() {
        if (this.mutedVideo) {
          this.localStream.unmuteVideo();
          this.mutedVideo = false;
        } else {
          this.localStream.muteVideo();
          this.mutedVideo = true;
        }
      },
    },
  });