let permissions = false;
const endTime = 0;
let remainTime = 423;



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
      callableUsers: [],
      incomingCall: false,
      incomingCallerName: "",
      incomingCallerID: null,
      agoraChannel: null,
      isCallDeclined: false,
      isGotCallableStatMessage: false, 
      isGotAcceptMessage: false,
      isWatingCall: false,
      isCallFinished: false,
      previousCallUserId: null,
    },
    mounted() {
      this.initUserOnlineChannel();
    },
  
    methods: {
      initUserOnlineChannel() {
        const userOnlineChannel = pusher.subscribe("presence-online-channel");
  
        // 이곳에서 Pusher, 이벤트 리스너 등 동작을 정의함
        setInterval(() => {
          console.log(this.callPlaced, this.isCallFinished, this.incomingCall, this.isWatingCall);
          if (!this.callPlaced && !this.isCallFinished && !this.incomingCall && !this.isWatingCall && permissions) {
            this.placeCall(AUTH_USER_ID);
          }
          console.log(this.callableUsers)
          this.getUserOnlineUserCount()
        }, 5000); //5초 간격으로 전화시도

        setInterval(() => {
          if (!this.callPlaced && !this.isCallFinished && !this.incomingCall && !this.isWatingCall && permissions) {
          this.addCallableUsersToAlluser();
          this.resetCallableUsers();
          }
        }, 10000); //10초 간격으로 나를 모든 유저들의 신규 callableuser 풀에 추가시켜줌

        userOnlineChannel.bind("pusher:subscription_succeeded", (data) => {
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

          const callableUserIndex = this.callableUsers.findIndex(
            (data) => data.id === user.id
          );
          if (callableUserIndex < 0) {
            this.callableUsers.push(user);
          }
        });
  
        userOnlineChannel.bind("pusher:member_removed", (data) => {
          let user = data.info;
          console.log(user);
          const leavingUserIndex = this.onlineUsers.findIndex(
            (data) => data.id === user.id
          );
          this.onlineUsers.splice(leavingUserIndex, 1);

          const leavingCallableUserIndex = this.callableUsers.findIndex(
            (data) => data.id === user.id
          );
          this.callableUsers.splice(leavingCallableUserIndex, 1);
        });
  
        userOnlineChannel.bind("pusher:subscription_error", (err) => {
          console.log("Subscription Error", err);
        });
  
        userOnlineChannel.bind("get-callable-state-from-callee", (data) => {
          if (parseInt(data.caller_id) === parseInt(AUTH_USER_ID)) {
            if (data.is_unable_to_call) { //상대가 통화중이면 call decline
              console.log("Call Declined")
              this.isCallDeclined = true;
            }
            else {
              console.log("Call Accepted")
              this.isCallDeclined = false;
            }
            this.isGotCallableStatMessage = true;
          }
        });
        
        userOnlineChannel.bind("get-accept-message-from-opponent", (data) => {
          if (parseInt(data.opponent_id) === parseInt(AUTH_USER_ID)) {
            console.log("get-accept-message-from-opponent 실행됨")
            this.isGotAcceptMessage = true;
          }
        });

        userOnlineChannel.bind("add-callable-users", (data) => { //통화가능 인원에 신규 추가
          if (parseInt(data.id) != parseInt(AUTH_USER_ID)) //자기 자신 제외
          {
            const newUserIndex = this.callableUsers.findIndex(
              (user) => user.id === data.id
            );
            if (newUserIndex < 0) {
              this.callableUsers.push(data);
              console.log("add-callable-users : ", this.callableUsers);  
            }
          }
        });

        userOnlineChannel.bind("make-agora-call", (data) => {
          // 전화가 걸려왔을 때 실행되는 이벤트
            if (parseInt(data.userToCall) === parseInt(AUTH_USER_ID)) {
              let isUnableToCall;
              console.log("직전 상대 ID : " , data.from === this.previousCallUserId);
              //현재 상대의 id를 직전 상대 id 변수로 저장
              if (this.callPlaced || this.isWatingCall || this.isCallFinished || this.incomingCall || data.genderMatch == false || !permissions || data.from === this.previousCallUserId) {
                isUnableToCall = true;
              }
              else {
                isUnableToCall = false;
              }
  
              this.sendCallableStateToCaller(data.from, isUnableToCall); //Caller에게 전화를 받을 수 있는 상태인지를 메시지 fetch
              if (isUnableToCall === true) return;

              const callerIndex = this.onlineUsers.findIndex(
                (user) => user.id === data.from
              );
  
              this.incomingCallerName = this.onlineUsers[callerIndex]["name"];
              this.incomingCallerID = this.onlineUsers[callerIndex]["id"];
              this.incomingCall = true;
              this.isGotAcceptMessage = false;
              incomingCallModal();

              // the channel that was sent over to the user being called is what
              // the receiver will use to join the call when accepting the call.
              this.agoraChannel = data.channelName;
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
        console.log(this.onlineUsers.length + '명이 통화 페이지에 있습니다.')
        return this.onlineUsers.length;
      },
  
      async placeCall(callerId) {
        if(!permissions) return;
        // 랜덤으로 현재 온라인인 사람들에게 전화하는 내용, 매개변수는 전화를 건 사람의 id (caller) 
        if (this.callableUsers.length < 1 ) return; //전화가능 인원이 없으면 return
        this.isWatingCall = true;

        let randNum;
        while (true) {
          randNum = Math.floor(Math.random() * this.callableUsers.length);
          if (this.callableUsers[randNum].id != callerId) break;
          if (this.onlineUsers.length <= 1) return;
        }
        if (this.callableUsers[randNum].id == this.previousCallUserId) 
        {
          this.isWatingCall = false;
          console.error("직전에 통화한 상대입니다!");
          return;
        }


        const id = this.callableUsers[randNum].id;
        const calleeName = this.callableUsers[randNum].name;


        console.log("========== 전화 시도 : " + calleeName + "==========");
        //===================================================
        try {
          // channelName = the caller's and the callee's id. you can use anything. tho.
          const channelName = `${AUTH_USER}_${calleeName}`;
          this.agoraChannel = channelName;

          console.log('채널 이름:'+channelName);

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

              if (this.isCallDeclined === false) { //전화 성공시
                //통화 건 사람의 상대방의 프로필을 html에 넣어주는 함수
                this.isGotAcceptMessage = false;
                this.incomingCall = true;
                incomingCallModal();

                this.incomingCallerName = calleeName;
                this.incomingCallerID = id;
                //현재 상대의 id를 직전 상대 id 변수로 저장
                clearInterval(interval);
              }
              else {
                this.isWatingCall = false;
                clearInterval(interval);
                throw ("상대가 전화를 받을 수 없는 상태입니다! (Declined)");
              }
            }
            
            if (connetionTimeoutCount >= 5){ //5초가 지나도 연결안되면
              this.isWatingCall = false;
              this.resetCallableUsers();
              clearInterval(interval);
              throw ("Connetion Timeout");
            }
            connetionTimeoutCount += 1;
          }, 1000)

        } catch (error) {
          this.isWatingCall = false;
          console.log(error);
        }
      },
  
      async acceptCall() {
        this.sendAcceptMessageToOpponent(this.incomingCallerID);
        disableAcceptButton();
        const tokenRes = await this.generateToken(this.agoraChannel);
        var interval = setInterval(() => {
          console.log("this.isGotAcceptMessage : ", this.isGotAcceptMessage);
          if (this.isGotAcceptMessage === true) {
            this.isGotAcceptMessage = false;
            this.initializeAgora(tokenRes.data.appID); 
            this.joinRoom(tokenRes.data.token, this.agoraChannel);
            CreateCallMainUI(this.onlineUsers, this.incomingCallerID);
            this.previousCallUserId = this.incomingCallerID;
            ReleaseCallSearch();
            this.callPlaced = true;
            clearInterval(interval);
          }
          if (this.incomingCall === false) //(시간 지나 모달창 사라지면 incomingCall은 False가 됨)
          {
              clearInterval(interval);
          }
        }, 1000);
      },
  
      declineCall(caller_id) {
        // You can send a request to the caller to
        // alert them of rejected call
        ReleaseCallSearch();
        delete_incomingCallModal();
        ringingToneSound();
      },

      sendCallableStateToCaller (caller_id, isUnableToCall) {
          fetch('/check-callable-state/', {
            method: "POST",
            body: JSON.stringify({'caller_id': caller_id, 'is_unable_to_call': isUnableToCall}),
            headers: {
                "X-CSRFToken": CSRF_TOKEN,
            },
          });
      },

      sendAcceptMessageToOpponent (opponent_id) {
        console.log("send-accept-message 실행됨");
        fetch('/send-accept-message/', {
          method: "POST",
          body: JSON.stringify({'opponent_id': opponent_id}),
          headers: {
              "X-CSRFToken": CSRF_TOKEN,
          },
        });
      },

      addCallableUsersToAlluser () {        
        fetch('/add-callable-users/', {
          method: "POST",
          body: JSON.stringify({'id': AUTH_USER_ID, 'name': AUTH_USER}),
          headers: {
              "X-CSRFToken": CSRF_TOKEN,
          },
        });
      },

      resetCallableUsers () {
        this.callableUsers = [];
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
            callPlacedSound();

            this.createLocalStream();
            this.initializedAgoraListeners();

            this.startClockCount();
            this.checkOpponentIsActive()

            axios.post('/game/')
              .then(
              res => {
                document.querySelector('.game_text').innerHTML = res.data.game;
              }
            )
            
          },
          (err) => {
            console.log("Join channel failed", err);
          }
        );
      },

      startClockCount() {
        //전화 받은 사람의 남은 시간 보여줌
        setInterval(() => {
          this.client.getSessionStats((stats) => {
            remainTime = makeRemainTime(stats.Duration);
            TimeUp(remainTime);
            //7분 되면 끊어지게 
            if(remainTime == endTime) this.endCall();
            if(remainTime == 415) document.querySelector('.closeCallBtn').style.visibility = 'visible';         
          });
        }, 1000)
      },

      checkOpponentIsActive() {
        //13초 후에, 이 채널에 유저가 1명 뿐이면 (연결이 안됐으면)
        setTimeout(() => {
          this.client.getSessionStats((stats) => {
            console.log(stats.UserCount)
            if (stats.UserCount <= 1) {
              callModal();
              document.querySelector('.modal_text').innerHTML = "상대가 채널에 미접속하여<br>통화가 종료되었습니다."
              setTimeout(() => {this.endCall();}, 3000)
            }
          } );
        },13000);
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
          () => {
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

        
        this.client.getSessionStats((stats) => {
          remainTime = 423 - stats.Duration;
        });
        //중간에 전화 끊었을 때 상대방 정보 사라지고 다시 통화 연결중 보이게
        //딜레이 때문에 1초 플러스
        if(remainTime > endTime + 360){
          changeToMatchingPage();
          endCallSound();
          setTimeout(() => {
            ringingToneSound();
          }, 1000)
        }
        else {
          changeToCallFinishPage()
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

function getStateOfCallFinished() {
  return app.isCallFinished;
}

function getStateOfCallPlaced() {
  return app.callPlaced;
}

function setStateOfCallFinished(value) {
  app.isCallFinished = value;
}

function ReleaseCallSearch() {
  app.isWatingCall = false;
  app.incomingCall = false;
}